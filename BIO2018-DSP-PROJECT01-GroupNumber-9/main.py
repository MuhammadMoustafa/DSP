import equalizer
import os
import sys
import numpy as np
from scipy.io.wavfile import read
from scipy.io.wavfile import write
#from scikits.audiolab import wavread
from scipy.signal import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
from PyQt4 import QtGui, QtCore
from _io import open
import wave


class DemoApp(QtGui.QMainWindow, equalizer.Ui_MainWindow):
    def __init__(self):
        super(DemoApp, self).__init__()
        self.setupUi(self)
        self.plotSignalBtn.clicked.connect(self.plotSignal)
        self.fftBtn.clicked.connect(self.plotFft)
        self.browseBtn.clicked.connect(self.browseWavFile)
        self.AddFreqBtn.clicked.connect(self.addFreq)
        self.generateFreqBtn.clicked.connect(self.generateFreq)
        self.equalizerSlider1.sliderReleased.connect(self.valuechange)
        self.equalizerSlider2.sliderReleased.connect(self.valuechange2)
        self.equalizerSlider3.sliderReleased.connect(self.valuechange3)
        self.equalizerSlider4.sliderReleased.connect(self.valuechange4)
        self.equalizerSlider5.sliderReleased.connect(self.valuechange5)
        self.equalizerSlider6.sliderReleased.connect(self.valuechange6)
        self.equalizerSlider7.sliderReleased.connect(self.valuechange7)
        self.equalizerSlider8.sliderReleased.connect(self.valuechange8)
        self.equalizerSlider9.sliderReleased.connect(self.valuechange9)
        self.equalizerSlider10.sliderReleased.connect(self.valuechange10)
        self.clearWorkspaceBtn.clicked.connect(self.clearWorkspace)
        self.addedFreq=[]
        self.sf=44100.0


    def plotSignal(self):
        signal = self.audio
        n = len(signal)  # length of the signal
        Fs = self.sf;  # sampling rate
        Ts = 1.0 / Fs;  # sampling interval
        timeLength = n / Fs
        time = np.arange(0, timeLength, Ts)  # time vector
        fig1 = Figure()
        fig1.patch.set_facecolor('white')
        ax1f1 = fig1.add_subplot(111)
        ax1f1.plot(time, signal)
        self.clearLayout(self.signalPlotLayout)
        self.canvas = FigureCanvas(fig1)
        self.signalPlotLayout.addWidget(self.canvas)
        self.saveBtn.clicked.connect(self.save)
        self.canvas.draw()
    def plotFft (self):

        n = len(self.fourier)  # length of the signal
        Fs = self.sf;  # sampling rate
        Ts = 1.0 / Fs;  # sampling interval
        timeLength = n/Fs
        t = np.arange(0, timeLength, Ts)  # time vector
        k = np.arange(n)
        T = n / Fs
        frq = k / T  # two sides frequency range
        if (self.radianRadio.isChecked()):
            frq = frq[range(n / 2)] / (self.sf * 0.5)  # one side frequency range
        else :
            frq = frq[range(n / 2)] # one side frequency range

        Y = self.fourier/n   # fft computing and normalization
        Y = Y[range(n / 2)]

        fig1 = Figure()
        fig1.patch.set_facecolor('white')
        ax1f1 = fig1.add_subplot(111)
        if(self.hzRadio.isChecked()):
            ax1f1.set_xscale('log')
        ax1f1.plot(frq, np.abs(Y))
        self.clearLayout(self.fourierPlotLayout)
        self.canvas = FigureCanvas(fig1)
        self.fourierPlotLayout.addWidget(self.canvas)
        self.canvas.draw()

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QtGui.QWidgetItem):
                print "widget" + str(item)
                item.widget().close()
                # or
                # item.widget().setParent(None)
            elif isinstance(item, QtGui.QSpacerItem):
                print "spacer " + str(item)
                # no need to do extra stuff
            else:
                print "layout " + str(item)
                self.clearLayout(item.layout())

            # remove the item from layout
            layout.removeItem(item)


    def browseWavFile(self):
        filePath = QtGui.QFileDialog.getOpenFileName(self,'Single File', "~/","*.wav")
        self.sf , self.audioOriginal = read(filePath)
        self.sf = float(self.sf)
        self.audioOriginal = self.audioOriginal[:,0]
        self.audio = self.audioOriginal.copy()
        self.fourier = np.fft.fft(self.audioOriginal)
        self.fourierOriginal = np.fft.fft(self.audioOriginal)
        self.plotSignal()
        self.plotFft()
    def addFreq(self):
        f=float(self.addFreqTxtBox.text())
        if (self.radianRadio.isChecked()):
            f = self.sf * 0.5 * f

        self.addedFreq.append(f)

    def generateFreq(self):
        signalLength=3
        self.addedFreq.sort(reverse=True)
        self.sf = 44100
        step = 1.0/self.sf
        self.audio =np.zeros(int(signalLength*self.sf))
        time = np.arange(0, signalLength,step)
        for freq in self.addedFreq :
            signal = np.sin(time * 2 * np.pi * freq)
            self.audio = self.audio + signal
        self.audioOriginal=self.audio.copy()
        self.fourier = np.fft.fft(self.audio)
        self.fourierOriginal = np.fft.fft(self.audioOriginal)


    def clearWorkspace(self):
        self.audio = np.zeros(self.sf)
        self.addedFreq=[]
        self.clearLayout(self.signalPlotLayout)
        self.clearLayout(self.fourierPlotLayout)
        self.equalizerSlider1.setValue(30)
        self.equalizerSlider2.setValue(30)
        self.equalizerSlider3.setValue(30)
        self.equalizerSlider4.setValue(30)
        self.equalizerSlider5.setValue(30)
        self.equalizerSlider6.setValue(30)
        self.equalizerSlider7.setValue(30)
        self.equalizerSlider8.setValue(30)
        self.equalizerSlider9.setValue(30)
        self.equalizerSlider10.setValue(30)









    def save(self):
        write("generated.wav",self.sf,self.audio)








    def valuechange(self) :
        db = self.equalizerSlider1.value()-30
        step= len(self.fourier)/20

        self.fourier[0:step]=self.fourierOriginal[0:step]*10**(db/10.0)
        self.audio = np.fft.ifft(self.fourier)
        self.plotFft()
        self.plotSignal()


    def valuechange2(self) :
        db = self.equalizerSlider2.value() - 30
        step = len(self.fourier) / 20

        self.fourier[step*1:step*2] = self.fourierOriginal[step*1:step*2] * 10 ** (db / 10.0)
        self.audio = np.fft.ifft(self.fourier)
        self.plotFft()
        self.plotSignal()


    def valuechange3(self) :
        db = self.equalizerSlider3.value() - 30
        step = len(self.fourier) / 20
        self.fourier[step * 2:step * 3] = self.fourierOriginal[step * 2:step * 3] * 10 ** (db / 10.0)
        self.audio = np.fft.ifft(self.fourier)
        self.plotFft()
        self.plotSignal()


       
    def valuechange4(self) :
        db = self.equalizerSlider4.value() - 30
        step = len(self.fourier) / 20
        self.fourier[step * 3:step * 4] = self.fourierOriginal[step * 3:step * 4] * 10 ** (db / 10.0)
        self.audio = np.fft.ifft(self.fourier)
        self.plotFft()
        self.plotSignal()


    def valuechange5(self) :
        db = self.equalizerSlider5.value() - 30
        step = len(self.fourier) / 20
        self.fourier[step * 4:step * 5] = self.fourierOriginal[step * 4:step * 5] * 10 ** (db / 10.0)
        self.audio = np.fft.ifft(self.fourier)
        self.plotFft()
        self.plotSignal()



    def valuechange6(self) :
        db = self.equalizerSlider6.value() - 30
        step = len(self.fourier) / 20
        self.fourier[step * 5:step * 6] = self.fourierOriginal[step * 5:step * 6] * 10 ** (db / 10.0)
        self.audio = np.fft.ifft(self.fourier)
        self.plotFft()
        self.plotSignal()



    def valuechange7(self) :
        db = self.equalizerSlider7.value() - 30
        step = len(self.fourier) / 20
        self.fourier[step * 6:step * 7] = self.fourierOriginal[step * 6:step * 7] * 10 ** (db / 10.0)
        self.audio = np.fft.ifft(self.fourier)
        self.plotFft()
        self.plotSignal()



    def valuechange8(self) :
        db = self.equalizerSlider8.value() - 30
        step = len(self.fourier) / 20
        self.fourier[step * 7:step * 8] = self.fourierOriginal[step * 7:step * 8] * 10 ** (db / 10.0)
        self.audio = np.fft.ifft(self.fourier)
        self.plotFft()
        self.plotSignal()



    def valuechange9(self) :
        db = self.equalizerSlider9.value() - 30
        step = len(self.fourier) / 20
        self.fourier[step * 8:step * 9] = self.fourierOriginal[step * 8:step * 9] * 10 ** (db / 10.0)
        self.audio = np.fft.ifft(self.fourier)
        self.plotFft()
        self.plotSignal()



    def valuechange10(self) :
        db = self.equalizerSlider10.value() - 30
        step = len(self.fourier) / 20
        self.fourier[step * 9:step * 10] = self.fourierOriginal[step * 9:step * 10] * 10 ** (db / 10.0)
        self.audio = np.fft.ifft(self.fourier)
        self.plotFft()
        self.plotSignal()




def main():
    App = QtGui.QApplication(sys.argv)
    form = DemoApp()
    form.show()
    App.exec_()


if __name__ == '__main__':
    main()
