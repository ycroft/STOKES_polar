import spec

def testReco():
	data = spec.df.SpectrumData()
	# data.formatImport('/home/ycroft/tmp/twd/valid/stokes_vector_2.out')
	data.formatImport('/home/ycroft/tmp/twd/valid/mf_2.out')
	sdata = spec.df.SpectrumData('./spec_data/refer.sd')
	sdata.scaleX(1E-7)
	sdata.reciprocalX()
	sdomain = sdata.getXdomain()
	sfft = spec.fft.fft(sdata,1024).abs()
	yaxis = sfft.getYaxis()
	sfdomain = sfft.getXdomain()

	s = 0
	m = yaxis[0]
	for x in yaxis:
		s += x
		if(x < m):
			m = x
	aver = s/len(yaxis)

	print aver, m;
	lu = spec.df.SpectrumData();
	lu.append(sfdomain[0], aver);
	lu.append(sfdomain[1], aver);
	lv = spec.df.SpectrumData();
	lv.append(sfdomain[0], 2*aver-m);
	lv.append(sfdomain[1], 2*aver-m);

	# checkfft = sfft.abs()
	# sfeature = spec.reco.Feature(checkfft)
	# sfeature.start(8)
	# swindows = sfeature.getWindows()
	# sboundaries = sfeature.getBoundaries()
	# sffti = spec.reco.filter(swindows,sfft)

	# for i in range(0,sboundaries.length()):
	# 	if (int)(i) % 2 == 0 and i != 0:
	# 		print (sboundaries.get(i)[0]+sboundaries.get(i-1)[0])/2,i
	# for x,y in swindows:
	# 	print (x+y)/2
	# print("====")
	# print(swindows)

	dg = spec.plot.Datagram({
		'title' : 'RECO test',
		'xlabel': ' ',
		'ylabel': ' ',
		'grid' : True
	});
	style_0 = {
		'color' : 'r',
		'label' : 'fft',
		'linewidth' : 1,
		'linestyle' : '-',
		'marker' : '.'
	}
	style_1 = {
		'color' : 'y',
		'label' : 'fft',
		'linewidth' : 1,
		'linestyle' : '-'
	}
	style_2 = {
		'color' : 'b',
		'label' : 'fft',
		'linewidth' : 1,
		'linestyle' : '-'
	}
	style_3 = {
		'color' : 'g',
		'label' : 'fft',
		'linewidth' : 1,
		'linestyle' : '-'
	}
	style_yellow_dot = {
		'color' : 'y',
		'marker': 'o',
		'label' : 'boundaries',
		'linewidth': 1,
		'linestyle' : '--'
	}
	# dg.add(data,style_0);
	# dg.add(sffti[0],style_0);
	# dg.add(sffti[1],style_1);
	# dg.add(sffti[2],style_2);
	# dg.add(sffti[3],style_3);
	dg.add(sfft,style_3);
	dg.add(lu,style_0);
	dg.add(lv,style_2);
	dg.show()

if __name__ == "__main__":
	testReco()