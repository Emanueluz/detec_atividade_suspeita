import paho.mqtt.client as mqtt

# Configurar o cliente MQTT
client = mqtt.Client()
client.connect("b5b85536bc1e42009bf45c3e2997d02d.s2.eu.hivemq.cloud", 8883)   
# Definir as mensagens e tópicos
messages = [
    ("/", "Mensagem para o tópico 1"),
   
]

# Publicar as mensagens em tópicos diferentes
for topic, message in messages:
    client.publish(topic, message)

# Encerrar a conexão
client.disconnect()
