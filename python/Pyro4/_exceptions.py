"""

The exceptions module was removed from Python 2 to Python 3.
Here is the Python 3 version of the exceptions module.



"""

##Traceback (most recent call last):
##  File "C:/Users/wollknaeul/Documents/HPI/_Semester 8/Komponentenprogrammierung und Middleware/ping/python/shutdown.py", line 5, in <module>
##    playfield.shutdown()
##  File "C:/Users/wollknaeul/Documents/HPI/_Semester 8/Komponentenprogrammierung und Middleware/ping/python\Pyro4\core.py", line 163, in __call__
##    return self.__send(self.__name, args, kwargs)
##  File "C:/Users/wollknaeul/Documents/HPI/_Semester 8/Komponentenprogrammierung und Middleware/ping/python\Pyro4\core.py", line 323, in _pyroInvoke
##    data = serializer.deserializeData(msg.data, compressed=msg.flags & Pyro4.message.FLAGS_COMPRESSED)
##  File "C:/Users/wollknaeul/Documents/HPI/_Semester 8/Komponentenprogrammierung und Middleware/ping/python\Pyro4\util.py", line 155, in deserializeData
##    return self.loads(data)
##  File "C:/Users/wollknaeul/Documents/HPI/_Semester 8/Komponentenprogrammierung und Middleware/ping/python\Pyro4\util.py", line 440, in loads
##    return self.recreate_classes(serpent.loads(data))
##  File "C:/Users/wollknaeul/Documents/HPI/_Semester 8/Komponentenprogrammierung und Middleware/ping/python\Pyro4\util.py", line 351, in recreate_classes
##    return self.dict_to_class(literal)
##  File "C:/Users/wollknaeul/Documents/HPI/_Semester 8/Komponentenprogrammierung und Middleware/ping/python\Pyro4\util.py", line 321, in dict_to_class
##    exceptiontype = getattr(exceptions, classname.split('.', 1)[1])
##NameError: name 'exceptions' is not defined


classes = set()

def add(cls):
    if cls in classes or cls.__module__ != Exception.__module__:
        return
    # tribute to
    #   http://stackoverflow.com/questions/436159/how-to-get-all-subclasses
    for cls in cls.__subclasses__():
        add(cls)
    globals()[cls.__name__] = cls
    classes.add(cls)

add(BaseException)
