import mygui
import os
import sys
import numpy as np
import thread
from scipy.io.wavfile import read
import scipy.signal as sc
from scipy.ndimage import fourier
from scipy.signal import butter
from scipy.signal import lfilter
from scipy.io.wavfile import write
import sounddevice as sd
# from scikits.audiolab import wavread
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
import pyglet


class DemoApp(QtGui.QMainWindow, mygui.Ui_MainWindow):
    def __init__(self):
        super(DemoApp, self).__init__()
        self.setupUi(self)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.browseBtn.clicked.connect(self.browseWavFile)
        self.playBtn.clicked.connect(self.playSound)
        self.plotBtn.clicked.connect(self.plotAll)



    def plotAll(self):

        filterType = "lowpass"  ##default
        if (self.highpassRadio.isChecked()):
            filterType = "highpass"
        cornerFreq = float(self.cornerFreq.text())
        self.b, self.a = butter(4, cornerFreq,filterType)
        self.fourierPLot()
        self.filterResponsePlot()
        self.onlineFilter()






    def browseWavFile(self):
        self.filePath = QtGui.QFileDialog.getOpenFileName(self, 'Single File', "~/", "*.wav")
        self.sf, self.audioOriginal = read(self.filePath)
        self.audioOriginal = self.audioOriginal[:,0]
        self.sf = float(self.sf)
        thread.start_new_thread(self.fourierTrans, ("thread-1",))
        self.l = len(self.audioOriginal)

    def fourierTrans(self, threadName):
        self.fourierOriginal = np.fft.fft(self.audioOriginal)/len(self.audioOriginal)


    def filterResponsePlot(self):
        # num,dom = butter(4, .1, 'lowpass')
        b=self.b
        a=self.a
        frq, h = sc.freqz(b, a)
        frq = frq/np.pi

        n = len(h)  # length of the signal

        Y = h / float(n)  # fft computing and normalization

        fig1 = Figure()
        fig1.patch.set_facecolor('white')
        ax1f1 = fig1.add_subplot(111)
        ax1f1.plot(frq, np.abs(Y))
        self.clearLayout(self.filterMagnitudeLayout)
        self.canvas = FigureCanvas(fig1)
        self.filterMagnitudeLayout.addWidget(self.canvas)

        # self.saveBtn.clicked.connect(self.save)
        self.canvas.draw()

        ##
        fig2 = Figure()
        fig2.patch.set_facecolor('white')
        ax1f1 = fig2.add_subplot(111)
        ax1f1.plot(frq, np.angle(Y))
        self.clearLayout(self.filterPhaseLayout)
        self.canvas = FigureCanvas(fig2)
        self.filterPhaseLayout.addWidget(self.canvas)
        self.canvas.draw()









    def playSound(self):
        sd.play(self.filteredSignal,self.sf)



    def digitalFilter(self,b,a, signal):
        ## this functin takes signal and transfer function coeffecients, and return the filtered signal
        length = len(signal)
        y = np.zeros(length)

        a = a / a[0]
        b = b / a[0]
        ##cycling over all the samples , for every sample accumelate the terms of coeefecients a and b
        for i in range(0,length):
            for j in range(1,len(a)):
                if (i - j > 0):

                    y[i] = y[i] - y[i-j] * a[j]
            for j in range(0,len(b)):
                if (i - j > 0):
                    y[i] = y[i] + signal[i]*b[j]



        return y/len(y)


    def fourierPLot(self):
        fourier = np.fft.fft(self.audioOriginal)/len(self.audioOriginal)
        n = len(fourier)  # length of the signal
        k = np.arange(n)
        T = n / self.sf
        frq = k / T  # two sides frequency range



        frq = frq[range(n / 2)] / (self.sf * 0.5)  # one side frequency range
        Y = fourier
        Y = Y[range(n / 2)]



        fig1 = Figure()
        fig1.patch.set_facecolor('white')
        ax1f1 = fig1.add_subplot(111)
        ax1f1.plot(frq, np.abs(Y))
        self.clearLayout(self.offlineMagnitudeLayout)
        self.canvas = FigureCanvas(fig1)
        self.offlineMagnitudeLayout.addWidget(self.canvas)

        self.canvas.draw()

        ##
        fig2 = Figure()
        fig2.patch.set_facecolor('white')
        ax1f1 = fig2.add_subplot(111)
        ax1f1.plot(frq, np.angle(Y))
        self.clearLayout(self.offlinePhaseLayout)
        self.canvas = FigureCanvas(fig2)
        self.offlinePhaseLayout.addWidget(self.canvas)

        # self.saveBtn.clicked.connect(self.save)
        self.canvas.draw()



    def onlineFilter(self):
        b=self.b
        a=self.a


        self.filteredSignal = self.digitalFilter(b,a,self.audioOriginal)

        fourier = np.fft.fft(self.filteredSignal)
        n = len(fourier)
        k = np.arange(n)
        T = n / self.sf
        frq = k / T  # two sides frequency range

        frq = frq[range(n / 2)] / (self.sf * 0.5)  # one side frequency range
        Y = fourier
        Y = Y[range(n / 2)]

        fig1 = Figure()
        fig1.patch.set_facecolor('white')
        ax1f1 = fig1.add_subplot(111)
        ax1f1.plot(frq, np.abs(Y))
        self.clearLayout(self.onlineMagnitudeLayout)
        self.canvas = FigureCanvas(fig1)
        self.onlineMagnitudeLayout.addWidget(self.canvas)

        # self.saveBtn.clicked.connect(self.save)
        self.canvas.draw()

        ##
        fig2 = Figure()
        fig2.patch.set_facecolor('white')
        ax1f1 = fig2.add_subplot(111)
        ax1f1.plot(frq, np.angle(Y))
        self.clearLayout(self.onlinePhaseLayout)
        self.canvas = FigureCanvas(fig2)
        self.onlinePhaseLayout.addWidget(self.canvas)

        # self.saveBtn.clicked.connect(self.save)
        self.canvas.draw()
        #################







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








def main():
    App = QtGui.QApplication(sys.argv)
    form = DemoApp()
    form.show()
    App.exec_()


if __name__ == '__main__':
    main()