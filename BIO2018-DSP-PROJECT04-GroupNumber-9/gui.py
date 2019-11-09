# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1201, 602)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.signalBefore = PlotWidget(self.centralwidget)
        self.signalBefore.setGeometry(QtCore.QRect(140, 10, 321, 181))
        self.signalBefore.setObjectName(_fromUtf8("signalBefore"))
        self.browseBtn = QtGui.QPushButton(self.centralwidget)
        self.browseBtn.setGeometry(QtCore.QRect(10, 20, 101, 23))
        self.browseBtn.setObjectName(_fromUtf8("browseBtn"))
        self.saveBtn = QtGui.QPushButton(self.centralwidget)
        self.saveBtn.setGeometry(QtCore.QRect(10, 60, 101, 23))
        self.saveBtn.setObjectName(_fromUtf8("saveBtn"))
        self.recordBeforeBtn = QtGui.QPushButton(self.centralwidget)
        self.recordBeforeBtn.setGeometry(QtCore.QRect(10, 100, 101, 23))
        self.recordBeforeBtn.setObjectName(_fromUtf8("recordBeforeBtn"))
        self.signalAfter = PlotWidget(self.centralwidget)
        self.signalAfter.setGeometry(QtCore.QRect(140, 250, 321, 181))
        self.signalAfter.setObjectName(_fromUtf8("signalAfter"))
        self.freqMagBefore = PlotWidget(self.centralwidget)
        self.freqMagBefore.setGeometry(QtCore.QRect(480, 10, 321, 181))
        self.freqMagBefore.setObjectName(_fromUtf8("freqMagBefore"))
        self.freqMagAfter = PlotWidget(self.centralwidget)
        self.freqMagAfter.setGeometry(QtCore.QRect(480, 250, 321, 181))
        self.freqMagAfter.setObjectName(_fromUtf8("freqMagAfter"))
        self.freqPhaseBefore = PlotWidget(self.centralwidget)
        self.freqPhaseBefore.setGeometry(QtCore.QRect(820, 10, 321, 181))
        self.freqPhaseBefore.setObjectName(_fromUtf8("freqPhaseBefore"))
        self.freqPhaseAfter = PlotWidget(self.centralwidget)
        self.freqPhaseAfter.setGeometry(QtCore.QRect(820, 250, 321, 181))
        self.freqPhaseAfter.setObjectName(_fromUtf8("freqPhaseAfter"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 200, 81, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 440, 101, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(555, 200, 171, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(570, 440, 171, 20))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(890, 440, 171, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(890, 200, 171, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.recordAfterBtn = QtGui.QPushButton(self.centralwidget)
        self.recordAfterBtn.setGeometry(QtCore.QRect(10, 140, 101, 23))
        self.recordAfterBtn.setObjectName(_fromUtf8("recordAfterBtn"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1201, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.browseBtn.setText(_translate("MainWindow", "Browse", None))
        self.saveBtn.setText(_translate("MainWindow", "Save", None))
        self.recordBeforeBtn.setText(_translate("MainWindow", "Record Before filt", None))
        self.label.setText(_translate("MainWindow", "Original Signal", None))
        self.label_2.setText(_translate("MainWindow", "Filtered Signal", None))
        self.label_3.setText(_translate("MainWindow", "Original Signal Fourier (Mag.)", None))
        self.label_4.setText(_translate("MainWindow", "Filtered Signal Fourier (Mag.)", None))
        self.label_5.setText(_translate("MainWindow", "Filtered Signal Fourier (Phase)", None))
        self.label_6.setText(_translate("MainWindow", "Original Signal Fourier (Phase)", None))
        self.recordAfterBtn.setText(_translate("MainWindow", "Record After filt", None))

from pyqtgraph import PlotWidget
