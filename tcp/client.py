import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("localhost", 5700)
sock.connect(address)
while True:
    time.sleep(1)
    print("현재 시각: ", sock.recv(1024).decode())
