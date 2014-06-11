import Pyro4

class PlayField(object):

    @staticmethod
    def test(*args):
        s = 'called test({})'.format(', '.join(map(str, args)))
        print(s)
        return s

    def __init__(self):
        self.uri = daemon.register(self)
        self.as_proxy = Pyro4.Proxy(self.uri)
        self.balls = []

    def get_width(self):
        return int(500)

    def get_height(self):
        return int(500)

    def get_balls(self):
        return list(self.balls)

    def create_ball(self):
        uri = ns.lookup('ping.balls')
        ball_builder = Pyro4.Proxy(uri)
        ball = ball_builder.create_ball(self.as_proxy)
        return ball

    def create_block(self):
        uri = ns.lookup('ping.blocks')
        block_builder = Pyro4.Proxy(uri)
        block = block_builder.create_block(self.as_proxy)
        return block

playfield = PlayField()

daemon=Pyro4.Daemon()                 # make a Pyro daemon
ns=Pyro4.locateNS()                   # find the name server
uri=daemon.register(playfield)        # register the greeting object as a Pyro object
ns.register("ping.playfield", uri)    # register the object with a name in the name server
print("Ready. Playfield uri = {}".format(uri))      # print the uri so we can use it in the client later
daemon.requestLoop()                  # start the event loop of the server to wait for calls
