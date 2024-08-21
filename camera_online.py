import cv2
 
# Variáveis de configuração
usuario = "admin"
senha = "Aluno@00"
ip = "172.19.0.11"  # Substitua pelo IP do seu DVR
porta = "554"  # Porta RTSP padrão

# URL da câmera utilizando as variáveis
url_camera = f"rtsp://{usuario}:{senha}@{ip}:{porta}/ch1/main/av_stream"
print(url_camera)
# Abertura da stream da câmera
cap = cv2.VideoCapture(f"rtsp://{usuario}:{senha}@{ip}:{porta}/Streaming/Channels/101?timeout=10000")

if not cap.isOpened():
    print("Erro ao acessar a câmera.")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao receber o quadro.")
            break
        
        cv2.imshow("Câmera Hikvision", frame)
        
        # Saia do loop ao pressionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
