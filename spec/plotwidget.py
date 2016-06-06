# -*- coding: utf-8 -*-
from matplotlib import figure
from PyQt4 import QtCore
import pylab

class PlotWidget(QtCore.QThread):
    def __init__(self,data,parent):
        QtCore.QThread.__init__(self,parent)
        self.x = data.getXaxis()
        self.y = data.getYaxis()

    def run(self):
        pylab.plot(self.x, self.y, color='black', linestyle='-')
        pylab.show()

class Datagram(object):
    def __init__(self,baseConfig):
        pylab.clf()
        pylab.title(baseConfig.get('title','NoName'))
        pylab.ylabel(baseConfig.get('ylabel','NoName'))
        pylab.xlabel(baseConfig.get('xlabel','NoName'))
        pylab.grid(baseConfig.get('grid',False))
        
        pylab.grid(True)

    def lim(self,xl,xr,yl,yr):
        pylab.xlim(xl,xr)
        pylab.ylim(yl,yr)

    def add(self,data,lineConf,local=0):
        marker = lineConf.get('marker',None)
        color = lineConf.get('color', 'r')
        markerfacecolor = lineConf.get('markerfacecolor',color)
        label = lineConf.get('label','NoName')
        linewidth = lineConf.get('linewidth',1)
        linestyle = lineConf.get('linestyle','-')

        pylab.plot(data.getXaxis(),data.getYaxis(), marker=marker,
            color=color,markerfacecolor=markerfacecolor, label=label,
            linewidth=linewidth,linestyle=linestyle)
        pylab.legend(loc=local)

    def show(self):
        pylab.show()

    def save(self,fname):
        pylab.savefig(fname+'.jpg')

    def plotAll(self,data,**args):
        if 'style' in args:
            style = args['style']
        else:
            style = 'null'
        num = len(data)
        row = args['row']
        column = num / (row + 1) + 1
        for i in range(1,num+1):
            index_r = (i-1) % row + 1
            index_c = (i-1) / row + 1
            index = (index_r-1)*column + index_c
            position = str(row) + str(column) + str(index)
            pylab.subplot(position)
            if style == 'line' or style == 'null':
                pylab.plot(data[i-1].getXaxis(),data[i-1].getYaxis(), label='interped values')
            elif style == 'dot':
                pylab.plot(data[i-1].getXaxis(),data[i-1].getYaxis(), '--b*')

        pylab.show()

    def plotTogether(self,args):
        l = len(args)
        for d in args:
            data = d[0]
            lineConf = d[1]

            marker = lineConf.get('marker',None)
            color = lineConf.get('color', 'r')
            markerfacecolor = lineConf.get('markerfacecolor',color)
            label = lineConf.get('label','NoName')
            linewidth = lineConf.get('linewidth',1)
            linestyle = lineConf.get('linestyle','-')

            pylab.plot(data.getXaxis(),data.getYaxis(), marker=marker,
                color=color,markerfacecolor=markerfacecolor, label=label,
                linewidth=linewidth,linestyle=linestyle)
            pylab.legend(loc = 0)
        pylab.show()

if __name__ == '__main__':
    from PyQt4 import QtGui
    import sys
    app = QtGui.QApplication(sys.argv)
    pw = PlotWidget(app)
    pw.start()
    sys.exit(app.exec_())
