from socket import *
from PyQt5.QtCore import pyqtSignal, QObject
import threading
import time

class Signal(QObject):
    recv_signal = pyqtSignal(str, bool)

class ServerSocket:
    def __init__(self, parent):
        self.port = 8080
        self.parent = parent
        self.recv = Signal()
        self.recv.recv_signal.connect(self.parent.updateMessage)
        self.serverSock = socket(AF_INET, SOCK_STREAM)
        self.serverSock.bind(('', self.port))
        self.serverSock.listen(1)
        self.connectionSock, self.addr = self.serverSock.accept()
        t = threading.Thread(target=self.receive)
        t.start()
        print(self.addr, "접속")
        
    def listen(self):
        self.serverSock.listen(1)
        self.connectionSock, self.addr = self.serverSock.accept()
        return self.addr

    def send(self, sendData):
        self.connectionSock.send(sendData.encode('utf-8'))

    def receive(self):
        while True:
            recvData = self.connectionSock.recv(1024)
            self.recv.recv_signal.emit(recvData.decode('utf-8'), False)
            time.sleep(0.1)