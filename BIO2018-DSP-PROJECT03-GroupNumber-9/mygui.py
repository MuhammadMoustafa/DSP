# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filter.ui'
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
        MainWindow.resize(1237, 931)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.mainWidget = QtGui.QWidget(self.centralwidget)
        self.mainWidget.setGeometry(QtCore.QRect(-10, 0, 1381, 881))
        self.mainWidget.setObjectName(_fromUtf8("mainWidget"))
        self.layoutWidget = QtGui.QWidget(self.mainWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 0, 151, 95))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.browseBtn = QtGui.QPushButton(self.layoutWidget)
        self.browseBtn.setObjectName(_fromUtf8("browseBtn"))
        self.verticalLayout_2.addWidget(self.browseBtn)
        self.plotBtn = QtGui.QPushButton(self.layoutWidget)
        self.plotBtn.setObjectName(_fromUtf8("plotBtn"))
        self.verticalLayout_2.addWidget(self.plotBtn)
        self.playBtn = QtGui.QPushButton(self.layoutWidget)
        self.playBtn.setObjectName(_fromUtf8("playBtn"))
        self.verticalLayout_2.addWidget(self.playBtn)
        self.verticalLayoutWidget = QtGui.QWidget(self.mainWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(110, 110, 541, 201))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.offlineMagnitudeLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.offlineMagnitudeLayout.setObjectName(_fromUtf8("offlineMagnitudeLayout"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.mainWidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(690, 110, 531, 201))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.offlinePhaseLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.offlinePhaseLayout.setObjectName(_fromUtf8("offlinePhaseLayout"))
        self.verticalLayoutWidget_3 = QtGui.QWidget(self.mainWidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(690, 580, 531, 241))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.onlinePhaseLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.onlinePhaseLayout.setObjectName(_fromUtf8("onlinePhaseLayout"))
        self.verticalLayoutWidget_4 = QtGui.QWidget(self.mainWidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(110, 580, 541, 241))
        self.verticalLayoutWidget_4.setObjectName(_fromUtf8("verticalLayoutWidget_4"))
        self.onlineMagnitudeLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_4)
        self.onlineMagnitudeLayout.setObjectName(_fromUtf8("onlineMagnitudeLayout"))
        self.label = QtGui.QLabel(self.mainWidget)
        self.label.setGeometry(QtCore.QRect(30, 200, 66, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.mainWidget)
        self.label_2.setGeometry(QtCore.QRect(40, 690, 66, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.mainWidget)
        self.label_3.setGeometry(QtCore.QRect(340, 90, 101, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.mainWidget)
        self.label_4.setGeometry(QtCore.QRect(850, 80, 66, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayoutWidget_5 = QtGui.QWidget(self.mainWidget)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(110, 340, 541, 221))
        self.verticalLayoutWidget_5.setObjectName(_fromUtf8("verticalLayoutWidget_5"))
        self.filterMagnitudeLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_5)
        self.filterMagnitudeLayout.setObjectName(_fromUtf8("filterMagnitudeLayout"))
        self.verticalLayoutWidget_6 = QtGui.QWidget(self.mainWidget)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(690, 340, 541, 221))
        self.verticalLayoutWidget_6.setObjectName(_fromUtf8("verticalLayoutWidget_6"))
        self.filterPhaseLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_6)
        self.filterPhaseLayout.setObjectName(_fromUtf8("filterPhaseLayout"))
        self.layoutWidget_2 = QtGui.QWidget(self.mainWidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(170, 0, 151, 91))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.lowpassRadio = QtGui.QRadioButton(self.layoutWidget_2)
        self.lowpassRadio.setObjectName(_fromUtf8("lowpassRadio"))
        self.verticalLayout_3.addWidget(self.lowpassRadio)
        self.highpassRadio = QtGui.QRadioButton(self.layoutWidget_2)
        self.highpassRadio.setObjectName(_fromUtf8("highpassRadio"))
        self.verticalLayout_3.addWidget(self.highpassRadio)
        self.cornerFreq = QtGui.QLineEdit(self.layoutWidget_2)
        self.cornerFreq.setObjectName(_fromUtf8("cornerFreq"))
        self.verticalLayout_3.addWidget(self.cornerFreq)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1237, 25))
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
        self.plotBtn.setText(_translate("MainWindow", "PLOT", None))
        self.playBtn.setText(_translate("MainWindow", "Play", None))
        self.label.setText(_translate("MainWindow", "offline", None))
        self.label_2.setText(_translate("MainWindow", "online", None))
        self.label_3.setText(_translate("MainWindow", "Magnitude", None))
        self.label_4.setText(_translate("MainWindow", "Phase", None))
        self.lowpassRadio.setText(_translate("MainWindow", "low pass", None))
        self.highpassRadio.setText(_translate("MainWindow", "high pass", None))
        self.cornerFreq.setText(_translate("MainWindow", "corner frequency", None))

