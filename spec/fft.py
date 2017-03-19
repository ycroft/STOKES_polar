import numpy as np
import scipy.interpolate as itp
import df
from winfunc import *

def fft(data, N, **args):
    if 'abs' in args:
        absa = args['abs']
    else:
        absa = 0
    if 'window' in args:
        window = args['window']
        win = eval(window)
        domain = data.getXdomain()
        data = win(data, domain[0],domain[1])

    domain = data.getXdomain()
    if N == -1:
        y = data.getYaxis()
        N = len(y)
    else:
        t = np.linspace(domain[0],domain[1],N)
        y = itp.spline(np.array(data.getXaxis()),np.array(data.getYaxis()),t)
    n = np.linspace(0,N-1,N)
    fft_y = np.fft.fft(y)
    if absa:
        fft_y = np.abs(fft_y)
    scale = N/(domain[1]-domain[0])
    fft_x = n * scale / N
    return df.SpectrumData(fft_x, fft_y)

def ifft(data,rdomain , N):
    y = data.getYaxis()
    iy = np.fft.ifft(y)
    if N == -1:
        N = len(y)
    return df.SpectrumData(np.linspace(rdomain[0],rdomain[1],N),iy)

