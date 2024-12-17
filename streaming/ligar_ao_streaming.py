import cv2
from urllib.request import urlopen
import torch
import os
import numpy as np
from mss import mss
from PIL import Image
from time import time 
import sys
from time import sleep
from kafka import KafkaProducer
from datetime import datetime
from ultralytics import YOLO
import pandas as pd
def display_stream_urllib(url,model):
    """
    Captura continuamente o vídeo do endpoint usando urllib.
    """
    stream = urlopen(url)
    bytes_data = b""
    try:
        while True:
            chunk = stream.read(4096)
            if not chunk:
                break
            bytes_data += chunk

            start = bytes_data.find(b'\xff\xd8')
            end = bytes_data.find(b'\xff\xd9')

            if start != -1 and end != -1:
                jpg_data = bytes_data[start:end + 2]
                bytes_data = bytes_data[end + 2:]

                frame = cv2.imdecode(np.frombuffer(jpg_data, dtype=np.uint8), cv2.IMREAD_COLOR)

                image=frame

                 
                results= model(image,conf=0.5)
                for result in results:
                    for box in result.boxes:
                        # Extrai as informações da predição
                        x_min, y_min, x_max, y_max = box.xyxy[0].cpu().numpy()  # Coordenadas da bounding box
                        confidence = float(box.conf.cpu().numpy())  # Confiança
                        class_id = int(box.cls.cpu().numpy())  # ID da classe
                        name = model.names[class_id]  # Nome da classe

                        # Exibe os resultados no terminal
                        #print(f"x_min: {x_min:.2f}, y_min: {y_min:.2f}, x_max: {x_max:.2f}, y_max: {y_max:.2f}, "
                         #     f"confidence: {confidence:.2f}, class_id: {class_id}, name: {name}")

                        # Desenha as caixas delimitadoras e o texto no frame
                        cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
                        label = f"{name} {confidence:.2f}"
                        cv2.putText(frame, label, (int(x_min), int(y_min) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                            #aux=str(confidence)
                            #MENSAGEM PARA O KAFKA 
                            #future = producer.send("words", value=str(name)+"--"+aux+"--"+str(datetime.now()))
                        
                if frame is not None:
                    cv2.imshow("Video Stream", frame)
                    #time.sleep(0.2)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
    except Exception as e:
        print(f"Erro ao processar o stream: {e}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":


    bounding_box = {'top': 0, 'left': 0, 'width': 1000, 'height': 1000}
    sct = mss()
    # Carregar o modelo YOLOv5 pré-treinado

    model_name='/home/emanuel/Documents/detec_atividade/yolov/runs/best.pt'
    diretorio="/home/emanuel/Documents/detec_atividade/yolov/"

    #model = torch.hub.load(diretorio, 'custom', source='local', path = model_name, force_reload = True)
    model = YOLO("yolov8m")

    stream_url = "http://0.0.0.0:5000/video"
    display_stream_urllib(stream_url,model)
