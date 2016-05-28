import spec
import time

if __name__ == '__main__':
	data = spec.df.SpectrumData('./spec_data/60.rd')
	data.reciprocalX()
	domain = data.getXdomain()
	fft = spec.fft.fft(data,1024)
	fft = spec.fft.ifft(fft,domain,1024)
	dg = spec.plot.Datagram({
		'title' : ' ',
		'grid' : True
	})
	style = {
		'color' : 'k',
		'label' : 'test data',
		'linewidth' : '1',
		'linestyle' : '-'
	}
	style1 = {
		'color' : 'r',
		'label' : 'test dataq',
		'linewidth' : '1',
		'linestyle' : '-'
	}
	dg.add(fft,style)
	dg.add(data,style1)
	dg.show()
