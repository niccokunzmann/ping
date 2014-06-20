import Pyro4
import Pyro4.errors

ns=Pyro4.locateNS()                   # find the name server
playfield = Pyro4.Proxy(ns.lookup('ping.playfield'))
try:
    playfield.shutdown()
except Pyro4.errors.ConnectionClosedError:
    pass
print('shutdown successful')
