import socket
import win32gui
import re
import time

# 서버의 주소입니다. hostname 또는 ip address를 사용할 수 있습니다.
HOST = '172.28.113.191'
# 서버에서 지정해 놓은 포트 번호입니다.
PORT = 5000

# 소켓 객체를 생성합니다.
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 지정한 HOST와 PORT를 사용하여 서버에 접속합니다.
client_socket.connect((HOST, PORT))

# 메시지를 전송합니다.
window = ''
while True:
    current_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    if window != current_window:
        window = current_window
        client_socket.sendall(window.encode())
    time.sleep(1)