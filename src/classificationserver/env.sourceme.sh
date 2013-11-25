CLASSPATH=$CLASSPATH:bin/
for i in lib/*jar; do CLASSPATH=$CLASSPATH:$i; done
for i in lib/jetty-distribution-7.6.10.v20130312/lib/*jar; do CLASSPATH=$CLASSPATH:$i; done
for i in lib/httpcomponents-client-4.3-beta1/lib/*jar; do CLASSPATH=$CLASSPATH:$i; done
echo "CLASSPATH set!"

echo "Now run java -cp $CLASSPATH de.haas.classification.ServLet"
