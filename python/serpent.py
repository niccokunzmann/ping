"""
ast.literal_eval() compatible object tree serialization.

Serpent serializes an object tree into bytes (utf-8 encoded string) that can
be decoded and then passed as-is to ast.literal_eval() to rebuild it as the
original object tree. As such it is safe to send serpent data to other
machines over the network for instance (because only 'safe' literals are
encoded).

Compatible with Python 2.6+ (including 3.x), IronPython 2.7+, Jython 2.7+.

Serpent handles several special Python types to make life easier:

 - str  --> promoted to unicode (see below why this is)
 - bytes, bytearrays, memoryview, buffer  --> string, base-64
   (you'll have to manually un-base64 them though)
 - uuid.UUID, datetime.{datetime, time, timespan}  --> appropriate string/number
 - decimal.Decimal  --> string (to not lose precision)
 - array.array typecode 'c'/'u' --> string/unicode
 - array.array other typecode --> list
 - Exception  --> dict with some fields of the exception (message, args)
 - all other types  --> dict with  __getstate__  or vars() of the object

Note: all str will be promoted to unicode. This is done because it is the
default anyway for Python 3.x, and it solves the problem of the str/unicode
difference between different Python versions. Also it means the serialized
output doesn't have those problematic 'u' prefixes on strings.

Note: the serializer is not thread-safe. Make sure you're not making changes
to the object tree that is being serialized, and don't use the same
serializer in different threads.

Caveat: Python 2.6 cannot deserialize complex numbers (limitation of
ast.literal_eval in 2.6)

Note: because the serialized format is just valid Python source code, it can
contain comments.

Note: set literals are not supported on python <3.2 (ast.literal_eval
limitation). If you need Python < 3.2 compatibility, you'll have to use
set_literals=False when serializing.

Copyright 2013, Irmen de Jong (irmen@razorvine.net)
Software license: "MIT software license". See http://opensource.org/licenses/MIT
"""

from __future__ import print_function, division
import __future__
import ast
import base64
import sys
import types
import os
import gc

__version__ = "1.5"
__all__ = ["dump", "dumps", "load", "loads", "register_class", "unregister_class"]


def dumps(obj, indent=False, set_literals=True, module_in_classname=False):
    """Serialize object tree to bytes"""
    return Serializer(indent, set_literals, module_in_classname).serialize(obj)


def dump(obj, file, indent=False, set_literals=True, module_in_classname=False):
    """Serialize object tree to a file"""
    file.write(dumps(obj, indent=indent, set_literals=set_literals, module_in_classname=module_in_classname))


def loads(serialized_bytes):
    """Deserialize bytes back to object tree. Uses ast.literal_eval (safe)."""
    serialized = serialized_bytes.decode("utf-8")
    if sys.version_info < (3, 0) and sys.platform != "cli":
        if os.name == "java":
            # Because of a bug in Jython we have to manually convert all Str nodes to unicode. See http://bugs.jython.org/issue2008
            serialized = ast.parse(serialized, "<serpent>", mode="eval")
            for node in ast.walk(serialized):
                if isinstance(node, ast.Str) and type(node.s) is str:
                    node.s = node.s.decode("utf-8")
        else:
            # python 2.x: parse with unicode_literals (promotes all strings to unicode)
            serialized = compile(serialized, "<serpent>", mode="eval", flags=ast.PyCF_ONLY_AST | __future__.unicode_literals.compiler_flag)
    try:
        if os.name != "java" and sys.platform != "cli":
            gc.disable()
        return ast.literal_eval(serialized)
    finally:
        gc.enable()


def load(file):
    """Deserialize bytes from a file back to object tree. Uses ast.literal_eval (safe)."""
    data = file.read()
    return loads(data)


_special_classes_registry = {}


def unregister_class(clazz):
    """Unregister the specialcase serializer for the given class."""
    if clazz in _special_classes_registry:
        del _special_classes_registry[clazz]


