package de.haas.classification;

import java.io.*;

import javax.servlet.*;
import javax.servlet.http.*;

import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;

import java.net.InetSocketAddress;

public class ServLet extends HttpServlet {

	String MODEL = "/home/students/haas/dev/twitter-sentiment-analysis/data/models/def_sentiment_smiley/naive-bayes/full-de-naive-bayes.model";
    //String MODEL = "/home/students/haas/dev/twitter-sentiment-analysis/data/models/def_sentiment_smiley/zeror/full-de-zeror.model";
	WekaWrapper m;

	public ServLet() {
		super();
		try {
			this.m = new WekaWrapper(MODEL);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	
	public void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		response.setContentType("text/html");
		PrintWriter out = response.getWriter();
		out.println("HAllo");

	}

	@Override
	public void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {

		Object obj = JSONValue.parse(request.getReader());
		JSONObject foo = (JSONObject) obj;
		JSONObject res = new JSONObject();
		System.err.println("Server: Got " + foo);

		for (Object key : foo.keySet()) {
			Object value = foo.get(key);

			try {
				String cls = m.classify((String) value);
				res.put(key, cls);
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}

		System.err.println("Server: Sending " + res);

		response.setContentType("application/json");
		PrintWriter out = response.getWriter();
		out.println(res);
		out.close();
	}

	public static void main(String[] args) throws Exception {
        InetSocketAddress bound = new InetSocketAddress("localhost", 8090); 
		Server server = new Server(bound);

		ServletContextHandler context = new ServletContextHandler(
				ServletContextHandler.SESSIONS);
		context.setContextPath("/");
		server.setHandler(context);

		context.addServlet(new ServletHolder(new ServLet()), "/*");

		server.start();
		server.join();
	}

}
