import spec
import os
import sys,getopt
import reporter

class Polar:
    
    # missionStart = QtCore.pyqtSignal()
    # missionComplete = QtCore.pyqtSignal()
    # missionFailed = QtCore.pyqtSignal()

    def __init__(self):
        self.globalConfig = {
            'mf': True,
            'ns': 1024,
            'd1': 1.9,
            'd2': 3.8,
            'autofix': True,
            'freq': 'high',
            'urls': '',
            'mrls': '',
            'mls': ''
        }

    def config(self, conf):
        self.globalConfig = conf

    def startup(self):
        # self.emit(QtCore.SIGNAL('missionStart()'))
        '''
            config :
                --ns        default
                --d1        default
                --d2        default
                --autofix   default
                --frequency default
                ==mrls     NOT NULL
                ==urls     NOT NULL
                ==mls     NOT NULL
        '''
        self.calcMf = self.globalConfig.get('mf',True)
        self.NS = self.globalConfig.get('ns',1024)
        self.D1 = self.globalConfig.get('d1',1.9)
        self.D2 = self.globalConfig.get('d2',3.8)
        self.autofix = self.globalConfig.get('autofix',True)
        self.frequency = self.globalConfig.get('freq','high')
        self.sdataPath = self.globalConfig.get('mrls', '')
        self.idataPath = self.globalConfig.get('urls', '')
        self.rdataPath = self.globalConfig.get('mls', '')

        self.sdataName = (self.sdataPath.split('/')[-1]).split('.')[0]
        self.rdataName = (self.rdataPath.split('/')[-1]).split('.')[0]
        self.workpath = './spec_data/'

        if self.rdataName=='' and self.calcMf:
            print('MF DATA FILE NOT FOUND')
            # self.emit(QtCore.SIGNAL('missionFailed()'))
            return
        if self.rdataName=='':
            print('RAW DATA FILE NOT FOUND')
            # self.emit(QtCore.SIGNAL('missionFailed()'))
            return
        if self.workpath[-1] != '/':
            self.workpath += '/'
        if not os.path.isdir(self.workpath):
            os.mkdir(self.workpath)
        if not os.path.isdir(self.workpath + 'img/'):
            os.mkdir(self.workpath + 'img/')
        if not os.path.isdir(self.workpath + 'repo/'):
            os.mkdir(self.workpath + 'repo/')

        self.imgPath = self.workpath + 'img/'
        self.repoPath = self.workpath + 'repo/'

        self.cs0 = spec.df.SpectrumData()
        self.cs1 = spec.df.SpectrumData()
        self.cs2 = spec.df.SpectrumData()
        self.cs3 = spec.df.SpectrumData()
        self.windows = []

        self.rdata = spec.df.SpectrumData()
        self.rffti = spec.df.SpectrumData()
        self.sfft = spec.df.SpectrumData()
        self.sffti = spec.df.SpectrumData()

        self.fa0 = spec.df.SpectrumData()
        self.fa1 = spec.df.SpectrumData()
        self.fa2 = spec.df.SpectrumData()
        self.fa3 = spec.df.SpectrumData()

        self.s0 = spec.df.SpectrumData()
        self.s1 = spec.df.SpectrumData()
        self.s2 = spec.df.SpectrumData()
        self.s3 = spec.df.SpectrumData()

        self.dop = spec.df.SpectrumData()

        if self.calcMf:
            self.exportCsx()
        self.importCsx()
        self.doSi()
        self.doDop()
        self.savePlotRaw()
        self.savePlotCsi()
        self.savePlotFft()
        self.savePlotFai()
        self.savePlotSi()
        self.savePlotDop()
        # self.emit(QtCore.SIGNAL('missionComplete()'))

    def start(self):
        self.startup()

    def exportCsx(self):
        self.sdata = spec.df.SpectrumData(self.sdataPath)
        outputName = self.workpath + '_auto'
        self.sdata.scaleX(1E-7)
        self.sdata.reciprocalX()
        sdomain = self.sdata.getXdomain()
        self.sfft = sfft = spec.fft.fft(self.sdata,self.NS)
        checkfft = sfft.abs()
        # checkfft.slice(0.5)
        sfeature = spec.reco.Feature(checkfft)
        sfeature.start(8)
        swindows = sfeature.getWindows()
        self.windows = swindows
        self.sffti = sffti = spec.reco.filter(swindows,sfft)
        ms0 = spec.fft.ifft(sffti[0] + sffti[7],sdomain,self.NS)
        ms1 = spec.fft.ifft(sffti[1],sdomain,self.NS)
        ms2 = spec.fft.ifft(sffti[2],sdomain,self.NS)
        ms3 = spec.fft.ifft(sffti[3],sdomain,self.NS)
        msx = ms0.getXaxis()

        self.idata = spec.df.SpectrumData(self.idataPath)
        self.idata.scaleX(1E-7)
        self.idata.reciprocalX()
        self.idata.spline(msx)

        tmpcs0 = ms0/self.idata
        tmpcs1 = (ms1*(2.0**0.5))/self.idata
        tmpcs2 = (ms2*(2.0**0.5))/self.idata
        tmpcs3 = ((ms3*(2.0**0.5))*-1.0)/self.idata

        tmpcs0.formatExport(outputName+'.scs0')
        tmpcs1.formatExport(outputName+'.scs1')
        tmpcs2.formatExport(outputName+'.scs2')
        tmpcs3.formatExport(outputName+'.scs3')

        ofile = open(outputName+'.win','w')
        format_data = ''
        for i in swindows:
            format_data = format_data + str(i[0]) + ' ' + str(i[1]) + '\n'
        ofile.write(format_data)
        ofile.close()

    def importCsx(self):
        fname = self.workpath + '_auto'
        f0 = fname+'.scs0'
        f1 = fname+'.scs1'
        f2 = fname+'.scs2'
        f3 = fname+'.scs3'
        self.cs0.formatImport(f0)
        self.cs1.formatImport(f1)
        self.cs2.formatImport(f2)
        self.cs3.formatImport(f3)

        ifile = open(fname+'.win','r')
        content = ifile.readlines()
        for line in content:
            x = line.split(' ')
            self.windows.append([float(x[0]),float(x[1])])

    def doSi(self):
        k_0 = self.cs0
        k_1 = self.cs1
        k_2 = self.cs2
        k_3 = self.cs3
        self.rdata = rdata = spec.df.SpectrumData(self.rdataPath)
        rdata.scaleX(1E-7)
        rdata.reciprocalX()
        rdomain = rdata.getXdomain()
        rfft = spec.fft.fft(rdata,self.NS)
        self.rffti = rffti = spec.reco.filter(self.windows,rfft)
        self.fa0 = fa0 = spec.fft.ifft(rffti[0] + rffti[7],rdomain,self.NS)
        self.fa1 = fa1 = spec.fft.ifft(rffti[1],rdomain,self.NS)
        self.fa2 = fa2 = spec.fft.ifft(rffti[2],rdomain,self.NS)
        self.fa3 = fa3 = spec.fft.ifft(rffti[3],rdomain,self.NS)

        if self.autofix == True:
            tmpd = ((fa2/self.cs2)**2.0) + ((fa1*fa3)/(self.cs1*self.cs3))
            theta = tmpd.arg()
            phi2 = theta/2.0
            phi1 = phi2 * (self.D2/self.D1)
            k_0 = k_0
            k_1 = k_1.rotate(phi2-phi1)
            k_2 = k_2.rotate(phi2)
            k_3 = k_3.rotate(phi2-phi1)

        s0 = fa0/k_0
        s1 = fa2/k_2
        s23 = fa1/k_1
        s23n = fa3/k_3
        s2 = s23.real() 
        s3 = s23.imag()
        s2n = s23n.real()
        s3n = s23n.imag()

        if self.frequency == 'high':
            print 'HIGH'
            self.s0 = s0
            self.s1 = s1
            self.s2 = s2n
            self.s3 = s3n
        else:
            self.s0 = s0
            self.s1 = s1
            self.s2 = s2
            self.s3 = s3

        self.nsv1 = s1/s0
        self.nsv2 = s2/s0
        self.nsv3 = s3/s0

    def doDop(self):
        self.dop = (((self.s1**2.0) + (self.s2**2.0) + (self.s3**2.0))**0.5)/self.s0

    def savePlotRaw(self):
        dg = spec.plot.Datagram({
            'title' : 'spectrum data of ' + self.rdataName,
            'xlabel': 'wave number(cm-1)',
            'ylabel': ' ',
            'grid' : True
        })
        style = {
            'color' : 'k',
            'label' : 'raw data',
            'linewidth' : '1',
            'linestyle' : '-'
        }
        dg.add(self.rdata,style)
        dg.save(self.imgPath + self.rdataName + '_' + 'rd')
        # dg.show()

    def savePlotCsi(self):
        cs0 = spec.plot.Datagram({
            'title' : 'modulation factor 0',
            'xlabel': 'wave number(cm-1)',
            'ylabel': ' ',
            'grid' : True
        })
        style_cs0 = {
            'color' : 'r',
            'label' : 'MF_0',
            'linewidth' : '1',
            'linestyle' : '-'
        }
        cs0.add(self.cs0,style_cs0)
        cs0.save(self.imgPath + self.sdataName + '_' + 'cs0')
        # cs0.show()

        cs1 = spec.plot.Datagram({
            'title' : 'modulation factor 1',
            'xlabel': 'wave number(cm-1)',
            'ylabel': ' ',
            'grid' : True
        })
        style_cs1 = {
            'color' : 'g',
            'label' : 'MF_1',
            'linewidth' : '1',
            'linestyle' : '-'
        }
        cs1.add(self.cs1,style_cs1)
        cs1.save(self.imgPath + self.sdataName + '_' + 'cs1')
        # cs1.show()

        cs2 = spec.plot.Datagram({
            'title' : 'modulation factor 2',
            'xlabel': 'wave number(cm-1)',
            'ylabel': ' ',
            'grid' : True
        })
        style_cs2 = {
            'color' : 'b',
            'label' : 'MF_2',
            'linewidth' : '1',
            'linestyle' : '-'
        }
        cs2.add(self.cs2,style_cs2)
        cs2.save(self.imgPath + self.sdataName + '_' + 'cs2')
        # cs2.show()

        cs3 = spec.plot.Datagram({
            'title' : 'modulation factor 3',
            'xlabel': 'wave number(cm-1)',
            'ylabel': ' ',
            'grid' : True
        })
        style_cs3 = {
            'color' : 'm',
            'label' : 'MF_3',
            'linewidth' : '1',
            'linestyle' : '-'
        }
        cs3.add(self.cs3,style_cs3)
        cs3.save(self.imgPath + self.sdataName + '_' + 'cs3')
        # cs3.show()

    def savePlotFft(self):
        datagram = spec.plot.Datagram({
            'title' : 'FFT signal',
            'xlabel': ' ',
            'ylabel': ' ',
            'grid' : True
        })
        fft0 = self.rffti[0] + self.rffti[7]
        fft1 = self.rffti[1] + self.rffti[6]
        fft2 = self.rffti[2] + self.rffti[5]
        fft3 = self.rffti[3] + self.rffti[4]

        style_rfft0={
            'color' : 'g',
            'label' : '#0 peak',
            'linewidth' : '1',
            'linestyle' : '-'
        }
        style_rfft1={
            'color' : 'm',
            'label' : '#1 peak',
            'linewidth' : '1',
            'linestyle' : '-'
        }
        style_rfft2={
            'color' : 'c',
            'label' : '#2 peak',
            'linewidth' : '1',
            'linestyle' : '-'
        }
        style_rfft3={
            'color' : 'b',
            'label' : '#3 peak',
            'linewidth' : '1',
            'linestyle' : '-'
        }
        datagram.add(fft0,style_rfft0)
        datagram.add(fft1,style_rfft1)
        datagram.add(fft2,style_rfft2)
        datagram.add(fft3,style_rfft3)
        # datagram.lim(-0.001,0.061,-200000,200000)
        datagram.save(self.imgPath + self.rdataName + '_' + 'fft')
        # datagram.show()

    def savePlotFai(self):
        fa0 = spec.plot.Datagram({
            'title' : 'modulation signal 0 of ' + self.rdataName,
            'xlabel': 'wave number(cm-1)',
            'ylabel': ' ',
            'grid' : True
        })
        style_fa0 = {
            'color' : 'r',
            'label' : 'MS_0',
            'linewidth' : 1,
            'linestyle' : '-'
        }
        fa0.add(self.fa0,style_fa0)
        fa0.save(self.imgPath + self.rdataName + '_' + 'fa0')
        # fa0.show()
        fa1 = spec.plot.Datagram({
            'title' : 'modulation signal 1 of ' + self.rdataName,
            'xlabel': 'wave number(cm-1)',
            'ylabel': ' ',
            'grid' : True
        })
        style_fa1 = {
            'color' : 'g',
            'label' : 'MS_1',
            'linewidth' : 1,
            'linestyle' : '-'
        }
        fa1.add(self.fa1,style_fa1)
        fa1.save(self.imgPath + self.rdataName + '_' + 'fa1')
        # fa1.show()
        fa2 = spec.plot.Datagram({
            'title' : 'modulation signal 2 of ' + self.rdataName,
            'xlabel': 'wave number(cm-1)',
            'ylabel': ' ',
            'grid' : True
        })
        style_fa2 = {
            'color' : 'b',
            'label' : 'MS_2',
            'linewidth' : 1,
            'linestyle' : '-'
        }
        fa2.add(self.fa2,style_fa2)
        fa2.save(self.imgPath + self.rdataName + '_' + 'fa2')
        # fa2.show()
        fa3 = spec.plot.Datagram({
            'title' : 'modulation signal 3 of ' + self.rdataName,
            'xlabel': 'wave number(cm-1)',
            'ylabel': ' ',
            'grid' : True
        })
        style_fa3 = {
            'color' : 'm',
            'label' : 'MS_3',
            'linewidth' : 1,
            'linestyle' : '-'
        }
        fa3.add(self.fa3,style_fa3)
        fa3.save(self.imgPath + self.rdataName + '_' + 'fa3')
        # fa3.show()

    def savePlotSi(self):
        ds0 = spec.plot.Datagram({
            'title' : 'S_0 of ' + self.rdataName,
            'xlabel': 'wave number(cm-1)',
            'ylabel': ' ',
            'grid' : True
        })
        style_ds0 = {
            'color' : 'r',
            'label' : 'S_0',
            'linewidth' : 1.5,
            'linestyle' : '-'
        }
        ds0.add(self.s0,style_ds0)
        ds0.save(self.imgPath + self.rdataName + '_' + 's0')
        # ds0.show()
        ds1 = spec.plot.Datagram({
            'title' : 'S_1 of ' + self.rdataName,
            'xlabel': 'wave number(cm-1)',
            'ylabel': ' ',
            'grid' : True
        })
        style_ds1 = {
            'color' : 'g',
            'label' : 'S_1',
            'linewidth' : 1.5,
            'linestyle' : '-'
        }
        ds1.add(self.s1,style_ds1)
        ds1.save(self.imgPath + self.rdataName + '_' + 's1')
        # ds1.show()
        ds2 = spec.plot.Datagram({
            'title' : 'S_2 of ' + self.rdataName,
            'xlabel': 'wave number(cm-1)',
            'ylabel': ' ',
            'grid' : True
        })
        style_ds2 = {
            'color' : 'b',
            'label' : 'S_2',
            'linewidth' : 1.5,
            'linestyle' : '-'
        }
        ds2.add(self.s2,style_ds2)
        ds2.save(self.imgPath + self.rdataName + '_' + 's2')
        # ds2.show()
        ds3 = spec.plot.Datagram({
            'title' : 'S_3 of ' + self.rdataName,
            'xlabel': 'wave number(cm-1)',
            'ylabel': ' ',
            'grid' : True
        })
        style_ds3 = {
            'color' : 'm',
            'label' : 'S_3',
            'linewidth' : 1.5,
            'linestyle' : '-'
        }
        ds3.add(self.s3,style_ds3)
        ds3.save(self.imgPath + self.rdataName + '_' + 's3')
        # ds3.show()

    def savePlotDop(self):
        datagram = spec.plot.Datagram({
            'title' : 'DOP/WN of ' + self.rdataName,
            'xlabel': 'wave number(cm-1)',
            'ylabel': 'degree of polarization',
            'grid' : True
        })
        style_dop = {
            # 'marker' : 'x',
            'color' : 'g',
            # 'markerfacecolor' : 'r',
            'label' : 'measured value',
            'linewidth' : '1',
            'linestyle' : '-'
        }
        style_theo = {
            # 'marker' : 'x',
            'color' : 'b',
            # 'markerfacecolor' : 'r',
            'label' : 'theoretical value',
            'linewidth' : '1',
            'linestyle' : '--'
        }
        datagram.add(self.dop,style_dop)
        # theoData = spec.df.SpectrumData('./spec_data/pzd15.dat')
        # if theoData != None:
        #     datagram.add(theoData,style_theo)
        # datagram.lim(12000,19000,0.09,0.75)
        datagram.save(self.imgPath + self.rdataName + '_' + 'dop')
        #datagram.show()

