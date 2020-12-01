from socket import *
from PyQt5.QtCore import pyqtSignal, QObject
import threading
import time

class Signal(QObject):
    recv_signal = pyqtSignal(str, bool)

class ClientSocket:
    def __init__(self, parent):
        self.ip = ''
        self.port = 8080
        self.parent = parent
        self.recv = Signal()
        self.recv.recv_signal.connect(self.parent.updateMessage)
        self.clientSock = socket(AF_INET, SOCK_STREAM)
        self.clientSock.connect((self.ip, self.port))
        t = threading.Thread(target=self.receive)
        t.start()

    def send(self, sendData):
        self.clientSock.send(sendData.encode('utf-8'))

    def receive(self):
        while True:
            recvData = self.clientSock.recv(1024)
            self.recv.recv_signal.emit(recvData.decode('utf-8'), False)
            time.sleep(0.1)