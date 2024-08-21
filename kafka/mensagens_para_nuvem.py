from kafka import KafkaConsumer
import ssl
from paho import mqtt
import paho.mqtt.client as paho
import paho.mqtt.publish as publish


consumer = KafkaConsumer(
    "words",
    bootstrap_servers="localhost:29092",
    value_deserializer=lambda x: x.decode("utf-8")
)
for msg in consumer:
    
 

        # create a set of 2 test messages that will be published at the same time
        msgs = [{'topic': "paho/test/multiple", 'payload': str(msg)}]

        # use TLS for secure connection with HiveMQ Cloud
        sslSettings = ssl.create_default_context()

        # put in your cluster credentials and hostname
        auth = {'username': "aaaaa", 'password': "Aa123456"}
        publish.multiple(msgs, hostname="b5b85536bc1e42009bf45c3e2997d02d.s2.eu.hivemq.cloud", port=8883, auth=auth,
                         tls=sslSettings, protocol=paho.MQTTv31)


