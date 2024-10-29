import sys
import time
import cv2
from kafka import KafkaProducer

topic = "distributed-video1"

def add_frame_number(frame, frame_number):
 
    # Definir o texto com o número do frame
    text = f"Frame: {frame_number}"
    
    # Definir a posição do texto (x, y)
    position = (10, 30)  # Posição no canto superior esquerdo
    
    # Definir a fonte, escala, cor e espessura do texto
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (0, 255, 0)  # Verde
    thickness = 2
 
    cv2.putText(frame, text, position, font, font_scale, color, thickness, cv2.LINE_AA)
    
    return frame


def publish_video(video_file):
    """
    Publish given video file to a specified Kafka topic. 
    Kafka Server is expected to be running on the localhost. Not partitioned.
    
    :param video_file: path to video file <string>
    """
    # Start up producer
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    # Open file654321
    video = cv2.VideoCapture(video_file)
    print('publishing video...')

    while(video.isOpened()):
        
        success, frame = video.read()
       

        # Ensure file was read successfully
        if not success:
            print("bad read!")
            break
        
        # Convert image to png
        ret, buffer = cv2.imencode('.jpg', frame)

        # Convert to bytes and send to kafka
        producer.send(topic, buffer.tobytes())

        #time.sleep(0.2)
    video.release()
    print('publish complete')

    
def publish_camera():
    """
    Publish camera video stream to specified Kafka topic.
    Kafka Server is expected to be running on the localhost. Not partitioned.
    """

    # Start up producer
    producer = KafkaProducer(bootstrap_servers='localhost:29092')

    
    camera = cv2.VideoCapture(0)
    frame_number=0

    try:
        while(True):
            success, frame = camera.read()
            frame_number=frame_number+1
            frame=add_frame_number(frame, frame_number)
            ret, buffer = cv2.imencode('.jpg', frame)
            producer.send(topic, buffer.tobytes())
            
            # Choppier stream, reduced load on processor
            #time.sleep(0.2)

    except:
        print("\nExiting.")
        sys.exit(1)

    
    camera.release()


if __name__ == '__main__':
    """
    Producer will publish to Kafka Server a video file given as a system arg. 
    Otherwise it will default by streaming webcam feed.
    """
    if(len(sys.argv) > 1):
        video_path = sys.argv[1]
        publish_video(video_path)
    else:
        print("publishing feed!")
        publish_camera()