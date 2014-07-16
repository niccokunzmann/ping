import Pyro4

ns=Pyro4.locateNS()
playfield = Pyro4.Proxy(ns.lookup('ping.playfield'))
playfield.create_block()
