import re
import numpy as np
import scipy.interpolate as itp
import zipfile

def parseFileWithValuePairs(file_path, xaxis, yaxis):
    dataFile = open(file_path, 'r')
    content = dataFile.readlines()
    for line in content:
        isValid = 1
        for w in line:
            if re.match(r'[a-z]|[A-Z]',w):
                isValid = 0
        if isValid == 1:
            data= re.findall(r'\d+\.*\d+', line)
            if len(data) == 2:
                xaxis.append(float(data[0]))
                yaxis.append(float(data[1]))
    xaxis = np.array(xaxis)
    yaxis = np.array(yaxis)
    dataFile.close()

def parseZipFile(file_path, xaxis, yaxis):
    is_pixel = False
    is_wave_length = False
    target = ''
    zf = zipfile.ZipFile(file_path)
    for fname in zf.namelist():
        if re.match('ps_', fname):
            target = fname
            break

    for line in zf.read(target).split('\n'):
        if re.search('<pixelValues>', line):
            is_pixel = True
            continue
    
        if re.search('</pixelValues>', line):
            is_pixel = False
            continue
    
        if re.search('<channelWavelengths>', line):
            is_wave_length = True;
            continue
    
        if re.search('</channelWavelengths>', line):
            is_wave_length = False;
            continue
    
        if is_pixel:
            res = re.search('<double>([0-9]+\.[0-9]*)</double>', line)
            yaxis.append(float(res.group(1)))
        elif is_wave_length:
            res = re.search('<double>([0-9]+\.[0-9]*)</double>', line)
            xaxis.append(float(res.group(1)))
    zf.close()