def register_class(clazz, serializer):
    """
    Register a specialcase serializer function for objects of the given class.
    The function will be called with (object, serpent_serializer, outputstream, indentlevel) arguments.
    The function must write the serialized data to outputstream. It doesn't return a value.
    """
    _special_classes_registry[clazz] = serializer


class BytesWrapper(object):
    """Wrapper for bytes, bytearray etc. to make them appear as base-64 encoded data."""
    def __init__(self, data):
        self.data = data

    def __getstate__(self):
        if sys.platform == "cli":
            b64 = base64.b64encode(str(self.data))  # weird IronPython bug?
        elif (os.name == "java" or sys.version_info < (2, 7)) and type(self.data) is bytearray:
            b64 = base64.b64encode(bytes(self.data))  # Jython bug http://bugs.jython.org/issue2011
        else:
            b64 = base64.b64encode(self.data)
        return {
            "data": b64 if type(b64) is str else b64.decode("ascii"),
            "encoding": "base64"
        }

    @staticmethod
    def from_bytes(data):
        return BytesWrapper(data)

    @staticmethod
    def from_bytearray(data):
        return BytesWrapper(data)

    @staticmethod
    def from_memoryview(data):
        return BytesWrapper(data.tobytes())

    @staticmethod
    def from_buffer(data):
        return BytesWrapper(data)


if sys.version_info < (3, 0):
    _repr = repr     # python <3.0 won't need explicit encoding to utf-8, so we optimize this
else:
    def _repr(obj):
        return repr(obj).encode("utf-8")


