#coding=utf8

from PyQt4 import QtCore
from PyQt4 import QtGui
from polar import Polar
import sys

class MainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupCore()
        self.setupUI()
    
    def setupCore(self):
        '''
        status:
            0 :     waiting
            1 :     running
            -1 :    crashed
        '''
        self.status = 0
        self.fpath_mrls = ''
        self.fpath_urls = ''
        self.fpath_mls = ''
        self.sapp = Polar(self)

    def setupUI(self):
        # 定义组件
        self.button_start = QtGui.QPushButton(u'启动')
        self.button_exit = QtGui.QPushButton(u'退出')
        self.button_fopen_urefer = QtGui.QPushButton(u'选择未调制参考光')
        self.button_fopen_mrefer = QtGui.QPushButton(u'选择已调制参考光')
        self.button_fopen_meassure = QtGui.QPushButton(u'选择实测光谱')
        self.button_plot_mls = QtGui.QPushButton(u'实测')
        self.button_plot_mf = QtGui.QPushButton(u'载波')
        self.button_plot_af = QtGui.QPushButton(u'自相关函数')
        self.button_plot_ch = QtGui.QPushButton(u'调制各通道')
        self.button_plot_sv = QtGui.QPushButton(u'STOKES矢量')
        self.button_plot_dop = QtGui.QPushButton(u'偏振')
        self.label_isset_urefer = QtGui.QLabel(u'未设置')
        self.label_isset_mrefer = QtGui.QLabel(u'未设置')
        self.label_isset_meassure = QtGui.QLabel(u'未设置')
        self.label_title_plot = QtGui.QLabel(u'绘制图像')
        self.label_conf_ns = QtGui.QLabel(u'插值点数: 2^')
        self.label_conf_lens_1 = QtGui.QLabel(u'LENS_1:')
        self.label_conf_lens_2 = QtGui.QLabel(u'LENS_2:')
        self.label_status = QtGui.QLabel(u'=等待=')
        self.lineedit_conf_ns = QtGui.QLineEdit()
        self.lineedit_conf_lens_1 = QtGui.QLineEdit()
        self.lineedit_conf_lens_2 = QtGui.QLineEdit()
        self.checkbox_conf_autofix = QtGui.QCheckBox(u'载波自动修正')
        self.checkbox_conf_highfreq = QtGui.QCheckBox(u'使用高频成分')
        self.checkbox_mf = QtGui.QCheckBox(u'重新计算载波')

        self.lineedit_conf_ns.setText('10')
        self.lineedit_conf_lens_1.setText('1.9')
        self.lineedit_conf_lens_2.setText('3.6')
        self.checkbox_mf.setCheckState(2)
        self.checkbox_conf_autofix.setCheckState(2)
        self.checkbox_conf_highfreq.setCheckState(2)

        # 设置布局
        layout_main = QtGui.QVBoxLayout()
        layout_settings = QtGui.QVBoxLayout()
        layout_buttons = QtGui.QHBoxLayout()
        layout_settings_grid = QtGui.QGridLayout()
        layout_status_bar = QtGui.QHBoxLayout()

        layout_settings_grid.addWidget(self.label_isset_urefer,0,0,1,1)
        layout_settings_grid.addWidget(self.label_isset_mrefer,1,0,1,1)
        layout_settings_grid.addWidget(self.button_fopen_urefer,0,1,1,1)
        layout_settings_grid.addWidget(self.button_fopen_mrefer,1,1,1,1)
        layout_settings_grid.addWidget(self.checkbox_mf,2,0,1,2)
        layout_settings_grid.addWidget(self.label_isset_meassure,3,0,1,1)
        layout_settings_grid.addWidget(self.button_fopen_meassure,3,1,1,1)

        layout_settings_grid.addWidget(self.label_conf_ns,4,0,1,1)
        layout_settings_grid.addWidget(self.label_conf_lens_1,5,0,1,1)
        layout_settings_grid.addWidget(self.label_conf_lens_2,6,0,1,1)
        layout_settings_grid.addWidget(self.lineedit_conf_ns,4,1,1,1)
        layout_settings_grid.addWidget(self.lineedit_conf_lens_1,5,1,1,1)
        layout_settings_grid.addWidget(self.lineedit_conf_lens_2,6,1,1,1)
        layout_settings_grid.addWidget(self.checkbox_conf_autofix,7,0,1,2)
        layout_settings_grid.addWidget(self.checkbox_conf_highfreq,8,0,1,2)

        layout_settings_grid.addWidget(self.label_title_plot,9,0,1,2)
        layout_settings_grid.addWidget(self.button_plot_mls,10,0,1,1)
        layout_settings_grid.addWidget(self.button_plot_mf,11,0,1,1)
        layout_settings_grid.addWidget(self.button_plot_dop,12,0,1,1)
        layout_settings_grid.addWidget(self.button_plot_af,10,1,1,1)
        layout_settings_grid.addWidget(self.button_plot_ch,11,1,1,1)
        layout_settings_grid.addWidget(self.button_plot_sv,12,1,1,1)
        layout_settings_grid.setColumnStretch(2, 1);

        layout_settings.addLayout(layout_settings_grid)
        layout_settings.addStretch(1)
        layout_buttons.addStretch(1)
        layout_buttons.addWidget(self.label_status)
        layout_buttons.addWidget(self.button_start)
        layout_buttons.addWidget(self.button_exit)
        layout_main.addLayout(layout_settings)
        layout_main.addLayout(layout_buttons)
        self.setLayout(layout_main)

        # 设置信号与槽
        self.connect(self.button_start, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('startup()'))
        self.connect(self.button_exit, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('exit()'))
        self.connect(self.button_fopen_mrefer, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('chooseMRLS()'))
        self.connect(self.button_fopen_urefer, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('chooseURLS()'))
        self.connect(self.button_fopen_meassure, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('chooseMLS()'))
        self.connect(self.checkbox_mf, QtCore.SIGNAL('stateChanged(int)'), self, QtCore.SLOT('disableRefer()'))
        self.connect(self.sapp, QtCore.SIGNAL('missionStart()'), self, QtCore.SLOT('statusStart()'))
        self.connect(self.sapp, QtCore.SIGNAL('missionComplete()'), self, QtCore.SLOT('statusComplete()'))
        self.connect(self.sapp, QtCore.SIGNAL('missionFailed()'), self, QtCore.SLOT('statusFailed()'))

    @QtCore.pyqtSlot()
    def disableRefer(self):
        checked = self.checkbox_mf.isChecked()
        self.button_fopen_urefer.setEnabled(checked)
        self.button_fopen_mrefer.setEnabled(checked)
        if checked:
            self.label_isset_urefer.setText(u'未设置')
            self.label_isset_mrefer.setText(u'未设置')
        else:
            self.label_isset_urefer.setText(u'已禁用')
            self.label_isset_mrefer.setText(u'已禁用')

    @QtCore.pyqtSlot()
    def exit(self):
        self.sapp.exit(0)
        QtGui.qApp.quit()

    @QtCore.pyqtSlot()
    def chooseMRLS(self):
        self.fpath_mrls = QtGui.QFileDialog.getOpenFileName(self, u'选取已调制参考光')
        self.label_isset_mrefer.setText(u'已设置')

    @QtCore.pyqtSlot()
    def chooseURLS(self):
        self.fpath_urls = QtGui.QFileDialog.getOpenFileName(self, u'选取未调制参考光')
        self.label_isset_urefer.setText(u'已设置')

    @QtCore.pyqtSlot()
    def chooseMLS(self):
        self.fpath_mls = QtGui.QFileDialog.getOpenFileName(self, u'选取实测光谱')
        self.label_isset_meassure.setText(u'已设置')

    @QtCore.pyqtSlot()
    def startup(self):
        mf = self.checkbox_mf.isChecked()
        ns = 1024
        d1 = (float)(self.lineedit_conf_lens_1.text())
        d2 = (float)(self.lineedit_conf_lens_2.text())
        autofix = self.checkbox_conf_autofix.isChecked()
        if self.checkbox_conf_highfreq:
            freq = 'high'
        else:
            freq = 'low'
        urls = unicode(self.fpath_urls)
        mrls = unicode(self.fpath_mrls)
        mls = unicode(self.fpath_mls)
        conf = {
            'mf': mf,
            'ns': ns,
            'd1': d1,
            'd2': d2,
            'autofix': autofix,
            'freq': freq,
            'urls': urls,
            'mrls': mrls,
            'mls': mls
        }
        self.sapp.config(conf)
        self.sapp.start()
    
    @QtCore.pyqtSlot()
    def statusStart(self):
        self.status = 1
        self.renewStatus()

    @QtCore.pyqtSlot()
    def statusComplete(self):
        self.status = 0
        self.renewStatus()

    @QtCore.pyqtSlot()
    def statusFailed(self):
        self.status = -1
        self.renewStatus()

    @QtCore.pyqtSlot()
    def renewStatus(self):
        if self.status == 0:
            self.label_status.setText(u'=等待=')
        elif self.status == 1:
            self.label_status.setText(u'=运行=')
        elif self.status == -1:
            self.label_status.setText(u'=错误=')

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = MainWidget()
    mw.show()
    sys.exit(app.exec_())
