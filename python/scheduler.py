import Pyro4
import time

ns=Pyro4.locateNS()
playfield = Pyro4.Proxy(ns.lookup('ping.playfield'))
while 1:
    for ball in playfield.get_balls() + playfield.get_blocks():
        ball.schedule()
    print('scheduled')
    #time.sleep(0.05)