class Serializer(object):
    """
    Serialize an object tree to a byte stream.
    It is not thread-safe: make sure you're not making changes to the
    object tree that is being serialized.
    """
    # noinspection PySetFunctionToLiteral
    repr_types = set([
        str,
        int,
        float,
        complex,
        bool,
        type(None)
    ])

    translate_types = {
        bytes: BytesWrapper.from_bytes,
        bytearray: BytesWrapper.from_bytearray
    }

    # do some dynamic changes to the types configuration if needed
    if bytes is str:
        del translate_types[bytes]
    if hasattr(types, "BufferType"):
        translate_types[types.BufferType] = BytesWrapper.from_buffer
    try:
        translate_types[memoryview] = BytesWrapper.from_memoryview
    except NameError:
        pass
    if sys.platform == "cli":
        repr_types.remove(str)  # IronPython needs special str treatment
    if sys.version_info < (2, 7):
        repr_types.remove(float)   # repr(float) prints floating point roundoffs in Python < 2.7

    def __init__(self, indent=False, set_literals=True, module_in_classname=False):
        """
        Initialize the serializer.
        indent=indent the output over multiple lines (default=false)
        setLiterals=use set-literals or not (set to False if you need compatibility with Python < 3.2)
        module_in_classname = include module prefix for class names or only use the class name itself
        """
        self.indent = indent
        self.set_literals = set_literals
        self.module_in_classname = module_in_classname

    def serialize(self, obj):
        """Serialize the object tree to bytes."""
        header = "# serpent utf-8 "
        if self.set_literals:
            header += "python3.2\n"   # set-literals require python 3.2+ to deserialize (ast.literal_eval limitation)
        else:
            header += "python2.6\n"
        out = [header.encode("utf-8")]
        try:
            if os.name != "java" and sys.platform != "cli":
                gc.disable()
            self._serialize(obj, out, 0)
        finally:
            gc.enable()
        if sys.platform == "cli":
            return "".join(out)
        return b"".join(out)

    def _serialize(self, obj, out, level):
        t = type(obj)
        if t in self.translate_types:
            obj = self.translate_types[t](obj)
            t = type(obj)
        if t in self.repr_types:
            out.append(_repr(obj))    # just a simple repr() is enough for these objects
            return
        # check special registered types:
        for clazz in _special_classes_registry:
            if isinstance(obj, clazz):
                _special_classes_registry[clazz](obj, self, out, level)
                return
        # exception?
        if isinstance(obj, BaseException):
            self.ser_exception_class(obj, out, level)
        else:
            # serialize dispatch
            module = t.__module__
            if module == "__builtin__":
                module = "builtins"  # python 2.x compatibility
            method_name = "ser_{0}_{1}".format(module, t.__name__)
            getattr(self, method_name, self.ser_default_class)(obj, out, level)  # dispatch

    def ser_builtins_str(self, str_obj, out, level):
        # special case str, for IronPython where str==unicode and repr() yields undesired result
        self.ser_builtins_unicode(str_obj, out, level)

    def ser_builtins_float(self, float_obj, out, level):
        # special case float, for Python < 2.7, to not print the float roundoff errors
        out.append(str(float_obj))

    def ser_builtins_unicode(self, unicode_obj, out, level):
        # for python 2.x
        z = unicode_obj.encode("utf-8")
        z = z.replace("\\", "\\\\")  # double-escape the backslashes
        z = z.replace("\a", "\\a")
        z = z.replace("\b", "\\b")
        z = z.replace("\f", "\\f")
        z = z.replace("\n", "\\n")
        z = z.replace("\r", "\\r")
        z = z.replace("\t", "\\t")
        z = z.replace("\v", "\\v")
        if "'" not in z:
            z = "'" + z + "'"
        elif '"' not in z:
            z = '"' + z + '"'
        else:
            z = z.replace("'", "\\'")
            z = "'" + z + "'"
        out.append(z)

    def ser_builtins_long(self, long_obj, out, level):
        # used with python 2.x
        out.append(str(long_obj))

    def ser_builtins_tuple(self, tuple_obj, out, level):
        if self.indent and tuple_obj:
            indent_chars = b"  " * level
            indent_chars_inside = indent_chars + b"  "
            out.append(b"(\n")
            for elt in tuple_obj:
                out.append(indent_chars_inside)
                self._serialize(elt, out, level + 1)
                out.append(b",\n")
            out[-1] = out[-1].rstrip()  # remove the last \n
            if len(tuple_obj) > 1:
                del out[-1]  # undo the last ,
            out.append(b"\n" + indent_chars + b")")
        else:
            out.append(b"(")
            for elt in tuple_obj:
                self._serialize(elt, out, level + 1)
                out.append(b",")
            if len(tuple_obj) > 1:
                del out[-1]  # undo the last ,
            out.append(b")")

    def ser_builtins_list(self, list_obj, out, level):
        if self.indent and list_obj:
            indent_chars = b"  " * level
            indent_chars_inside = indent_chars + b"  "
            out.append(b"[\n")
            for elt in list_obj:
                out.append(indent_chars_inside)
                self._serialize(elt, out, level + 1)
                out.append(b",\n")
            del out[-1]  # remove the last ,\n
            out.append(b"\n" + indent_chars + b"]")
        else:
            out.append(b"[")
            for elt in list_obj:
                self._serialize(elt, out, level + 1)
                out.append(b",")
            if list_obj:
                del out[-1]  # remove the last ,
            out.append(b"]")

    def ser_builtins_dict(self, dict_obj, out, level):
        if self.indent and dict_obj:
            indent_chars = b"  " * level
            indent_chars_inside = indent_chars + b"  "
            out.append(b"{\n")
            dict_items = dict_obj.items()
            try:
                sorted_items = sorted(dict_items)
            except TypeError:  # can occur when elements can't be ordered (Python 3.x)
                sorted_items = dict_items
            for k, v in sorted_items:
                out.append(indent_chars_inside)
                self._serialize(k, out, level + 1)
                out.append(b": ")
                self._serialize(v, out, level + 1)
                out.append(b",\n")
            del out[-1]  # remove last ,\n
            out.append(b"\n" + indent_chars + b"}")
        else:
            out.append(b"{")
            for k, v in dict_obj.items():
                self._serialize(k, out, level + 1)
                out.append(b":")
                self._serialize(v, out, level + 1)
                out.append(b",")
            if dict_obj:
                del out[-1]  # remove the last ,
            out.append(b"}")

    def ser_builtins_set(self, set_obj, out, level):
        if not self.set_literals:
            if self.indent:
                set_obj = sorted(set_obj)
            self._serialize(tuple(set_obj), out, level)     # use a tuple instead of a set literal
            return
        if self.indent and set_obj:
            indent_chars = b"  " * level
            indent_chars_inside = indent_chars + b"  "
            out.append(b"{\n")
            try:
                sorted_elts = sorted(set_obj)
            except TypeError:   # can occur when elements can't be ordered (Python 3.x)
                sorted_elts = set_obj
            for elt in sorted_elts:
                out.append(indent_chars_inside)
                self._serialize(elt, out, level + 1)
                out.append(b",\n")
            del out[-1]  # remove the last ,\n
            out.append(b"\n" + indent_chars + b"}")
        elif set_obj:
            out.append(b"{")
            for elt in set_obj:
                self._serialize(elt, out, level + 1)
                out.append(b",")
            del out[-1]  # remove the last ,
            out.append(b"}")
        else:
            # empty set literal doesn't exist unfortunately, replace with empty tuple
            self.ser_builtins_tuple((), out, level)

    def ser_builtins_frozenset(self, set_obj, out, level):
        self.ser_builtins_set(set_obj, out, level)

    def ser_decimal_Decimal(self, decimal_obj, out, level):
        # decimal is serialized as a string to avoid losing precision
        self._serialize(str(decimal_obj), out, level)

    def ser_datetime_datetime(self, datetime_obj, out, level):
        self._serialize(datetime_obj.isoformat(), out, level)

    if os.name == "java" or sys.version_info < (2, 7):    # jython bug http://bugs.jython.org/issue2010
        def ser_datetime_timedelta(self, timedelta_obj, out, level):
            secs = ((timedelta_obj.days * 86400 + timedelta_obj.seconds) * 10 ** 6 + timedelta_obj.microseconds) / 10 ** 6
            self._serialize(secs, out, level)
    else:
        def ser_datetime_timedelta(self, timedelta_obj, out, level):
            secs = timedelta_obj.total_seconds()
            self._serialize(secs, out, level)

    def ser_datetime_time(self, time_obj, out, level):
        self._serialize(str(time_obj), out, level)

    def ser_uuid_UUID(self, uuid_obj, out, level):
        self._serialize(str(uuid_obj), out, level)

    def ser_exception_class(self, exc_obj, out, level):
        if self.module_in_classname:
            class_name = "%s.%s" % (exc_obj.__class__.__module__, exc_obj.__class__.__name__)
        else:
            class_name = exc_obj.__class__.__name__
        value = {
            "__class__": class_name,
            "__exception__": True,
            "args": exc_obj.args,
            "attributes": vars(exc_obj)  # add any custom attributes
        }
        self._serialize(value, out, level)

    def ser_array_array(self, array_obj, out, level):
        if array_obj.typecode == 'c':
            self._serialize(array_obj.tostring(), out, level)
        elif array_obj.typecode == 'u':
            self._serialize(array_obj.tounicode(), out, level)
        else:
            self._serialize(array_obj.tolist(), out, level)

    def ser_default_class(self, obj, out, level):
        try:
            value = obj.__getstate__()
            if isinstance(value, dict):
                self.ser_builtins_dict(value, out, level)
                return
        except AttributeError:
            if self.module_in_classname:
                class_name = "%s.%s" % (obj.__class__.__module__, obj.__class__.__name__)
            else:
                class_name = obj.__class__.__name__
            try:
                value = dict(vars(obj))  # make sure we can serialize anything that resembles a dict
                value["__class__"] = class_name
            except TypeError:
                if hasattr(obj, "__slots__"):
                    # use the __slots__ instead of the vars dict
                    value = {}
                    for slot in obj.__slots__:
                        value[slot] = getattr(obj, slot)
                    value["__class__"] = class_name
                else:
                    raise TypeError("don't know how to serialize class " + str(obj.__class__) + ". Give it vars() or an appropriate __getstate__")
        self._serialize(value, out, level)
