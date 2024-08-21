import cv2
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


producer = KafkaProducer(
    bootstrap_servers="localhost:29092",
    value_serializer=lambda x: x.encode("utf-8")
)

model_name='best.pt'
diretorio=""
model = torch.hub.load(diretorio, 'custom', source='local', path = model_name, force_reload = True)

cap = cv2.VideoCapture(0)
cap.set(3, 480)
cap.set(4, 480)

while True:
    ret, image= cap.read()
    start=time()
    results= model(image)
    predictions = results.pandas().xyxy[0]

    # Fazer algo com as previsões, como desenhar caixas delimitadoras nos objetos detectados
    for _,prediction in predictions.iterrows():

        #print(prediction)  
        x_min, y_min, x_max, y_max, confidence, class_id, name = prediction
        class_name = model.names[int(class_id)]
        if confidence> 0.8:
            # Desenhar a caixa delimitadora e o rótulo do objeto
            cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
            cv2.putText(image, f'{class_name}: {confidence:.2f}', (int(x_min), int(y_min) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


            aux=str(confidence)
            #MENSAGEM PARA O KAFKA 
            future = producer.send("words", value=str(name)+"--"+aux+"--"+str(datetime.now()))

        # Exibir a imagem com as caixas delimitadoras e rótulos desenhados
    '''  cv2.imshow('Detecção de Objetos YOLOv5', image)
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
    '''
    

    end=time()
 
# Aguardar até que uma tecla seja pressionada e fechar a janela

 

cap.release()
cv2.destroyAllWindows()