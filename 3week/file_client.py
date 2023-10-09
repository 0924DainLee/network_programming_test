import socket

s_sock = socket.socket()
host = "localhost"
port = 2500

s_sock.connect((host,port))
s_sock.send("I am ready".encode())

fn = s_sock.recv(1024).decode()## 받았지만 차이를 위해 새로 지정

with open("./dummy/"+"recv",'wb') as f:
    print("receiving")
    while True:
        data = s_sock.recv(8192)
        if not data:
            break
        f.write(data)

print("download complete")
s_sock.close()
