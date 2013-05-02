package de.haas.classification;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.simple.JSONObject;

public class TestServLet {

	public static void main(String args[]) throws IOException {

		//if (args.length < 1) {
		//	System.err.println("Usage: file.arff");
		//}

		// String testFile = args[0];
		String testFile = "data/min.arff";

		StringBuffer content = new StringBuffer();

		BufferedReader r = new BufferedReader(
				new FileReader(new File(testFile)));

		String line;
		while ((line = r.readLine()) != null) {
			content.append(line);
			content.append("\n");
		}

		r.close();

		String key = "blahblah";

		JSONObject obj = new JSONObject();

		obj.put(key, content.toString());

		HttpClient httpclient = new DefaultHttpClient();
		HttpPost httppost = new HttpPost("http://localhost:8080/");

		StringEntity myEntity = new StringEntity(obj.toJSONString(),
				ContentType.create("application/json", "UTF-8"));

		httppost.setEntity(myEntity);

		// Execute and get the response.
		HttpResponse response = httpclient.execute(httppost);
		HttpEntity entity = response.getEntity();

		if (entity != null) {
			InputStream instream = (InputStream) entity.getContent();
			BufferedReader rr = new BufferedReader(new InputStreamReader(
					instream));
			try {
				// do something useful
				String line2;
				while ((line2 = rr.readLine()) != null) {
					System.out.println(line2);

				}
			} finally {
				instream.close();
			}
		}

	}
}
