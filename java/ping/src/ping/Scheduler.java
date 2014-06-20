package ping;

import net.razorvine.pyro.*;
import java.util.List;

public class Scheduler {

	public static void main (String[] args) throws Exception {
		NameServerProxy ns = NameServerProxy.locateNS(null);
		PyroProxy playfield = new PyroProxy(ns.lookup("ping.playfield"));
		Object result = playfield.call("test", 42, "hello", new int[]{1,2,3});
		String message = (String)result;
		System.out.println("result message="+message);

		while (true) {
			if ((boolean)playfield.call("is_paused")) {
				System.out.println("paused");
			}
			else {
				List<PyroProxy> balls = (List<PyroProxy>)playfield.call("get_balls");
				for(PyroProxy ball:balls) {
					ball.call_oneway("schedule");
				}
			}
			Thread.sleep(100);
		}

		//playfield.close();
		//ns.close();
	}
}
