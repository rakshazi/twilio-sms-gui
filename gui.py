#!/usr/bin/env python3
from yaml import load, SafeLoader
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from twilio.rest import Client

class TwilioGui(QWidget):
    def __init__(self):
        super().__init__()
        self.config = self.loadConfig('config.yml')
        self.to = []
        self.initUI()

    def log(self, msg):
        print(msg)
        self._log.setText(msg)

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
            self.log(item.text() + ' removed')
        else:
            self.to.append(self.config['contacts'][item.text()])
            self.log(item.text() + ' selected')

    def onBtnClick(self):
        self.button.setEnabled(False)
        for number in self.to:
            self.sendSMS(number, self.text.toPlainText())
        self.button.setEnabled(True)

    def onToggleAll(self, event):
        self.log('Toggle All clicked')
        for index in range(self.contactListModel.rowCount()):
            item = self.contactListModel.item(index)
            if item.isCheckable() == False:
                continue
            if item.checkState() == Qt.Unchecked:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)

    def initUI(self):
        layout = QGridLayout(self)

        # Toggle label
        selectLabel = QLabel('Toggle All', self)
        selectLabel.mousePressEvent = self.onToggleAll
        layout.addWidget(selectLabel, 0,0)

        # SMS label
        layout.addWidget(QLabel('Your text goes here', self), 0, 1)

        # Contact list
        list = QListView(self)
        self.contactListModel = QStandardItemModel(list)
        self.contactListModel.itemChanged.connect(self.onItemChanged)
        for contact in self.config['contacts']:
            item = QStandardItem(contact)
            item.setCheckable(True)
            item.setEditable(False)
            self.contactListModel.appendRow(item)
        list.setModel(self.contactListModel)
        layout.addWidget(list, 1, 0)

        # SMS text
        self.text = QPlainTextEdit(self)
        layout.addWidget(self.text, 1, 1)

        # Log
        self._log = QLabel('UI loaded')
        layout.addWidget(self._log, 2, 0)

        # Button
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
