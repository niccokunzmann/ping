import Pyro4
try:
    import hanging_threads
except ImportError:
    pass

class Ball(object):

    def __init__(self, playfield):
        print('Ball', playfield)
        self.playfield = playfield
        self.uri = daemon.register(self)
        self.as_proxy = Pyro4.Proxy(self.uri)

        self.x = self.playfield.get_width() / 2
        self.y = self.playfield.get_height() / 2
        self.radius = 5

        self.direction_x = 0
        self.direction_y = -10
        print(1)
        self.playfield.add_ball(self.as_proxy)
        print(2)
        

    def get_radius(self):
        return self.radius

    def get_x(self):
        return int(self.x)

    def get_y(self):
        return int(self.y)

    def move(self):
        self.x += self.direction_x
        self.y += self.direction_y
        if self.x < self.radius:
            # collision left
            self.x = self.radius * 2 - self.x
            self.direction_x *= -1
        elif self.x + self.radius > self.playfield.get_width():
            # collision right
            self.x = width * 2 - self.radius * 2 - self.x
            self.direction_x *= -1
        if self.y < self.radius:
            # collision top
            self.direction_y *= -1
            self.y = self.radius * 2 - self.y
        elif self.y > self.playfield.get_height():
            # collision bottom
            self.y = self.playfield.get_height()
        for block in self.get_blocks():
            # collision block
            # calls repell_from_block
            block.collides_with(self.as_proxy)

    def get_blocks(self):
        return self.playfield.get_blocks()


    def repell_from_block(self, block):
        direction_x = (self.x - block.get_x() - block.get_width() / 2)
        direction_y = - (self.y - block.get_y() + self.radius + block.get_height())
        size = (direction_x * direction_x + direction_y * direction_y) ** 0.5
        self.direction_x = direction_x * self.velocity / size
        self.direction_y = direction_y * self.velocity / size


class BallBuilder(object):

    @staticmethod
    def test(*args):
        s = 'called test({})'.format(', '.join(map(str, args)))
        print(s)
        return s

    def create_ball(self, playfield):
        return Ball(playfield).as_proxy

ball_builder = BallBuilder()

daemon=Pyro4.Daemon()                 # make a Pyro daemon
ns=Pyro4.locateNS()                   # find the name server
playfield = Pyro4.Proxy(ns.lookup('ping.playfield'))
playfield.add_daemon(daemon)
uri=daemon.register(ball_builder)        # register the greeting object as a Pyro object
ns.register("ping.balls", uri)    # register the object with a name in the name server
print("Ready. ball_builder uri = {}".format(uri))      # print the uri so we can use it in the client later
daemon.requestLoop()                  # start the event loop of the server to wait for calls
ns.remove("ping.balls")
