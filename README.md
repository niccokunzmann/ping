About
-----

This project uses [Pyro4](https://github.com/irmen/Pyro4) and [Pyrolite](https://github.com/irmen/Pyrolite) to create a slow sample game of breakout.

We use Python (Python2 or Python3 or Jython or IronPython), C# and Java.

Use it
------

start the files in the following order:

1 name server  
2 the playfield  
3 the ball builder  
4 the block builder  
5 one of the schedulers  
6 the ping program  

And if you like you can create single items:

10 a ball  
11 a block  

When you are done you can run

99 shutdown  

ERRORS
------

16th of July 2014

-	we create so many open socket connections that there are no left on the computer

Suggestions
-----------

[How to create nicer Proxies](http://stackoverflow.com/questions/24365101/generate-method-if-not-existent) with three answers how to circumvent `PyroProy.call("method", ...)` and use `PyroProxy.method(...)` instead.

