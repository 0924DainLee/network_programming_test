import cv2
import socket
import threading
import tkinter as tk
from ui import VideoChatUI

class VideoChatServer:
    def __init__(self):
        # VideoChatUI 인스턴스 초기화
        self.ui = VideoChatUI(tk.Tk(), "라이브스트리밍 서버")
        self.ui.on_send_message = self.send_message_to_clients
        self.clients = []

        # 웹캠 설정
        self.cap = cv2.VideoCapture(0)

        # 소켓 생성
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 8080))  # 서버는 1024 포트를 사용
        self.server_socket.listen(5)

        # 영상 전송 스레드 시작
        self.webcam_thread = threading.Thread(target=self.send_webcam)
        self.webcam_thread.daemon = True
        self.webcam_thread.start()

        # 클라이언트 연결을 처리하는 스레드 시작
        self.receive_thread = threading.Thread(target=self.receive_clients)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        # 서버 GUI 시작
        tk.mainloop()

    def show_frame(self, frame):
        self.ui.show_frame(frame)

   # 서버에서 메시지 전송
    def send_message_to_clients(self, message):
        for client in self.clients:
            client.send(message.encode())
        self.ui.receive_message("서버: " + message)

    # 서버에 영상 전송
    def send_webcam(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue
            # BGR에서 RGB로 변환
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encoded_frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
            encoded_frame = encoded_frame[1].tobytes()
            for client in self.clients:
                try:
                    client.send(encoded_frame)
                except:
                    self.clients.remove(client)
            self.show_frame(frame)

    def receive_clients(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f"New client connected: {client_address}")

            # 클라이언트로 메시지 수신
            while True:
                try:
                    message = client_socket.recv(8080).decode()
                    if not message:
                        break
                    print(f"Received message from {client_address}: {message}")
                    self.send_message_to_clients(message)  # 모든 클라이언트에게 메시지 전송
                except:
                    pass

if __name__ == "__main__":
    server = VideoChatServer()
