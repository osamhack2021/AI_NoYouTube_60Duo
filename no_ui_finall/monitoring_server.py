import socket
import threading
import time
from sentiment_predict import sentiment_predict

# 모든 아이피 접속 
host = "0.0.0.0"
port = 5000

#백그라운드에서 클라이언트가 보낸 메시지를 수신하기 위해 대기합니다. 
def handle_client(client_socket, addr):
    while True:
        time.sleep(1)
        data = client_socket.recv(1024)
        data = data.decode()
        study_data = sentiment_predict(data)
        print('Received from', addr, data)
        print(study_data)

def accept_func():
    global server_socket
    #IPv4 체계, TCP 타입 소켓 객체를 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #포트를 사용 중 일때 에러를 해결하기 위한 구문
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #ip주소와 port번호를 함께 socket에 바인드 한다.
    #포트의 범위는 1-65535 사이의 숫자를 사용할 수 있다.
    server_socket.bind((host, port))

    #서버가 최대 5개의 클라이언트의 접속을 허용한다.
    server_socket.listen(5)
    
    while 1:
        try:
            #클라이언트 함수가 접속하면 새로운 소켓을 반환한다.
            client_socket, addr = server_socket.accept()
        except KeyboardInterrupt:
            server_socket.close()
            print("Keyboard interrupt")
            
        print("접속한 클라이언트의 주소 입니다. : ", addr)
        time.sleep(1)

        print("클라이언트 핸들러 스레드로 이동 됩니다.")
        #accept()함수로 입력만 받아주고 이후 알고리즘은 핸들러에게 맡긴다.
        t = threading.Thread(target=handle_client, args=(client_socket, addr))
        t.daemon = True
        t.start()
        
accept_func()
 

