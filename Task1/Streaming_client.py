import socket
import cv2
import threading
from ui import VideoChatUI
import tkinter as tk

class VideoChatClient:
    def __init__(self):
        self.ui = VideoChatUI(tk.Tk(), "라이브스트리밍 클라이언트")
        self.ui.on_send_message = self.send_message_to_server

        # 주소 및 포트
        self.server_address = ('localhost', 8080)

        # 가로 X 세로 해상도
        width = 640
        height = 480

        # 소켓 서버와 연결
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)

        # 웹캠 초기화
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)  # 가로 해상도 설정
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  # 세로 해상도 설정

        # 웹캠 스레드
        self.show_frame_thread = threading.Thread(target=self.show_frame)
        self.show_frame_thread.daemon = True
        self.show_frame_thread.start()

        # 메시지 수신 스레드
        self.receive_thread = threading.Thread(target=self.receive_message)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        # 클라이언트 GUI 시작
        tk.mainloop()

    def show_frame(self):
        while True:
            # 웹캠 서버로 전송
            ret, frame = self.cap.read()
            if not ret:
                continue

            # BGR에서 RGB로 변환
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            _, encoded_frame = cv2.imencode('.jpg', frame_rgb, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
            encoded_frame = encoded_frame.tobytes()

            self.client_socket.send(encoded_frame)
            self.ui.show_frame(frame_rgb)

    def send_message_to_server(self, message):
        self.client_socket.send(message.encode())
    # 메시지 수신
    def receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break
                self.ui.receive_message("클라이언트: " + message)
            except:
                pass

if __name__ == "__main__":
    client = VideoChatClient()