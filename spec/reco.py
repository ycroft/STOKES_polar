# encoding: utf-8

import df
import winfunc

class Feature(object):
	# this works only when starting at area A or C
	# a lot of datagram testing to be done
	def __init__(self,data):
		self.__data = data
		self.__y = data.getYaxis()
		self.__x = data.getXaxis()
		self.__state = ['','','']
		self.__boundaries = df.SpectrumData()
		self.__mount = -1
		self.__cracked = 0
		self.__peaky = 0
		self.__peakx = 0
		self.__peaks = df.SpectrumData()
		self.__lAB = 2*data.getAverage() - data.getMin()
		self.__lBC = data.getAverage()

	def __pushState(self,st):
		for i in range(0,len(self.__state)-1):
			self.__state[i] = self.__state[i+1]
		self.__state[-1] = st

	def __initState(self):
		if self.__y[0] > self.__lAB:
			self.__state = ['','','A']
			self.__mount = 1
			self.__peaky = self.__y[0]
		elif self.__y[0] > self.__lBC:
			raise Exception()
		else:
			self.__state = ['','','C']
			self.__mount = 0

	def __updateState(self,i):
		if self.__y[i] > self.__lAB:
			st = 'A'
		elif self.__y[i] > self.__lBC:
			st = 'B'
		else:
			st = 'C'
		if self.__state[-1] != st:
			self.__pushState(st)

	def __trigger(self,i):
		x = self.__state[0]
		y = self.__state[1]
		z = self.__state[2]
		m = self.__mount
		if self.__y[i] > self.__peaky:
			self.__peaky = self.__y[i]
			self.__peakx = self.__x[i]
		if x=='A' and y=='B' and z=='C' and m==1 :
			self.__boundaries.append(self.__x[i],self.__y[i])
			self.__peaks.append(self.__peakx,self.__peaky)
			self.__mount = 0
		elif y=='A' and z=='C' and m==1:
			self.__boundaries.append(self.__x[i],self.__y[i])
			self.__peaks.append(self.__peakx,self.__peaky)
			self.__mount = 0
		elif x=='C' and y=='B' and z=='A' and m==0:
			self.__boundaries.append(self.__x[i-2],self.__y[i-2])
			self.__peaky = self.__y[i]
			self.__peakx = self.__x[i]
			self.__mount = 1
		elif y=='C' and z=='A' and m==0:
			self.__boundaries.append(self.__x[i-1],self.__y[i-1])
			self.__peaky = self.__y[i]
			self.__peakx = self.__x[i]
			self.__mount = 1
		if i == len(self.__y)-1 and z=='A':
			self.__peaks.append(self.__peakx,self.__peaky)

	def start(self,require=-1):
		self.__initState()
		for i in range(1,len(self.__y)):
			self.__updateState(i)
			self.__trigger(i)
		if require != -1:
			self.__peaks.sliceTop(require)

	def getWindows(self,rx=0.5):
		tmpx = self.__peaks.getXaxis()
		windows = []
		for i in range(0,len(tmpx)):
			if i == 0:
				rd = (tmpx[i+1]-tmpx[i]) * rx
				windows.append([tmpx[i]-rd,tmpx[i]+rd])
			elif i == len(tmpx)-1:
				ld = (tmpx[i]-tmpx[i-1]) * rx
				windows.append([tmpx[i]-ld,tmpx[i]+ld])
			else:
				rd = (tmpx[i+1]-tmpx[i]) * rx
				ld = (tmpx[i]-tmpx[i-1]) * rx
				if ld < rd:
					windows.append([tmpx[i]-ld,tmpx[i]+ld])
				else:
					windows.append([tmpx[i]-rd,tmpx[i]+rd])
		
		# domain = self.__data.getXdomain()
		# rid = self.__boundaries.length();
		# windows.append([domain[0] - self.__boundaries.get(0)[0],self.__boundaries.get(0)[0]])
		# for i in range(1,self.__boundaries.length()-1):
		# 	if i % 2 == 0:
		# 		windows.append([self.__boundaries.get(i-1)[0],self.__boundaries.get(i)[0]])
		# windows.append([self.__boundaries.get(rid-1)[0],2*domain[1]-self.__boundaries.get(rid-1)[0]])

		# log positions:
		# self.getPeaks()
		# for k,v in enumerate(windows):
		# 	print '第',k+1,'个窗函数位置（左边界，右边界）:',v
		return windows

	def getPeaks(self):
		# log messages:
		print '一共找到',self.__peaks.length(),'个峰'
		tmpx = self.__peaks.getXaxis()
		for k,v in enumerate(tmpx):
			print '第',k+1,'个峰位置:',v
		# end log
		return self.__peaks

	def getBoundaries(self):
		return self.__boundaries

	def getlAB(self):
		return df.SpectrumData(self.__x,[self.__lAB,]*len(self.__x))

	def getlBC(self):
		return df.SpectrumData(self.__x,[self.__lBC,]*len(self.__x))

def filter(windows,rdata):
	ffti = []
	for v in windows:
		func = winfunc.hanning(rdata,v[0],v[1])
		ffti.append(func)
	return ffti
