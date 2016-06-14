#coding=utf8

from PyQt4 import QtCore
from PyQt4 import QtGui
from polar import Polar
import sys
import pylab
import warnings

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
        self.sapp = Polar()

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
        self.button_plot_urls = QtGui.QPushButton(u'未调制参考光')
        self.button_plot_mrls = QtGui.QPushButton(u'已调制参考光')
        self.button_plot_nsv = QtGui.QPushButton(u'归一化矢量')
        self.button_plot_sffti = QtGui.QPushButton(u'参考光自相关')
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
        layout_settings_grid.addWidget(self.button_plot_mrls,13,0,1,1)
        layout_settings_grid.addWidget(self.button_plot_urls,13,1,1,1)
        layout_settings_grid.addWidget(self.button_plot_sffti,14,0,1,1)
        layout_settings_grid.addWidget(self.button_plot_nsv,14,1,1,1)
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
        self.connect(self.button_plot_sv, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('plotSV()'))
        self.connect(self.button_plot_ch, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('plotCHX()'))
        self.connect(self.button_plot_af, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('plotFFTX()'))
        self.connect(self.button_plot_dop, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('plotDOP()'))
        self.connect(self.button_plot_mf, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('plotMF()'))
        self.connect(self.button_plot_mls, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('plotMLS()'))
        self.connect(self.button_plot_urls, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('plotURLS()'))
        self.connect(self.button_plot_mrls, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('plotMRLS()'))
        self.connect(self.button_plot_nsv, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('plotNSV()'))
        self.connect(self.button_plot_sffti, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('plotSFFTX()'))
        self.connect(self.checkbox_mf, QtCore.SIGNAL('stateChanged(int)'), self, QtCore.SLOT('disableRefer()'))

    def figPlot(self, datagram, title='', color='black'):
        fig = pylab.figure(title)
        pylab.plot(datagram.getXaxis(),datagram.getYaxis(),label=title,color=color,linestyle='-')

    @QtCore.pyqtSlot()
    def plotDOP(self):
        pylab.close()
        self.figPlot(self.sapp.dop,'DOP', 'blue')
        pylab.show()

    @QtCore.pyqtSlot()
    def plotSV(self):
        pylab.close()
        self.figPlot(self.sapp.s0, 'STOKES VECTOR 0', 'red')
        self.figPlot(self.sapp.s1, 'STOKES VECTOR 1', 'black')
        self.figPlot(self.sapp.s2, 'STOKES VECTOR 2', 'blue')
        self.figPlot(self.sapp.s3, 'STOKES VECTOR 3', 'green')
        pylab.show()

    @QtCore.pyqtSlot()
    def plotFFTX(self):
        pylab.close()
        pylab.plot(self.sapp.rffti[0].getXaxis(),self.sapp.rffti[0].getYaxis(),label='FFT CHANNEL 0')
        pylab.plot(self.sapp.rffti[1].getXaxis(),self.sapp.rffti[1].getYaxis(),label='FFT CHANNEL 1')
        pylab.plot(self.sapp.rffti[2].getXaxis(),self.sapp.rffti[2].getYaxis(),label='FFT CHANNEL 2')
        pylab.plot(self.sapp.rffti[3].getXaxis(),self.sapp.rffti[3].getYaxis(),label='FFT CHANNEL 3')
        pylab.show()

    @QtCore.pyqtSlot()
    def plotMF(self):
        pylab.close()
        self.figPlot(self.sapp.cs0, 'MODULATION FACTOR 0', 'red')
        self.figPlot(self.sapp.cs1, 'MODULATION FACTOR 1', 'black')
        self.figPlot(self.sapp.cs2, 'MODULATION FACTOR 2', 'blue')
        self.figPlot(self.sapp.cs3, 'MODULATION FACTOR 3', 'green')
        pylab.show()

    @QtCore.pyqtSlot()
    def plotCHX(self):
        pylab.close()
        self.figPlot(self.sapp.fa0, 'CHANNEL 0', 'red')
        self.figPlot(self.sapp.fa1, 'CHANNEL 1', 'black')
        self.figPlot(self.sapp.fa2, 'CHANNEL 2', 'blue')
        self.figPlot(self.sapp.fa3, 'CHANNEL 3', 'green')
        pylab.show()

    @QtCore.pyqtSlot()
    def plotMLS(self):
        pylab.close()
        self.figPlot(self.sapp.rdata, 'MEASURED DATA', 'blue')
        pylab.show()

    @QtCore.pyqtSlot()
    def plotMRLS(self):
        pylab.close()
        self.figPlot(self.sapp.sdata, 'MODULATED REFERENCE LIGHT SPECTRUM', 'blue')
        pylab.show()

    @QtCore.pyqtSlot()
    def plotURLS(self):
        pylab.close()
        self.figPlot(self.sapp.idata, 'MODULATED REFERENCE LIGHT SPECTRUM', 'blue')
        pylab.show()

    @QtCore.pyqtSlot()
    def plotNSV(self):
        pylab.close()
        self.figPlot(self.sapp.nsv1, 'NOMALIZED STOKES VECTOR 1', 'red')
        self.figPlot(self.sapp.nsv2, 'NOMALIZED STOKES VECTOR 2', 'green')
        self.figPlot(self.sapp.nsv3, 'NOMALIZED STOKES VECTOR 3', 'blue')
        pylab.show()

    @QtCore.pyqtSlot()
    def plotSFFTX(self):
        pylab.close()
        pylab.plot(self.sapp.sffti[0].getXaxis(),self.sapp.sffti[0].getYaxis(),label='RLS FFT CHANNEL 0')
        pylab.plot(self.sapp.sffti[1].getXaxis(),self.sapp.sffti[1].getYaxis(),label='RLS FFT CHANNEL 1')
        pylab.plot(self.sapp.sffti[2].getXaxis(),self.sapp.sffti[2].getYaxis(),label='RLS FFT CHANNEL 2')
        pylab.plot(self.sapp.sffti[3].getXaxis(),self.sapp.sffti[3].getYaxis(),label='RLS FFT CHANNEL 3')
        pylab.show()

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
        self.label_status.setText(u'*运行*')
        mf = self.checkbox_mf.isChecked()
        ns = 1024
        d1 = (float)(self.lineedit_conf_lens_1.text())
        d2 = (float)(self.lineedit_conf_lens_2.text())
        autofix = self.checkbox_conf_autofix.isChecked()
        if self.checkbox_conf_highfreq.isChecked():
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
        print('***DONE***')
        self.label_status.setText(u'=等待=')

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    app = QtGui.QApplication(sys.argv)
    mw = MainWidget()
    mw.show()
    sys.exit(app.exec_())