# if __name__ == '__main__':
#     
#     def printHelp():
#         print 'Arguments:'
#         print '\t<-s , --standard>'
#         print '\t\tchoose the file name of the standard data.'
#         print ''
#         print '\t<-r , --raw>'
#         print '\t\tchoose the file name of the raw data.'
#         print ''
#         print '\t[-h , --help]'
#         print '\t\tshow help document.'
#         print ''
#         print '\t[-f , --fastmode]'
#         print '\t\tuse modulation factor which was storaged.'
#         print ''
#         print '\t[-n , --ns]'
#         print '\t\tset the number of the dots revolved in processing.'
#         print ''
#         print '\t[-x , --D1]'
#         print '\t\tset the thickness of lens #1.'
#         print ''
#         print '\t[-y , --D2]'
#         print '\t\tset the thickness of lens #2.'
#         print ''
#         print '\t[-p , --path]'
#         print '\t\tsetup the workplace.'
# 
#     NS = 1024
#     D1 = 1.9
#     D2 = 3.8
#     fastmode = False
#     path = './spec_data/'
#     standard = ''
#     raw = ''
#     try:
#         options,args = getopt.getopt(sys.argv[1:],"fhs:r:n:x:y:p:",
#             ["fastmode","help","standard=","raw=","ns=","d1=","d2=","path="])
#     except getopt.GetoptError:
#         print '! args error'
#         printHelp()
#         sys.exit()
#     
#     for name,value in options:
#         if name == '-f' or name == '--fastmode':
#             fastmode = True
#         elif name == '-s' or name == '--standard':
#             standard = value
#         elif name == '-r' or name == '--raw':
#             raw = value
#         elif name == '-n' or name == '--ns':
#             NS = int(value)
#         elif name == '-x' or name == '--d1':
#             D1 = float(value)
#         elif name == '-y' or name == '--d2':
#             D2 = float(value)
#         elif name == '-p' or name == '--path':
#             path = value
# 
#     if standard == '' or raw == '':
#         printHelp()
#         sys.exit()
# 
#     '''
#         config :
#             --ns        default
#             --d1        default
#             --d2        default
#             --workpath    default
#             --autofix    default
#             --frequency    default
#             ==sdata        NOT NULL
#             ==rdata        NOT NULL
#     '''
#     config = {
#         'ns' : NS,
#         'sdata' : standard,
#         'rdata' : raw,
#         'frequency' : 'high',
#         'workpath' : path
#     }
# 
#     sapp = Polar(config)
#     if fastmode == False:
#         sapp.exportCsx()
#     sapp.importCsx()
#     sapp.doSi()
#     sapp.doDop()
# 
#     sapp.plotCsi()
#     sapp.plotRaw()
#     sapp.plotFft()
#     sapp.plotFai()
#     sapp.plotSi()
#     sapp.plotDop()
# 
#     repo = reporter.Reporter(sapp)
#     repo.gen()
# 

