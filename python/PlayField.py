import Pyro4

class PlayField(object):
    def test(self, *args):
        s = 'called test({})'.format(', '.join(map(str, args)))
        print(s)
        return s

playfield = PlayField()

daemon=Pyro4.Daemon()                 # make a Pyro daemon
ns=Pyro4.locateNS()                   # find the name server
uri=daemon.register(playfield)   # register the greeting object as a Pyro object
ns.register("ping.playfield", uri)  # register the object with a name in the name server
print("Ready. Object uri = {}".format(uri))      # print the uri so we can use it in the client later
daemon.requestLoop()                  # start the event loop of the server to wait for calls
