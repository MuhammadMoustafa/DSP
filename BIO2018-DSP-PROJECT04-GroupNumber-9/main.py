import gui
import threading
import time
import serial
import numpy as np
import thread
import pyaudio
import sys
import matplotlib.pyplot as plt
from drawnow import *
from scipy.io.wavfile import read
from scipy.io.wavfile import write
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
from PyQt4 import QtGui, QtCore
ser = serial.Serial('com6', 9600)  # Establish the connection on a specific port

class DemoApp(QtGui.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super(DemoApp, self).__init__()
        self.setupUi(self)
        self.browseBtn.clicked.connect(self.browseWavFile)
        self.saveBtn.clicked.connect(self.save)
        self.recordBeforeBtn.clicked.connect(self.recordBefore)
        self.recordAfterBtn.clicked.connect(self.recordAfter)
        self.counter = 0
        self.ydata = [0]
        self.xdata=[0]
        self.xRange = np.linspace(0, 2, num=512)
        self.xRange = self.xRange.tolist()


        thread.start_new_thread(self.stream, ("thread-1",))
    def stream(self, threadName):

        while (self.counter < 512):
            print self.counter
            dataArray = ser.readline().split(",")
            dataX = float(dataArray[0])
            self.xdata.append(dataX)
            dataY = float(dataArray[1])
            self.ydata.append(dataY)
            self.counter += 1


        QtCore.QTimer.singleShot(0, self.plotFourier)
        QtCore.QTimer.singleShot(0, self.plotSignal)
        while(1):
            dataArray = ser.readline().split(",")
            dataX = float(dataArray[0])
            self.xdata.append(dataX)
            dataY = float(dataArray[1])
            self.ydata.append(dataY)
            self.counter += 1
            print self.counter
            QtCore.QTimer.singleShot(0, self.plotSignal)
            if ((self.counter % 512)==0):
                QtCore.QTimer.singleShot(0,self.plotFourier)






            # i+=1
            # if(i==512):
            #     QtCore.QTimer.singleShot(0, self.clear)
            #     i=0



                # self.ydata[self.counter]=300
    def plotSignal(self):
        self.signalBefore.plotItem.clear()
        self.signalPlot = self.signalBefore.plotItem.plot(pen='y')
        self.signalPlot.setData(self.xdata[self.counter-512:self.counter])
        self.signalAfter.plotItem.clear()
        self.signalPlot = self.signalAfter.plotItem.plot(pen='y')
        self.signalPlot.setData(self.ydata[self.counter - 512:self.counter])

    def plotFourier(self):
        self.freqMagBefore.plotItem.clear()
        fourierMag = self.freqMagBefore.plotItem.plot(pen='y')
        self.freqPhaseBefore.plotItem.clear()
        fourierPhase = self.freqPhaseBefore.plotItem.plot(pen='y')

        fourier = np.fft.fft(self.xdata[self.counter-512:self.counter])
        fourierMag.setData(np.abs(fourier),x = self.xRange)
        fourierPhase.setData(np.angle(fourier),x = self.xRange)

        self.freqMagAfter.plotItem.clear()
        fourierMag = self.freqMagAfter.plotItem.plot(pen='y')
        self.freqPhaseAfter.plotItem.clear()
        fourierPhase = self.freqPhaseAfter.plotItem.plot(pen='y')

        fourier = np.fft.fft(self.ydata[self.counter - 512:self.counter])
        fourierMag.setData(np.abs(fourier),x = self.xRange)
        fourierPhase.setData(np.angle(fourier),x = self.xRange)






    def recordBefore(self):
        counter = self.counter
        start = 0
        sf = 1000.0/15
        if(counter > 5000) :
            start = counter -5000
        record = np.array(self.xdata[start:counter])
        write("Recorded_Before.wav",sf,record)


    def recordAfter(self):
        counter = self.counter
        start = 0
        sf = 1000.0/15
        if(counter > 5000) :
            start = counter -5000
        record = np.array(self.ydata[start:counter])
        write("Recorded_After.wav",sf,record)


    def browseWavFile(self):
        self.filePath = QtGui.QFileDialog.getOpenFileName(self,'Single File', "~/","*.wav")
        self.sf , self.audioOriginal = read(self.filePath)



    def save(self):
        np.savetxt('test.txt', self.audioOriginal, fmt='%.3f',delimiter='\n')







class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

readingThread = myThread(1, "Thread-1", 1)


def main():
    App = QtGui.QApplication(sys.argv)
    form = DemoApp()
    form.show()
    App.exec_()


if __name__ == '__main__':
    main()
