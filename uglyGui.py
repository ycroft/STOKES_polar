#coding=utf8

from PyQt4 import QtCore
from PyQt4 import QtGui
import sys
import polar

class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUI()

    def setupUI(self):
        # 定义组件
        self.button_start = QtGui.QPushButton(u'启动')
        self.button_exit = QtGui.QPushButton(u'退出')
        self.button_fopen_urefer = QtGui.QPushButton(u'选择未调制参考光')
        self.button_fopen_mrefer = QtGui.QPushButton(u'选择已调制参考光')
        self.label_isset_urefer = QtGui.QLabel(u'未设置')
        self.label_isset_mrefer = QtGui.QLabel(u'未设置')
        self.checkbox_mf = QtGui.QCheckBox(u'重新计算载波')
        self.checkbox_mf.setCheckState(2)

        # 设置布局
        layout_main = QtGui.QVBoxLayout()
        layout_settings = QtGui.QVBoxLayout()
        layout_buttons = QtGui.QHBoxLayout()
        layout_refers = QtGui.QGridLayout()

        layout_refers.addWidget(self.label_isset_urefer,0,0,1,1)
        layout_refers.addWidget(self.label_isset_mrefer,1,0,1,1)
        layout_refers.addWidget(self.button_fopen_urefer,0,1,1,1)
        layout_refers.addWidget(self.button_fopen_mrefer,1,1,1,1)
        layout_refers.addWidget(self.checkbox_mf,2,0,1,2)
        layout_refers.setColumnStretch(2, 1);

        layout_settings.addLayout(layout_refers)
        layout_settings.addStretch(1)
        layout_buttons.addStretch(1)
        layout_buttons.addWidget(self.button_start)
        layout_buttons.addWidget(self.button_exit)
        layout_main.addLayout(layout_settings)
        layout_main.addLayout(layout_buttons)
        self.setLayout(layout_main)

        # 以下部分设置信号与槽
        self.connect(self.button_exit, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))
        self.connect(self.checkbox_mf, QtCore.SIGNAL('stateChanged(int)'), self, QtCore.SLOT('disableRefer()'))

    @QtCore.pyqtSlot()
    def disableRefer(self):
        checked = self.checkbox_mf.isChecked()
        self.button_fopen_urefer.setEnabled(checked)
        self.button_fopen_mrefer.setEnabled(checked)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = MainWidget()
    mw.show()
    sys.exit(app.exec_())
