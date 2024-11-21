from confluent_kafka import Consumer, KafkaError

def kafka_consumer_test(broker, topic, group_id):
    # Configuração do consumidor
    conf = {
        'bootstrap.servers': broker,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)
    consumer.subscribe([topic])

    print(f"Iniciando consumo de mensagens do tópico '{topic}'...")
    try:
        while True:
            msg = consumer.poll(1.0)  # Tempo máximo de espera (1 segundo)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print("Fim da partição alcançado.")
                else:
                    print(f"Erro no consumidor: {msg.error()}")
                continue

            print(f"Mensagem recebida: {msg.value().decode('utf-8')}")

    except KeyboardInterrupt:
        print("Consumo interrompido pelo usuário.")
    finally:
        consumer.close()

if __name__ == "__main__":
    BROKER = "localhost:29092"
    TOPIC = "test-topic"
    GROUP_ID = "test-group"

    kafka_consumer_test(BROKER, TOPIC, GROUP_ID)