class SpectrumData:
    def __init__(self, *args):
        self.index = -1;
        if len(args) == 0 :
            self.__xaxis = []
            self.__yaxis = []
        elif len(args) == 1 :
            self.__xaxis = []
            self.__yaxis = []
            # parseFileWithValuePairs(args[0], self.__xaxis, self.__yaxis)
            parseZipFile(args[0], self.__xaxis, self.__yaxis)
            print 'done','length: ',len(self.__xaxis)
        elif len(args) == 2 :
            self.__xaxis = np.array(args[0])
            self.__yaxis = np.array(args[1])
        else :
            raise TypeError()

    def __iter__(self):
        return self

    def next(self):
        if self.index >= self.length() - 1:
            self.index = -1
            raise StopIteration()
        self.index = self.index + 1
        return self.__xaxis[self.index],self.__yaxis[self.index]

    def __str__(self):
        output = ""
        for k, x in enumerate(self.__xaxis):
            y = self.__yaxis[k];
            output = output + "(" + str(x)  + ", " + str(y) + ")\n"
        return output

    def __add__(self,other):
        oy = other.getYaxis()
        ny = []
        if len(oy) != len(self.__yaxis):
            raise Exception()
        for i in range(0,len(oy)):
            ny.append(self.__yaxis[i] + oy[i])
        return SpectrumData(self.__xaxis,ny)

    def __sub__(self,other):
        oy = other.getYaxis()
        ny = []
        if len(oy) != len(self.__yaxis):
            raise Exception()
        for i in range(0,len(oy)):
            ny.append(self.__yaxis[i] - oy[i])
        return SpectrumData(self.__xaxis,ny)

    def __mul__(self,other):
        if isinstance(other,float):
            ny = [x * other for x in self.__yaxis]
            return SpectrumData(self.__xaxis,ny)
        elif isinstance(other,SpectrumData):
            oy = other.getYaxis()
            ny = []
            if len(oy) != len(self.__yaxis):
                raise Exception()
            for i in range(0,len(oy)):
                ny.append(self.__yaxis[i] * oy[i])
            return SpectrumData(self.__xaxis,ny)
        else:
            raise Exception()

    def __rmul__(self,other):
        if isinstance(other,float):
            ny = [x * other for x in self.__yaxis]
            return SpectrumData(self.__xaxis,ny)
        elif isinstance(other,SpectrumData):
            oy = other.getYaxis()
            ny = []
            if len(oy) != len(self.__yaxis):
                raise Exception()
            for i in range(0,len(oy)):
                ny.append(self.__yaxis[i] * oy[i])
            return SpectrumData(self.__xaxis,ny)
        else:
            raise Exception()

    def __div__(self,other):
        if isinstance(other,float):
            ny = [x / other for x in self.__yaxis]
            return SpectrumData(self.__xaxis,ny)
        elif isinstance(other,SpectrumData):
            oy = other.getYaxis()
            ny = []
            if len(oy) != len(self.__yaxis):
                raise Exception()
            for i in range(0,len(oy)):
                if oy[i] == 0:
                    ny.append(0)
                else:
                    ny.append(self.__yaxis[i] / oy[i])
            return SpectrumData(self.__xaxis,ny)
        else:
            raise Exception()
        

    def __pow__(self,other):
        if isinstance(other,float):
            ny = [x ** other for x in self.__yaxis]
            return SpectrumData(self.__xaxis,ny)
        elif isinstance(other,SpectrumData):
            oy = other.getYaxis()
            ny = []
            if len(oy) != len(self.__yaxis):
                raise Exception()
            for i in range(0,len(oy)):
                ny.append(self.__yaxis[i] ** oy[i])
            return SpectrumData(self.__xaxis,ny)
        else:
            raise Exception()

    def get(self,i):
        return self.__xaxis[i],self.__yaxis[i]

    def formatImport(self,ios):
        self.__xaxis = []
        self.__yaxis = []
        ifile = open(ios,'r')
        content = ifile.readlines()
        for line in content:
            if line != 'SOF\n' and line != 'EOF\n':
                x = line.split('\t')[0]
                y = line.split('\t')[1]
                x = float(x)
                y = complex(y)
                self.append(x,y)

    def formatExport(self,path):
        ofile = open(path,'w')
        format_data = 'SOF\n'
        for i in range(0,len(self.__xaxis)):
            format_data = format_data + str(self.__xaxis[i]) + "\t" + str(self.__yaxis[i]) + '\n'
        format_data = format_data + 'EOF\n'
        ofile.write(format_data)

    def rotate(self,angle):
        tmpd = SpectrumData()
        angle_y = angle.getYaxis()
        for i in range(0,len(self.__xaxis)):
            tmpy = self.__yaxis[i] * np.exp(angle_y[i]*1j)
            tmpd.append(self.__xaxis[i],tmpy)
        return tmpd

    def reverse(self):
        return SpectrumData(self.__xaxis[::-1], self.__yaxis[::-1])

    def abs(self):
        return SpectrumData(self.__xaxis, np.abs(self.__yaxis))

    def extremum(self):
        if self.__yaxis[1] > self.__yaxis[0]:
            goup = 1
        else:
            goup = 0
        extremumData = SpectrumData()
        for i in range(1,len(self.__yaxis)):
            if self.__yaxis[i] > self.__yaxis[i-1] and goup == 0:
                goup = 1
            elif self.__yaxis[i] < self.__yaxis[i-1] and goup == 0:
                pass
            elif self.__yaxis[i] < self.__yaxis[i-1] and goup == 1:
                extremumData.append(self.__xaxis[i-1],self.__yaxis[i-1])
                goup = 0
            elif self.__yaxis[i] > self.__yaxis[i-1] and goup == 1:
                pass
        return extremumData

    def getHalf(self):
        pass

    def length(self):
        return len(self.__xaxis)

    def arg(self):
        tmpd = SpectrumData()
        realy = self.real().getYaxis()
        imagy = self.imag().getYaxis()
        for i in range(0,len(realy)):
            theta = np.arctan(imagy[i]/realy[i])
            tmpd.append(self.__xaxis[i],theta)
        return tmpd

    def real(self):
        return SpectrumData(self.__xaxis, [i.real for i in self.__yaxis])

    def imag(self):
        return SpectrumData(self.__xaxis, [i.imag for i in self.__yaxis])

    def getResolution(self):
        return len(self.__xaxis)

    def getXdomain(self):
        min = self.__xaxis[0];
        max = self.__xaxis[0];
        for v in self.__xaxis:
            if v < min:
                min = v
            if v > max:
                max = v
        return (min, max)

    def getXpos(self,index):
        return self.__xaxis[index]

    def slice(self, *args):
        if len(args) == 1:
            scale = args[0]
            domain = self.getXdomain()
            start = domain[0]
            end = domain[0] + (domain[1]-domain[0])*scale
            self.slice(start,end)
        elif len(args) == 2:
            start = args[0]
            end = args[1]
            left = -1;
            right = -1;
            for k,v in enumerate(self.__xaxis):
                if ((v >= start) and (left == -1)):
                    left = k
                if ((v >= end) and (right == -1)):
                    right = k
            self.__xaxis = self.__xaxis[left : right]
            self.__yaxis = self.__yaxis[left : right]
        else:
            raise Exception()

    def sliceTop(self,i):
        tmpy = sorted(self.__yaxis,reverse=1)
        remain = tmpy[:i]
        for k,v in enumerate(self.__yaxis):
            if not v in remain:
                self.__yaxis[k] = 'n'
                self.__xaxis[k] = 'n'
        self.__yaxis = [x for x in self.__yaxis if x != 'n']
        self.__xaxis = [x for x in self.__xaxis if x != 'n']

    def getAverage(self):
        sum = 0
        for v in self.__yaxis:
            sum += v
        return sum/len(self.__yaxis)

    def getMax(self):
        return max(self.__yaxis)

    def getMin(self):
        return min(self.__yaxis)

    def getXaxis(self):
        return self.__xaxis

    def getYaxis(self):
        return self.__yaxis

    def scaleX(self,v):
        self.__xaxis = [x*v for x in self.__xaxis]

    def reciprocalX(self):
        self.__xaxis = [1/x for x in self.__xaxis]
        self.__xaxis = self.__xaxis[::-1]
        self.__yaxis = self.__yaxis[::-1]

    def spline(self,x):
        y = itp.spline(self.__xaxis,self.__yaxis,x)
        self.__xaxis = x
        self.__yaxis = y

    def append(self,x,y):
        self.__xaxis.append(x)
        self.__yaxis.append(y)

