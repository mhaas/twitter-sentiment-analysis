package de.haas.classification;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import java.util.Vector;

import weka.classifiers.Classifier;
import weka.classifiers.bayes.*;
import weka.core.Attribute;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.SerializationHelper;

public class WekaWrapper {

	Classifier cl;
	Instances header;

	public WekaWrapper(String model) throws Exception {

		this.cl = (Classifier) SerializationHelper.read(model);
		//this.header = (Instances) v.get(1);

	}

	public String classify(String arff) throws Exception {

		StringReader buf = new StringReader(arff);
		Instances inst = new Instances(buf);
		double pred = cl.classifyInstance(inst.firstInstance());
		Attribute att = inst.firstInstance().attribute(7);
		return att.value((int) pred);
	}

	
	
	public static void main(String[] args) throws Exception {

		if (args.length < 2) {
			System.err.println("Usage: modelFile testFile");
			System.exit(-1);
		}
		String model = args[0];
		String testFile = args[1];
		
		WekaWrapper foo = new WekaWrapper(model);
		
		StringBuffer content = new StringBuffer();
		
		BufferedReader r = new BufferedReader(new FileReader(new File(testFile)));
		
		String line;
		while ((line = r.readLine()) != null) {
			content.append(line);
			content.append("\n");
		}
		
		r.close();
		
		String cls = foo.classify(content.toString());
		System.out.println("Class is: " + cls);
		
		
		
			
	}

}
