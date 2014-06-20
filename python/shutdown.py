import Pyro4

ns=Pyro4.locateNS()                   # find the name server
playfield = Pyro4.Proxy(ns.lookup('ping.playfield'))
playfield.shutdown()
print('shutdown successful')
