import Pyro4
import time

ns=Pyro4.locateNS()
playfield = Pyro4.Proxy(ns.lookup('ping.playfield'))
while 1:
    balls = playfield.get_balls()
    print('balls: {}'.format(balls))
    for ball in balls:
        print('\tschedule ball {}'.format(ball))
        ball.schedule()
        x = ball.get_x()
        y = ball.get_y()
        print('\t\tx, y : {}, {}'.format(x, y))
    time.sleep(0.5)

