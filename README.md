#Implantação do ambiente de serviços de Visão computacional (Kafka, MQTT, Câmeras)





O ambiente de visão computacional se baseia no uso de IA para processar os frames das filmagens de câmeras de segurança e gerar mensagens para um servidor Kafka local(KAFKA BROKER) quando alguma atividade de interesse é identificada. O papel do servidor local é acumular as mensagens geradas pelas câmeras de segurança de um local só e depois encaminhar as mesmas para uma nuvem HIVEMQ que distribui as mensagens para os interessados finais das mesmas. 

seguindo a lógica do fluxograma a seguir 







A primeira parte do trabalho vai da captura até o envio ou não das mensagens para o servidor local de acordo com a avaliação das imagens pela nossa IA. Então os passos para conseguirmos executar nosso programa é levantar o servidor local, que fazemos executando :
sudo docker-compose up

Sem o KAFKA BROKER ativo, nosso programa de detecção não tem como ser executado, já que ele não tem um endereço para mandar as mensagens de detecção.

Posteriormente, já podemos executar o programa de detecção das imagens e verificar com o serviço de mensagens local se está tudo funcionando perfeitamente. O programa para verificar se está sendo produzido mensagens até o servidor local se encontra no diretório src e se chama consumer.py.

Para levantar nosso Cluster  MQTT na nuvem primeiramente usamos um navegador para ir até o site https://console.hivemq.cloud/  onde vamos abrir um cluster e pegar as informações presentes no mesmo, além de dar acesso aos usuários do nosso cluster. Ao final, vamos ter uma tela como o print a seguir.




Com o Cluster funcionando, podemos acionar nosso script que alimenta o mesmo com as mensagens do kafka local, que é o consumer_to_MQTT.py, que se encontra também na pasta src/kafka. Assim podemos, por fim verificar com o programa inscri_na_nuvem.py no diretorio src/MQTT se as mensagens estão sendo repassadas da nuvem. 

Ao todo, temos a seguinte execução dos seguintes comandos para criarmos o ambiente de comunicação entre uma câmera e a nuvem:

sudo docker-compose up  # levantar o servidor kafka
 
rede_com_webcan.py # analizar as imagens e alimentar o servidor kafka

src/kafka/consumer_to_MQTT.py # levar as mensagens do servidor kafka local para a nuvem MQTT




##Parte em relação às câmeras de segurança. 

https://www.hikvisioneurope.com/eu/portal/portal/Technical%20Materials/00%20%20Network%20Camera/02%20%20Product%20User%20Manuals%20%28multi-language%29/99-OldUserManuals/13-Portuguese/UD04470B_Baseline_User%20Manual%20of%20Network%20Camera_V5.4.5_20170123_PT.pdf

Depois de colocar um HD dentro do nvr hikvision e conectar as câmeras e um monitor  no mesmo, conseguimos fazer o login no nvr usando um mouse que vem junto com o kit.
Na maior parte do processo das câmeras, as configurações ficam com o modelo padrão e o cadastro do Administrador ficou como:
usuário: admin
senha: Aluno@00
Tivemos algumas dificuldades com a compatibilidade dos equipamentos com sistemas operacionais baseados em linux, já que o software que ativa o sistema no nvr e permite com que as câmeras fiquem online.

É necessário colocar senha e usuário em cada câmera para poder deixá-las online e acessá-las remotamente, o que conseguimos fazer com o celular, como mostra as imagens a seguir do aplicativo Hik-Connect

 
 Mas tivemos dificuldade de conseguir acessar o RTSP, para conseguir utilizar as câmeras remotamente. 


Como deve ser feita a aquisição das imagens no ambiente:

A aquisição das imagens deve ser realizada através do protocolo RTSP (Real Time Streaming Protocol). O RTSP é um protocolo de rede que permite a transmissão de dados de vídeo em tempo real, proporcionando uma maneira eficaz de acessar e gerenciar fluxos de vídeo ao vivo de câmeras de segurança e outros dispositivos de captura de vídeo.

No arquivo `rede_com_webcam.py`, implementamos a funcionalidade necessária para conectar-se ao fluxo RTSP da câmera de segurança associada ao contêiner. Esse arquivo contém um bloco de código específico que realiza a seguinte operação:

1. **Conexão ao Stream RTSP** :  O código utiliza a biblioteca `opencv-python` para estabelecer uma conexão com o stream RTSP da câmera. A URL do stream RTSP é configurada com as credenciais necessárias : Nome do usuário, senha, endereço IP e porta do protocolo.

2. **Início da Captura de Vídeo** : Após estabelecer a conexão, o código inicia a captura do vídeo ao vivo. O fluxo de vídeo é lido em tempo real e processado conforme as necessidades do sistema. Isso pode incluir a visualização ao vivo das imagens se necessário.

3. **Leitura e Processamento dos Frames**: O código continua a ler os frames do fluxo RTSP continuamente. Cada frame capturado pode ser processado pela rede YOLO de acordo com a aplicação.

4 **Criação das mensagens**: Se algum frame conter alguma atividade detectada pela rede, é ativada a função de enviar uma mensagem para o servidor local com os dados da captura.
 

 

 



Como deve ser feita a aquisição e envio de Mensagens no MQTT, dependendo do tipo de serviço: 

O serviço do MQTT funciona a partir de 3 partes básicas: 	
Broker: O servidor central que gerencia as mensagens entre publicadores e assinantes.
Publisher: Envia mensagens para um tópico específico.
Subscriber: Recebe mensagens de um tópico específico.

Um Publisher tem quer ter uma serie de dados de identificação, sendo eles a URL do broker, a porta referente ao serviço, o topíco de envio da mensagem, o identificador do cliente, além do usuário e senha do MQTT para conseguir mandar as mensagens. A seguir temos um exemplo da parte do código com os dados usados nos nossos testes.

broker = 'b5b85536bc1e42009bf45c3e2997d02d.s2.eu.hivemq.cloud'
port = 8883
topic = "encyclopedia/temperature"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = -------
password = -------

No nosso programa, o servidor local Kafka já é um Publisher do MQTT que manda para o Broker online e manda para todos os Subscriber as mensagens de interesse.
No caso do publisher, ele é responsável por enviar mensagens para um tópico específico. A estrutura da mensagem que ele envia geralmente inclui:
Tópico: O caminho hierárquico que categoriza a mensagem.
Payload: O conteúdo real da mensagem (os dados que você está enviando).
QoS (Qualidade de Serviço): Define o nível de garantia de entrega.
Retain Flag: Indica se o broker deve armazenar a última mensagem enviada para o tópico.
Nosso ambiente foi pensando para que os tópicos das mensagens fosse caracterizado da urgência/hierarquia da mesma, enquanto o Payload seria a parte da mensagens que teria todo o seu conteúdo, isto é, nível da predição que a rede identificou, posição do Bounding box e atividade/objeto identificado. O QoS e o Retain Flag ficam como opção da aplicação que se deseja executar.
 No caso de um Subscriber, também tem a parte temos que identificar que temos acesso às mensagens que serão recebidas pelo broker. A seguir tem outro exemplo de identificação.

auth = {'username': "-------", 'password': "----------"}
subscribe.callback(print_msg, "#", hostname="b5b85536bc1e42009bf45c3e2997d02d.s2.eu.hivemq.cloud", port=8883, auth=auth,
               	tls=sslSettings, protocol=paho.MQTTv31)




Serviço de contagem de pessoas que estão em um ambiente:

