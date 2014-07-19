#!/bin/sh

javac -cp java/ping/lib/pyrolite.jar:java/ping/lib/serpent.jar java/ping/src/ping/Scheduler.java

java -cp java/ping/src:java/ping/lib/pyrolite.jar:java/ping/lib/serpent.jar ping.Scheduler &


