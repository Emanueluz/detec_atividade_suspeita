import datetime
from flask import Flask, Response
from kafka import KafkaConsumer
from threading import Timer

# Fire up the Kafka Consumer
topic = "distributed-video1"

consumer = KafkaConsumer(
    topic, 
    bootstrap_servers=['localhost:29092'])


# Set the consumer in a Flask App
app = Flask(__name__)
message_count = 0
start_time = datetime.datetime.now()
@app.route('/video', methods=['GET'])
# Variáveis globais para contagem de mensagens


def video():
    """
    This is the heart of our video display. Notice we set the mimetype to 
    multipart/x-mixed-replace. This tells Flask to replace any old images with 
    new values streaming through the pipeline.
    """
    return Response(
        get_video_stream(), 
        mimetype='multipart/x-mixed-replace; boundary=frame')

def get_video_stream():
    """
    Here is where we recieve streamed images from the Kafka Server and convert 
    them to a Flask-readable format.
    """
    global message_count
    for msg in consumer:
        message_count += 1
        yield (b'--frame\r\n'
              b'Content-Type: image/jpg\r\n\r\n' + msg.value + b'\r\n\r\n')
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)