# -*- coding: utf-8 -*-
import reportlab.lib.fonts
from datetime import datetime
from reportlab.pdfgen.canvas import Canvas  
from reportlab.lib.units import inch

class Reporter(object):
	def __init__(self,vapp):
		self.dataApp = vapp
		path = self.dataApp.repoPath + self.dataApp.rdataName + '.pdf'
		self.canvas = Canvas(path)
		self.page = 1

	def header(self):
		self.canvas.setFont("Helvetica", 10)  
		self.canvas.drawCentredString(4.135*inch, 10.74*inch, 'Copyright@2015 : ycroft.net')  
		self.canvas.setFont("Helvetica", 11.5)
		self.canvas.line(1*inch, 10.69*inch, 7.27*inch, 10.69*inch) 

	def footer(self):
		self.canvas.setFont("Helvetica", 11.5)
		self.canvas.line(1*inch, 1*inch, 7.27*inch, 1*inch)
		self.canvas.setFont("Helvetica", 10)  
		self.canvas.drawCentredString(4.135*inch, 0.83*inch, '- '+str(self.page)+' -')

	def cover(self,coverInfo):
		dataName = coverInfo.get('dataName','no name')
		author = coverInfo.get('author','no name')
		version = coverInfo.get('version','unknown')
		self.header()
		self.footer()
		self.canvas.setFont("Helvetica-Bold", 40)
		self.canvas.drawCentredString(4.135*inch, 7.5*inch, 'Analysis Report')
		self.canvas.setFont("Helvetica", 20)
		self.canvas.drawCentredString(4.135*inch, 6.8*inch, 'for data \'' + dataName + '\'')

		self.canvas.setFont("Helvetica", 15)
		self.canvas.drawRightString(3.935*inch, 4.4*inch, 'author:')
		self.canvas.drawRightString(3.935*inch, 3.9*inch, 'date:')
		self.canvas.drawRightString(3.935*inch, 3.4*inch, 'version:')
		self.canvas.drawString(4.335*inch, 4.4*inch, author)
		self.canvas.drawString(4.335*inch, 3.9*inch, str(datetime.now().strftime('%a, %b %d %H:%M')))
		self.canvas.drawString(4.335*inch, 3.4*inch, version)
		self.canvas.showPage()
		self.page += 1

	def body(self):
		self.header()
		self.footer()
		sdataName = self.dataApp.sdataName
		rdataName = self.dataApp.rdataName
		imgPath = './spec_data/img/'
		self.canvas.setFont("Helvetica-Bold", 15)
		self.canvas.drawString(1.25*inch, 10*inch, 'I. Modulation Factors ')
		self.canvas.setFont("Helvetica", 12)
		self.canvas.drawString(1.5*inch, 9.7*inch, 'These factors are derived from the file \''+sdataName+'\'')
		self.canvas.drawInlineImage(imgPath + sdataName + '_cs0.jpg',1.25*inch,5.3*inch,5.77*inch,4.33*inch)
		self.canvas.drawInlineImage(imgPath + sdataName + '_cs1.jpg',1.25*inch,1.2*inch,5.77*inch,4.33*inch)
		self.canvas.showPage()
		self.page += 1
		self.header()
		self.footer()
		self.canvas.drawInlineImage(imgPath + sdataName + '_cs2.jpg',1.25*inch,5.3*inch,5.77*inch,4.33*inch)
		self.canvas.drawInlineImage(imgPath + sdataName + '_cs3.jpg',1.25*inch,1.2*inch,5.77*inch,4.33*inch)
		self.canvas.showPage()
		self.page += 1
		self.header()
		self.footer()
		self.canvas.setFont("Helvetica-Bold", 15)
		self.canvas.drawString(1.25*inch, 10*inch, 'II. Measured Data & FFT ')
		self.canvas.setFont("Helvetica", 12)
		self.canvas.drawString(1.5*inch, 9.7*inch, 'The data is derived from the file \''+rdataName+'\', and each fft channel has been filtered.')
		self.canvas.drawInlineImage(imgPath + rdataName + '_rd.jpg',1.25*inch,5.3*inch,5.77*inch,4.33*inch)
		self.canvas.drawInlineImage(imgPath + rdataName + '_fft.jpg',1.25*inch,1.2*inch,5.77*inch,4.33*inch)
		self.canvas.showPage()
		self.page += 1
		self.header()
		self.footer()
		self.canvas.setFont("Helvetica-Bold", 15)
		self.canvas.drawString(1.25*inch, 10*inch, 'III. Modulation Signals ')
		self.canvas.setFont("Helvetica", 12)
		self.canvas.drawString(1.5*inch, 9.7*inch, 'These signals are derived by ifft on the corresponding channel.')
		self.canvas.drawInlineImage(imgPath + rdataName + '_fa0.jpg',1.25*inch,5.3*inch,5.77*inch,4.33*inch)
		self.canvas.drawInlineImage(imgPath + rdataName + '_fa1.jpg',1.25*inch,1.2*inch,5.77*inch,4.33*inch)
		self.canvas.showPage()
		self.page += 1
		self.header()
		self.footer()
		self.canvas.drawInlineImage(imgPath + rdataName + '_fa2.jpg',1.25*inch,5.3*inch,5.77*inch,4.33*inch)
		self.canvas.drawInlineImage(imgPath + rdataName + '_fa3.jpg',1.25*inch,1.2*inch,5.77*inch,4.33*inch)
		self.canvas.showPage()
		self.page += 1
		self.header()
		self.footer()
		self.canvas.setFont("Helvetica-Bold", 15)
		self.canvas.drawString(1.25*inch, 10*inch, 'IV. Stokes Vectors ')
		self.canvas.setFont("Helvetica", 12)
		self.canvas.drawString(1.5*inch, 9.7*inch, 'This can be figured out using modulation signals and modulation factors.')
		self.canvas.drawInlineImage(imgPath + rdataName + '_s0.jpg',1.25*inch,5.3*inch,5.77*inch,4.33*inch)
		self.canvas.drawInlineImage(imgPath + rdataName + '_s1.jpg',1.25*inch,1.2*inch,5.77*inch,4.33*inch)
		self.canvas.showPage()
		self.page += 1
		self.header()
		self.footer()
		self.canvas.drawInlineImage(imgPath + rdataName + '_s2.jpg',1.25*inch,5.3*inch,5.77*inch,4.33*inch)
		self.canvas.drawInlineImage(imgPath + rdataName + '_s3.jpg',1.25*inch,1.2*inch,5.77*inch,4.33*inch)
		self.canvas.showPage()
		self.page += 1
		self.header()
		self.footer()
		self.canvas.setFont("Helvetica-Bold", 15)
		self.canvas.drawString(1.25*inch, 10*inch, 'IV. Degree of Polarization ')
		self.canvas.setFont("Helvetica", 12)
		self.canvas.drawString(1.5*inch, 9.7*inch, 'This was figured out using four Stokes vectors.')
		self.canvas.drawInlineImage(imgPath + rdataName + '_dop.jpg',1.25*inch,5.3*inch,5.77*inch,4.33*inch)
		self.canvas.showPage()
		self.page += 1
		self.header()
		self.footer()
		windows = self.dataApp.windows
		self.canvas.setFont("Helvetica-Bold", 15)
		self.canvas.drawString(1.25*inch, 10*inch, 'V. Data Analysis ')
		self.canvas.setFont("Helvetica", 12)
		self.canvas.drawString(1.5*inch, 9.7*inch, 'This was automatically generated by program.')
		self.canvas.drawString(1.5*inch, 9.0*inch, '-The number of the peaks recognized in `FFT` datagram:')
		self.canvas.drawString(2.0*inch, 8.7*inch, str(len(windows)) + ' peaks')
		self.canvas.drawString(1.5*inch, 8.4*inch, '-The range of the peaks recognized in `FFT` datagram:')
		for i in range(0,len(windows)):
			self.canvas.drawString(2.0*inch, (8.1-i*0.3)*inch, '[' + str(i)+ ']   ' +str(windows[i][0]))
			self.canvas.drawString(3.9*inch, (8.1-i*0.3)*inch, '~   ' + str(windows[i][1]))
		self.canvas.showPage()
		self.page += 1


	def gen(self):
		self.cover({
			'dataName' : self.dataApp.rdataName + '`C spec',
			'author' : 'ycroft',
			'version' : 'v0.1'
		})
		self.body()
		self.canvas.save()

if __name__ == "__main__":
	reporter = Reporter('report.pdf')
	reporter.gen()
