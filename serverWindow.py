import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QHBoxLayout, QGroupBox, 
QLabel, QLineEdit, QPushButton, QVBoxLayout, QListWidget, QListWidgetItem)
from PyQt5.QtCore import QDateTime, Qt
import serverSocket

class ServerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.date = QDateTime.currentDateTime()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Server Chat')
        
        # 채팅창 부분
        gb = QGroupBox('Message')
        box = QVBoxLayout()

        label = QLabel('Receive Message')
        box.addWidget(label)

        self.rMsg = QListWidget()
        box.addWidget(self.rMsg)

        label = QLabel('Send Message')
        box.addWidget(label)

        self.sMsg = QLineEdit()
        box.addWidget(self.sMsg)
        
        self.sBtn = QPushButton('Send')
        self.sBtn.clicked.connect(self.sendMessage)
        box.addWidget(self.sBtn)

        gb.setLayout(box)

        self.setLayout(box)
        self.show()

        self.s = serverSocket.ServerSocket(self)

    def updateMessage(self, msg, isSender):
        if isSender:
            self.rMsg.addItem(QListWidgetItem("send : "+msg))
        else:
            self.rMsg.addItem(QListWidgetItem("receive : "+msg))
 
        self.rMsg.setCurrentRow(self.rMsg.count()-1)

    def sendMessage(self):
        sMsg = self.sMsg.text()
        self.updateMessage(sMsg, True)
        self.s.send(sMsg)
        self.sMsg.clear()

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ServerWindow()
    sys.exit(app.exec_())