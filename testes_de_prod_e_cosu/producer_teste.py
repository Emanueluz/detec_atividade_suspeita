from kafka import KafkaProducer
import time

def delivery_report(err, msg):
    """ Callback chamado após cada mensagem enviada """
    if err is not None:
        print(f"Erro ao entregar mensagem: {err}")
    else:
        print(f"Mensagem entregue: {msg.topic} [{msg.partition}]")

def kafka_producer_test(broker, topic, num_messages):
    # Configuração do produtor
    producer = KafkaProducer(bootstrap_servers=broker, value_serializer=lambda v: v.encode('utf-8'))

    print(f"Iniciando envio de {num_messages} mensagens para o tópico '{topic}'...")
    start_time = time.time()

    for i in range(num_messages):
        message = f"Mensagem {i+1}"
        producer.send(topic, value=message)

        # Para evitar sobrecarregar, descomente para adicionar um atraso entre as mensagens
        # time.sleep(0.01)

        # Checa as mensagens pendentes para envio
        if i % 100 == 0:
            producer.flush()

    producer.flush()
    elapsed_time = time.time() - start_time
    print(f"Enviadas {num_messages} mensagens em {elapsed_time:.2f} segundos.")

if __name__ == "__main__":
    BROKER = "localhost:29092"
    TOPIC = "test-topic"
    NUM_MESSAGES = 100000  # Quantidade de mensagens a enviar

    kafka_producer_test(BROKER, TOPIC, NUM_MESSAGES)
