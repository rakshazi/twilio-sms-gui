from src import config, sms
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class UI(QWidget):
    def __init__(self):
        super().__init__()
        self._config = config.load()
        self.init()

    # When contact checked
    def onItemChanged(self, item):
        phone = self._config['contacts'][item.text()]
        sms.add(phone) if item.checkState() else sms.delete(phone)

    def onSend(self):
        self._send.setEnabled(False)
        sms.send(self._config['api'], self._text.toPlainText(), self._log)
        self._send.setEnabled(True)

    def onToggleAll(self, event):
        for index in range(self._contactListModel.rowCount()):
            item = self._contactListModel.item(index)
            if item.isCheckable() == False:
                continue
            if item.checkState() == Qt.Unchecked:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)

    def addToggleAll(self):
        label = QLabel('Toggle All', self)
        label.mousePressEvent = self.onToggleAll
        self._layout.addWidget(label, 0,0)
        return self

    def addText(self):
        self._layout.addWidget(QLabel('Your text goes here', self), 0, 1)
        return self

    def addContactList(self):
        list = QListView(self)
        self._contactListModel = QStandardItemModel(list)
        self._contactListModel.itemChanged.connect(self.onItemChanged)
        for contact in self._config['contacts']:
            item = QStandardItem(contact)
            item.setCheckable(True)
            item.setEditable(False)
            self._contactListModel.appendRow(item)
        list.setModel(self._contactListModel)
        self._layout.addWidget(list, 1, 0)
        return self

    def addTextarea(self):
        self._text = QPlainTextEdit(self)
        self._layout.addWidget(self._text, 1, 1)
        return self

    def addLog(self):
        self._log = QLabel('UI loaded')
        self._layout.addWidget(self._log, 2, 0)
        return self

    def addSend(self):
        self._send = QPushButton('Send')
        self._send.clicked.connect(self.onSend)
        self._layout.addWidget(self._send, 2, 1)
        return self

    def setGeometry(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        return self

    def init(self):
        self._layout = QGridLayout(self)

        # Widgets
        self.addToggleAll().addText() # Row 0
        self.addContactList().addTextarea() # Row 1
        self.addLog().addSend() # Row 2

        # Window
        self.setGeometry().setLayout(self._layout)
        self.setWindowTitle("Twilio SMS GUI - rakshazi.me")
        self.setWindowIcon(QIcon.fromTheme("send-to-symbolic"))
        self.show()
