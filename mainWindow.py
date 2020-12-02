import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime, Qt
import serverSocket
import clientSocket

class ServerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.date = QDateTime.currentDateTime()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Server Chat')

        inputBox = QHBoxLayout()
        gb = QGroupBox('select type')
        inputBox.addWidget(gb)

        box = QHBoxLayout()

        self.cRoom = QPushButton('Create')
        self.cRoom.clicked.connect(self.createRoom)
        box.addWidget(self.cRoom)

        self.jRoom = QPushButton('Join')
        self.jRoom.clicked.connect(self.joinRoom)
        box.addWidget(self.jRoom)

        gb.setLayout(box)
        
        # 채팅창 부분

        chatBox = QVBoxLayout()
        gb = QGroupBox('Message')
        chatBox.addWidget(gb)

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

        vBox = QVBoxLayout()
        vBox.addLayout(inputBox)
        vBox.addLayout(chatBox)
        self.setLayout(vBox)
        self.show()

        
        # self.c = clientSocket.ClientSocket(self)

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

    def createRoom(self):
        self.s = serverSocket.ServerSocket(self)

    def joinRoom(self):
        pass

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ServerWindow()
    sys.exit(app.exec_())