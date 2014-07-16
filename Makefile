all:
	xbuild .net/ping/ping/ping.csproj
	javac -cp java/ping/lib/pyrolite.jar:java/ping/lib/serpent.jar java/ping/src/ping/Scheduler.java

run: all
	./01_namesever.sh &
	sleep 1
	./02_spielfeld.sh &
	sleep 1
	./03_ball.sh &
	sleep 1
	./04_block.sh &
	sleep 1
	java -cp java/ping/src:java/ping/lib/pyrolite.jar:java/ping/lib/serpent.jar ping.Scheduler &
	sleep 1
	./.net/ping/ping/bin/Debug/ping.exe &

.PHONY: all run
