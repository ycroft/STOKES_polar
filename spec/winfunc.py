import numpy as np
import df

def window(data, start, end, win):
	x = data.getXaxis()
	y = data.getYaxis()
	domain = data.getXdomain()
	left = -1;
	right = -1;
	for k,v in enumerate(x):
		if ((v >= start) and (left == -1)):
			left = k
		if ((v >= end) and (right == -1)):
			right = k
	if left == 0:
		left = int(-(right/(end-domain[0]))*(domain[0]-start))
	if right == -1:
		right = len(x) + int(((len(x)-left)/(domain[1]-start))*(end-domain[1]))
	N = right - left
	n = np.linspace(0,N-1,N)
	w = win(n,N)
	hany = np.complex64(np.linspace(0,0,len(x)))
	if right > len(x):
		for i in range(left, len(x)):
			if i >=0:
				hany[i] = y[i] * w[i-left]
		return df.SpectrumData(x, hany)
	else:
		for i in range(left, right):
			if i >=0:
				hany[i] = y[i] * w[i-left]
		return df.SpectrumData(x, hany)

def rect(data,start,end):
	return window(data,start,end,lambda n,N: np.linspace(1,1,N) )

def hanning(data,start,end):
	return window(data,start,end,lambda n,N: 0.5*(1-np.cos((2*np.pi*n)/(N-1))) )

def hamming(data,start,end):
	return window(data,start,end,lambda n,N: 0.54-0.46*np.cos(2*np.pi*n/(N-1)) )

def blackman(data,start,end):
	return window(data,start,end,lambda n,N: 0.42-0.5*np.cos(2*np.pi*n/(N-1))+0.08*np.cos(4*np.pi*n/(N-1)))