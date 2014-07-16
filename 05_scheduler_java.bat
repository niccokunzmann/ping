cd %~dp0\java\ping

rem http://stackoverflow.com/questions/6066257/how-to-compile-java-program-with-jar-library

javac -d . -cp lib\pyrolite.jar;lib\serpent.jar src\ping\Scheduler.java

java -cp lib\pyrolite.jar;lib\serpent.jar;. ping.Scheduler

cd %~dp0