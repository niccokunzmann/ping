import Pyro4
import socket

try:
    import hanging_threads
except ImportError:
    pass


class Block(object):

    def __init__(self, playfield):
        self.playfield = playfield
        self.uri = daemon.register(self)
        self.as_proxy = Pyro4.Proxy(self.uri)
        self.playfield.add_block(self.as_proxy)
        print('Block {}'.format(self.uri))

        self.width = 30
        self.height = 5

        self.x = self.playfield.get_width() / 2 - self.get_width() / 2
        self.y = self.playfield.get_height() - self.get_height() - 5
        self.move_not()

    def get_x(self):
        return int(self.x)

    def get_y(self):
        return int(self.y)

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def collides_with_ball(self, ball):
        ball_x = ball.get_x()
        ball_y = ball.get_y()
        ball_radius = ball.get_radius()
        if ball.x < self.x:
            if (ball.x - self.x) ** 2 + (ball_y - self.y) ** 2 < ball_radius:
                ball.repell_from_block(self.as_proxy)
        elif ball_x > self.x + self.width:
            if (ball_x - self.x) ** 2 + (ball_y - self.y) ** 2 < ball_radius:
                ball.repell_from_block(self.as_proxy)
        else:
            if ball_y + ball_radius > self.y:
                ball.repell_from_block(self.as_proxy)
        ball._pyroRelease()

    def schedule(self):
        self.move()

    def asDict(self):
        return dict(x = self.get_x(),
                    y = self.get_y(),
                    height = self.get_height(),
                    width = self.get_width(),
                    )

    def move_left(self):
        self.direction = -1

    def move_right(self):
        self.direction = 1

    def move_not(self):
        self.direction = 0

    def move(self):
        self.x += self.direction
        if self.x < 0:
            self.x = 0
        if self.x + self.width > self.playfield.get_width():
            self.x = self.playfield.get_width() - self.width


class BlockBuilder(object):

    @staticmethod
    def test(*args):
        s = 'called test({})'.format(', '.join(map(str, args)))
        print(s)
        return s

    def create_block(self, playfield):
        return Block(playfield).as_proxy

block_builder = BlockBuilder()

daemon=Pyro4.Daemon(socket.gethostbyname(socket.gethostname()))                 # make a Pyro daemon
ns=Pyro4.locateNS()                   # find the name server
playfield = Pyro4.Proxy(ns.lookup('ping.playfield'))

daemon_proxy = Pyro4.Proxy(daemon.register(daemon))
playfield.add_daemon(daemon_proxy)

uri=daemon.register(block_builder)        # register the greeting object as a Pyro object
ns.register("ping.blocks", uri)    # register the object with a name in the name server
print("Ready. block_builder uri = {}".format(uri))      # print the uri so we can use it in the client later
daemon.requestLoop()                  # start the event loop of the server to wait for calls

ns.remove("ping.blocks")
        
            
