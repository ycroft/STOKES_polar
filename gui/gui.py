#!/usr/bin/python
# gui.py

import sys
from PyQt4 import QtGui,QtCore

class SigSlot(QtGui.QWidget):
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		self.setWindowTitle("signal and slot")
		self.setMouseTracking(True)
		self.setObjectName("main_window")
		style = '''
			QWidget#main_window{
				background-color: #F2EABC;
			}
			QPushButton#button{
				background-color: #EEEEEE;
				border: 3px solid #242424;
				color: #242424;
				width: 120px;
				height: 30px;
				font-size: 15px;
				font-weight: bold;
				line-height: 30px;
			}
			QPushButton#button:hover{
				background-color: #242424;
				border: 2px solid #EEEEEE;
				color: #EEEEEE;
			}
		'''

		start = QtGui.QPushButton('START')
		exit = QtGui.QPushButton('EXIT')
		start.setObjectName("button")
		exit.setObjectName("button")
		main = QtGui.QVBoxLayout()
		panel_buttons = QtGui.QHBoxLayout()
		panel_upper = QtGui.QHBoxLayout()
		panel_buttons.addStretch(1)
		panel_buttons.addWidget(start)
		panel_buttons.addWidget(exit)
		main.addLayout(panel_upper)
		main.addStretch(1)
		main.addLayout(panel_buttons)
		self.connect(exit,QtCore.SIGNAL('clicked()'),QtGui.qApp,QtCore.SLOT('quit()'))
		self.setLayout(main)
		self.resize(500,300)
		self.move(500,300)
		self.setStyleSheet(style)

	def mousePressEvent(self, event):
		if event.button()==QtCore.Qt.LeftButton:
			self.m_drag=True
			self.m_DragPosition=event.globalPos()-self.pos()
			event.accept()

	def mouseMoveEvent(self, QMouseEvent):
		if QMouseEvent.buttons() and QtCore.Qt.LeftButton:
			self.move(QMouseEvent.globalPos()-self.m_DragPosition)
			QMouseEvent.accept()

	def mouseReleaseEvent(self, QMouseEvent):
		self.m_drag=False

app = QtGui.QApplication(sys.argv)
qb = SigSlot()
qb.show()
sys.exit(app.exec_())