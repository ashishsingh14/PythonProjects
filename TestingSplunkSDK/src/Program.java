import com.splunk.*; 
public class Program {

	// This is a template for new users of the Splunk SDK for Java.
	// The code below connects to a Splunk instance, runs a search,
	// and prints out the results in a crude form.
	public static void main(String[] args) {
		// Create login parameters. We suggest finding
		// a better way to store these than hard coding
		// them in your program for production code.
		ServiceArgs serviceArgs = new ServiceArgs();
		serviceArgs.setUsername("admin");
		serviceArgs.setPassword("Lab123");
		serviceArgs.setHost("172.28.71.106");
		serviceArgs.setPort(8887);
		serviceArgs.setScheme("HTTPS");
		
		//Map<String, Object> connectionArgs = new HashMap<String, Object>();
		
		

		// Create a Service instance and log in with the argument map
		Service service = Service.connect(serviceArgs);
		
		// Set the parameters for the search
		
		// For a full list of options, see:
		//
		//     http://docs.splunk.com/Documentation/Splunk/latest/RESTAPI/RESTsearch#POST_search.2Fjobs

		// oneshotSearchArgs.put("earliest_time", "now-1w");
		// oneshotSearchArgs.put("latest_time",   "now");

		for (Application app : service.getApplications().values()) {
            System.out.println(app.getName());
        }
		
	}

}
