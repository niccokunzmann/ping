import Pyro4.naming
import sys
import socket

Pyro4.naming.startNSloop(socket.gethostbyname(socket.gethostname()))
