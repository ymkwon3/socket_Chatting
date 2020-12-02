from socket import *
from PyQt5.QtCore import pyqtSignal, QObject
import threading
import time

class Signal(QObject):
    recv_signal = pyqtSignal(str, bool)

class ServerSocket:
    def __init__(self, parent):
        self.port = 8080
        self.bListen = True
        self.parent = parent
        self.clients = []
        self.addr = []

        self.recv = Signal()
        self.recv.recv_signal.connect(self.parent.updateMessage)
        self.serverSock = socket(AF_INET, SOCK_STREAM)
        self.serverSock.bind(('', self.port))

        t= threading.Thread(target=self.listen)
        t.start()
        
    # 사용자 접속 대기
    def listen(self):
        while self.bListen:
            print("listen...")
            self.serverSock.listen(5)
            self.connectionSock, self.addr = self.serverSock.accept()
            print(self.addr, "접속")
            t = threading.Thread(target=self.receive)
            t.start()

    # 메시지 전송
    def send(self, sendData):
        self.connectionSock.send(sendData.encode('utf-8'))

    # 메시지 수신
    def receive(self):
        while True:
            recvData = self.connectionSock.recv(1024)
            self.recv.recv_signal.emit(recvData.decode('utf-8'), False)
            time.sleep(0.1)