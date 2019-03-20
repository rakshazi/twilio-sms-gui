#!/usr/bin/env python3
from yaml import load, SafeLoader
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from twilio.rest import Client

class TwilioGui(QWidget):
    def __init__(self):
        super().__init__()
        self.config = self.loadConfig('config.yml')
        self.to = []
        self.initUI()

    def log(self, msg):
        print(msg)

    def loadConfig(self, filename):
        return load(open(filename, 'r'), Loader=SafeLoader)

    def sendSMS(self, to, body):
        client = Client(self.config['api']['accountsid'], self.config['api']['authtoken'])
        message = client.messages.create(to=to, from_=self.config['api']['callerid'],body=body)
        self.log(to + ' - ' + message.sid)

    # When contact checked
    def onItemChanged(self, item):
        if not item.checkState():
            self.to.remove(self.config['contacts'][item.text()])
        self.to.append(self.config['contacts'][item.text()])

    def onBtnClick(self):
        self.button.setEnabled(False)
        for number in self.to:
            self.sendSMS(number, self.text.toPlainText())

    def initUI(self):
        layout = QGridLayout(self)

        # Contact list
        list = QListView(self)
        model = QStandardItemModel(list)
        model.itemChanged.connect(self.onItemChanged)
        for contact in self.config['contacts']:
            item = QStandardItem(contact)
            item.setCheckable(True)
            item.setEditable(False)
            model.appendRow(item)
        list.setModel(model)
        layout.addWidget(list, 1, 0)

        # SMS text
        self.text = QPlainTextEdit(self)
        layout.addWidget(self.text, 1, 1)
        self.button = QPushButton('Send')
        self.button.clicked.connect(self.onBtnClick)
        layout.addWidget(self.button, 2, 1)

        # Geometry
        self.setLayout(layout)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setWindowTitle("Twilio SMS GUI - rakshazi.me")
        self.show()


app = QApplication([])
app.setStyle('Fusion')
window = TwilioGui()
app.exec_()
