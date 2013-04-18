
import java.io.File;
import java.io.FilenameFilter;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.FileWriter;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import cmu.arktweetnlp.impl.Model;
import cmu.arktweetnlp.impl.ModelSentence;
import cmu.arktweetnlp.impl.Sentence;
import cmu.arktweetnlp.impl.features.FeatureExtractor;
import cmu.arktweetnlp.Twokenize;

public class SentimentTagger {
	public Model model;
	public FeatureExtractor featureExtractor;

	/**
	 * Loads a model from a file.  The tagger should be ready to tag after calling this.
	 * 
	 * @param modelFilename
	 * @throws IOException
	 */
	public void loadModel(String modelFilename) throws IOException {
		model = Model.loadModelFromText(modelFilename);
		featureExtractor = new FeatureExtractor(model, false);
	}

	/**
	 * One token and its tag.
	 **/
	public static class TaggedToken {
		public String token;
		public String tag;
	}


	/**
	 * Run the tokenizer and tagger on one tweet's text.
	 **/
	public List<TaggedToken> tokenizeAndTag(String text) {
		if (model == null) throw new RuntimeException("Must loadModel() first before tagging anything");
		List<String> tokens = Twokenize.tokenizeRawTweetText(text);

		Sentence sentence = new Sentence();
		sentence.tokens = tokens;
		ModelSentence ms = new ModelSentence(sentence.T());
		featureExtractor.computeFeatures(sentence, ms);
		model.greedyDecode(ms, false);

		ArrayList<TaggedToken> taggedTokens = new ArrayList<TaggedToken>();

		for (int t=0; t < sentence.T(); t++) {
			TaggedToken tt = new TaggedToken();
			tt.token = tokens.get(t);
			tt.tag = model.labelVocab.name( ms.labels[t] );
			taggedTokens.add(tt);
		}

		return taggedTokens;
	}


	public static void main(String[] args) throws IOException {
		String modelFilename = "data/model.20120919";

		SentimentTagger tagger = new SentimentTagger();
		tagger.loadModel(modelFilename);
		BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
		String s;
		while ((s = in.readLine()) != null && s.length() != 0) {
			List<TaggedToken> taggedTokens = tagger.tokenizeAndTag(s);
			for (TaggedToken token : taggedTokens) {
				String tag = token.tag;
				String tok = token.token;
				if(tag.equals("E")) {
					System.out.print(tok+"\tE\n");
				} else {
					System.out.print(tok+"\tW\n");
				}
			}
			System.out.println("END");
		}


	}



}
