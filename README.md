About
-----

This project uses [Pyro4](https://github.com/irmen/Pyro4) and [Pyrolite](https://github.com/irmen/Pyrolite) to create a slow sample game of breakout.

We use Python (Python2 or Python3 or Jython or IronPython), C# and Java.

This was tested under Windows and Linux.

Use it
------

Start the files in the following order:

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

Problems
--------

16th of July 2014

-	we create so many open socket connections that there are no left on the computer. PyroProxy in Python creates a new TCP-Connection for every instance. We use double-dispatch between Ball and Block for collision detection. This creates new proxies for every `ball.schedule()` call e.g. every time a ball moves and checks for collision. 

-	In Pyrolite there are no future calls. If we want to get a result this may last some time:

        private void update_balls()
        {
            List<Object> proxies = (List<Object>)playfield.call("get_balls");
            foreach (PyroProxy ball in proxies)
            {
                //synchronous: copy data
                balls.Add(Ball.FromPyroProxy(ball));
            }
        }

-	"Ugly calls": `(int)playfield.call(“get_width”);` instead of `playfield.getWidth();`.
	See [Stackoverflow](http://stackoverflow.com/questions/24365101/generate-method-if-not-existent) for sugestions. It suggests 3 solutions.

-	The IP-address is put into the URI. Because of this we used 

		Pyro4.Daemon(socket.gethostbyname(socket.gethostname()))     

	instead of
 
		Pyro4.Daemon()
	
	Still we are bound to one IP-address.

For more see the final_presenation in the presentations folder.

Suggestions
-----------

[How to create nicer Proxies](http://stackoverflow.com/questions/24365101/generate-method-if-not-existent) with three answers how to circumvent `PyroProy.call("method", ...)` and use `PyroProxy.method(...)` instead.

