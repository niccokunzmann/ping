import Pyro4
import socket

try:
    import hanging_threads
except ImportError:
    pass


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
        self.blocks = []

    def get_width(self):
        return int(500)

    def get_height(self):
        return int(500)

    def get_balls(self):
        return list(self.balls)

    def get_blocks(self):
        return list(self.blocks)

    def add_ball(self, ball):
        self.balls.append(ball)

    def add_block(self, block):
        self.blocks.append(block)

    def create_ball(self):
        uri = ns.lookup('ping.balls')
        ball_builder = Pyro4.Proxy(uri)
        ball = ball_builder.create_ball(self.as_proxy)
        print('create_ball', ball)
        return ball

    def create_block(self):
        uri = ns.lookup('ping.blocks')
        block_builder = Pyro4.Proxy(uri)
        block = block_builder.create_block(self.as_proxy)
        print('create_block', block)
        return block

daemon=Pyro4.Daemon(socket.gethostbyname(socket.gethostname()))
ns=Pyro4.locateNS()                   # find the name server
playfield = PlayField()
uri = playfield.uri
ns.register("ping.playfield", uri)    # register the object with a name in the name server
print("Ready. Playfield uri = {}".format(uri))      # print the uri so we can use it in the client later
daemon.requestLoop()                  # start the event loop of the server to wait for calls
