#!/usr/bin/perl

use strict;
use threads;
use Thread::Queue;
use AnyEvent::Twitter::Stream;
use Data::Dumper;
use Tree::Trie;
use Text::CSV;
use IPC::Open2;

sub worker {
    my $tid = threads->tid;
	## startup external resources
	my $csv = Text::CSV->new({binary=>1,sep_char=>"\t"}) or die;
	my $trie = Tree::Trie->new;

	foreach my $file (<data/GermanPolarityClues-2012/GermanPolarityClues-*-Lemma-21042012.tsv>) {
		open my $io, "<", $file or die;
		while (my $row = $csv->getline($io)) {
			my @fields = @$row;
			my $lemma = lc $fields[1];
			my $tag = $fields[2];
			my $sentiment = $fields[3];
			$trie->add_data($lemma=>{tag=>$tag,sentiment=>$sentiment});
		}
		close $io;
	}

	open SMILE, "<", "data/smileys";
	my $smileys = undef;
	while(<SMILE>) {
		chomp;
		my ($smiley,$emo) = split("\t",$_);
		$smileys->{$smiley} = $emo;
	}
	close SMILE;
	my $pid = open2 my $out, my $in, "/usr/bin/java -classpath \$CLASSPATH:libs/ark-tweet-nlp-0.3.2.jar:javabin/ SentimentTagger";
	die "$0: open2: $!" unless defined $pid;
	
	print "started\n";
    my( $Qwork, $Qresults ) = @_;
    while( my $work = $Qwork->dequeue ) {
        print $in $work; ## send tweet to tagger
		my $total = 0;
	    my $counts = undef;
    	$counts->{'E'}->{'neutral'} = 0;
    	$counts->{'E'}->{'negativ'} = 0;
    	$counts->{'E'}->{'positiv'} = 0;
    	$counts->{'W'}->{'neutral'} = 0;
    	$counts->{'W'}->{'negativ'} = 0;
	    $counts->{'W'}->{'positiv'} = 0;
    	my $score = 0;
    	my @taggedSequence = ();

		while (<$out>) {
			chomp; ## delete newline
			my ($word,$tag) = split("\t",$_);
			unless($tag) {
				my $jsonHash = undef;
				$jsonHash->{tweet} = \@taggedSequence;
				$jsonHash->{tokens} = $total;
				$jsonHash->{pos_tokens}=$counts->{'W'}->{'positiv'};
				$jsonHash->{neg_tokens}=$counts->{'W'}->{'negativ'};
				$jsonHash->{neutral_tokens}=$counts->{'W'}->{'neutral'};
				$jsonHash->{pos_smileys}=$counts->{'E'}->{'positiv'};
				$jsonHash->{neg_smileys}=$counts->{'E'}->{'negativ'};
				$jsonHash->{neutral_smileys}=$counts->{'E'}->{'neutral'};
				$jsonHash->{overall_sentiment_score}=$score;
        		$jsonHash->{normalized_sentiment_score}=$score / $total;
				$Qresults->enqueue($jsonHash);
				last;
			}
			$word = lc $word;
			if ($tag eq "W") {
				my $counter = 0;
				my @x = $trie->lookup_data($word);
				my $sentiment = "neutral";
				while(@x) {
					my $item = shift @x;
					if ($counter%2==0) {
						if ($item eq $word) {
							my $hash = shift @x;
							$sentiment = $hash->{'sentiment'};
							last;
							$counter++;
						}
					}
					$counter++;
				}
				if ($sentiment =~ /neu/) {
					$counts->{'W'}->{'neutral'}++;
				} elsif ($sentiment =~ /pos/) {
					$counts->{'W'}->{'positiv'}++;
					$score++;
				} elsif($sentiment =~/neg/) {
					$counts->{'W'}->{'negativ'}++;
					$score--;
		        }
				push(@taggedSequence,$word."\t".$tag."\t".$sentiment);
			} elsif($tag eq "E") {
				my $sentiment = "neutral";
				if ($smileys->{$word}) {
					$sentiment=$smileys->{$word};
				}
				if ($sentiment =~ /neu/) {
					$counts->{'E'}->{'neutral'}++;	
				} elsif ($sentiment =~ /pos/) {
					$counts->{'E'}->{'positiv'}++;
					$score++;
				} elsif($sentiment =~/neg/) {
					$counts->{'E'}->{'negativ'}++;
					$score--;
				}

				push(@taggedSequence,$word."\t".$tag."\t".$sentiment);
			}
			$total++;
		}
    }
    $Qresults->enqueue( undef );
}




our $THREADS = 3;
my $Qwork = new Thread::Queue;
my $Qresults = new Thread::Queue;


my @pool = map{threads->create( \&worker, $Qwork, $Qresults )} 1 .. $THREADS;

my $done = AE::cv;

my $listener = AnyEvent::Twitter::Stream->new(
	username => '',
	password => '',
	method => "filter",
	track => "#Frauenquote, #boston",
	on_tweet => sub {
		my $tweet = shift;
		
		print "GOT TWEEEEEET!!! OMFG\n";
		$Qwork->enqueue($tweet->{'text'}."\n");
		my $result = $Qresults->dequeue;
		print Dumper $result;
		### classification comes here
	},
);
$done->recv;

## Clean up the threads
#$_->join for @pool;
