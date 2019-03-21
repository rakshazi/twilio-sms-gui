#!/usr/bin/env python3
from src import ui
from sys import exit
from PyQt5.QtWidgets import QApplication

app = QApplication([])
app.setStyle('Fusion')
window = ui.UI()
exit(app.exec_())
