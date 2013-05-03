#!/bin/bash

echo "Starting Perl taggerserver"
cd ../taggerserver
perl server.pl &
echo "Perl taggerserver started"

echo "Starting Java classificationserver"
cd ../classificationserver 
source env.sourceme.sh
java -cp $CLASSPATH de.haas.classification.ServLet &
unset CLASSPATH
echo "Java classificationserver started."


echo "Starting Python mainserver"

cd ../mainserver
source env.sourceme.sh
source ../featureextraction/env.sourceme.sh
python main.py &
unset PYTHONPATH
echo "Python mainserver started"


