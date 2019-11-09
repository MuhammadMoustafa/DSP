import mygui
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas)
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sc
import time
import xml.etree.ElementTree as ET

class TFApp(QtWidgets.QMainWindow, mygui.Ui_MainWindow):
    def __init__(self):
        super(TFApp, self).__init__()
        self.setupUi(self)
        circle1 = plt.Circle((0, 0), 1, fill=False, ls='dashed')

        f = plt.figure()
        a = f.add_subplot(111)


        plt.grid(True)
        a.add_artist(circle1)
        a.set_xlim(-1.1, +1.1)
        a.set_ylim(-1.1, +1.1)
        self.canvas = FigureCanvas(f)
        self.zplaneLayout.addWidget(self.canvas)
        self.canvas.draw()
        self.isPointAddable = False
        self.canvas.mpl_connect('button_press_event', self.onMouseClick)

        self.zeros, self.zerosXY, self.polesXY, self.poles = [], [], [], []
        self.resetBtn.clicked.connect(self.reset)
        self.table_points.setColumnWidth(0,220)
        self.table_points.setColumnWidth(1,220)
        self.drawTransferFunction()
        self.addBtn.clicked.connect(self.addFromTxt)
        self.browseBtn.clicked.connect(self.browse)
        self.isClicked = False
        self.count =0
        self.saveBtn.clicked.connect(self.saveFilter)
        self.axis = a
        self.fig = f


    def onMouseClick(self, event):
        if (self.moveChkBox.isChecked() == False):
            x, y = float(event.xdata), float(event.ydata)
            zPoint, type = self.checkProximity(x, y, .05)
            if type == "new":
                self.isPointAddable = True
                mytext = 'x = %f, y = %f' % (
                    x, y)
                distance = np.sqrt(x ** 2 + y ** 2)
                if distance > 1.0:
                    self.isPointAddable = False
                    mytext = "Error: out of range"
                self.lbl_point.setText(mytext)
                if event.button == 1:
                    self.addPoint(x, y, "Zero")
                    self.addPoint(x, y * -1, "Zero")
                else:
                    self.addPoint(x, y, "Pole")
                    self.addPoint(x, y * -1, "Pole")
                self.updateCircle()



            else:
                zPointMirror = zPoint.real - zPoint.imag * 1j
                self.deletePoint(zPoint, type)
                self.deletePoint(zPointMirror, type)
                self.deleteTable(self.table_points)
                self.reConstructTable(self.zeros, self.poles)
                self.updateCircle()


        else :
            x, y = float(event.xdata), float(event.ydata)
            zPoint, type = self.checkProximity(x, y, .05)
            self.isClicked = True
            if type == "new" :
                self.isClicked = False
            else :

                zPointMirror = zPoint.real - zPoint.imag * 1j
                self.deletePoint(zPoint, type)
                self.deletePoint(zPointMirror, type)
                self.deleteTable(self.table_points)
                self.reConstructTable(self.zeros, self.poles)
                self.zPointType = type
                # self.canvas.mpl_connect('button_release_event', self.onRelease)

                # self.canvas.mpl_connect('motion_notify_event', self.onMotion)

    def onRelease(self,event):
        # print "in on release"
        if (self.isClicked == True):
            x, y = float(event.xdata), float(event.ydata)
            self.isPointAddable = True
            mytext = 'x = %f, y = %f' % (
                x, y)
            distance = np.sqrt(x ** 2 + y ** 2)
            if distance > 1.0:
                self.isPointAddable = False
                mytext = "Error: out of range"
            self.lbl_point.setText(mytext)
            self.addPoint(x, y, self.zPointType)
            self.addPoint(x, y * -1, self.zPointType)
            self.updateCircle()
            self.isClicked = False
            self.count=0

    def onMotion(self,event):
        if(self.isClicked):
            print "on motion :",self.count
            self.count =self.count+1
            x, y = event.xdata,event.ydata
            mytext = 'x = %f, y = %f' % (
                x, y)
            self.lbl_point.setText(mytext)
            # if(self.zPointType == "Zero"):
            #     self.zerosXY.append([x,y])
            #     self.zerosXY.append([x,-1*y])
            #     self.drawOnMotion()
            #     self.zerosXY.pop()
            #     self.zerosXY.pop()
            # else :
            #     self.polesXY.append([x, y])
            #     self.polesXY.append([x, -1 * y])
            #     self.drawOnMotion()
            #     self.polesXY.pop()
            #     self.polesXY.pop()





    # def getPoint(self, real, imag):
    #     return np.sqrt(real**2 + imag**2)

    # def getRealImag(self, x, y):
    #     theta = np.arctan(y/x)
    #     amplitude = np.sqrt(x**2 + y**2)
    #     real = amplitude * np.cos(theta)
    #     imag = amplitude * np.sin(theta)
    #     return self.getPoint(real, imag)

    def addPoint(self,x,y,type):
        if self.isPointAddable:
            if type == 'Zero':
                #zero = self.getRealImag(self.xPoint, self.yPoint)
                zero = complex(round(x, 5), round(y, 5))
                self.zeros.append(zero)
                self.zerosXY.append([x, y])
                if len(self.zeros) >= self.table_points.rowCount():
                    self.table_points.setRowCount(len(self.zeros))
                self.table_points.setItem(len(self.zeros)-1, 0, QtWidgets.QTableWidgetItem(str(zero)))

            if type == 'Pole':
                #pole = self.getRealImag(self.xPoint, self.yPoint)
                pole = complex(round(x, 5), round(y, 5))
                self.poles.append(pole)
                self.polesXY.append([x, y])
                if len(self.poles) >= self.table_points.rowCount():
                    self.table_points.setRowCount(len(self.poles))
                self.table_points.setItem(len(self.poles)-1, 1, QtWidgets.QTableWidgetItem(str(pole)))

    def column(self, matrix, i):
        return [row[i] for row in matrix]

    def updateCircle(self):
        plt.close('all')
        self.clearLayout(self.zplaneLayout)
        circle1 = plt.Circle((0, 0), 1, fill=False, ls='dashed')
        f = plt.figure()
        a = f.add_subplot(111)
        plt.grid(True)
        a.add_artist(circle1)
        a.set_xlim(-1.1, +1.1)
        a.set_ylim(-1.1, +1.1)
        t1 = plt.plot(self.column(self.zerosXY, 0), self.column(self.zerosXY, 1), 'go', ms=10)
        plt.setp(t1, markersize=10.0, markeredgewidth=1.0, markeredgecolor='k', markerfacecolor='g')

        t2 = plt.plot(self.column(self.polesXY, 0), self.column(self.polesXY, 1), 'rx', ms=10)
        plt.setp(t2, markersize=12.0, markeredgewidth=3.0, markeredgecolor='r', markerfacecolor='r')
        self.canvas = FigureCanvas(f)
        self.zplaneLayout.addWidget(self.canvas)
        self.canvas.draw()
        self.canvas.mpl_connect('button_press_event', self.onMouseClick)
        self.canvas.mpl_connect('button_release_event', self.onRelease)
        self.canvas.mpl_connect('motion_notify_event', self.onMotion)

        self.drawTransferFunction()
        self.fig=f
        self.axis=a
        return

    def drawTransferFunction(self):
        #plt.clf()
        self.clearLayout(self.transferFunctionLayout)
        num, dom = sc.zpk2tf(self.zeros, self.poles, 1)
        w, h = sc.freqz(num, dom)
        f = plt.figure()
        a=plt.subplot(111)
        a.plot(w, abs(h))
        self.canvas_tf = FigureCanvas(f)
        self.transferFunctionLayout.addWidget(self.canvas_tf)
        self.canvas_tf.draw()

        # plt.plot(w/np.pi, 20*np.log10(h.imag), "b")
        # plt.plot(-w/np.pi,  20*np.log10(h.imag), "r")
        return

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            # remove the item from layout
            layout.removeItem(item)

    def reset(self):
        plt.close('all')
        self.clearLayout(self.transferFunctionLayout)
        self.clearLayout(self.zplaneLayout)
        self.zeros, self.zerosXY, self.polesXY, self.poles = [], [], [], []
        self.deleteTable(self.table_points)
        self.reConstructTable(self.zeros, self.poles)
        self.updateCircle()

        # f = plt.figure()
        # a = f.add_subplot(111)
        # plt.grid(True)
        # # a.add_artist(circle1)
        # a.set_xlim(-1.1, +1.1)
        # a.set_ylim(-1.1, +1.1)
        # self.canvas = FigureCanvas(f)
        # self.zplaneLayout.addWidget(self.canvas)
        # self.canvas.draw()
        # self.isPointAddable = False
        # self.deleteTable(self.table_points)
        # self.reConstructgTable(self.zeros,self.poles)
        # self.canvas.mpl_connect('button_press_event', self.onMouseClick)
        # self.zeros, self.zerosXY, self.polesXY, self.poles = [], [], [], []
        # self.deleteTable(self.table_points)


    def deleteTable (self,table):
        for i in reversed(range(table.rowCount())):
            table.removeRow(i)
    def reConstructTable (self,zeros,poles):
        if len(zeros)>len(poles):
            self.table_points.setRowCount(len(zeros))
        else :
            self.table_points.setRowCount(len(poles))

        for i in range(len(zeros)):
            # zero = self.getRealImag(self.xPoint, self.yPoint)
            zero = zeros[i]
            self.table_points.setItem(i, 0, QtWidgets.QTableWidgetItem(str(zero)))

        for i in range(len(poles)):
            # zero = self.getRealImag(self.xPoint, self.yPoint)
            pole = poles[i]
            self.table_points.setItem(i,1 , QtWidgets.QTableWidgetItem(str(pole)))

    def checkProximity(self,x,y,epsilon):
        for i in range(len(self.zeros)):
            zero = self.zeros[i]
            distance = ((x-zero.real)**2+(y-zero.imag)**2)**.5
            if(distance<= epsilon):
                return zero ,"Zero"
        for i in range(len(self.poles)):
            pole = self.poles[i]
            distance = ((x-pole.real)**2+(y-pole.imag)**2)**.5
            if(distance<= epsilon):
                return pole ,"Pole"
        return 5, "new"
    def deletePoint (self,zPoint,type  ):
        if type =="Zero" :
            i=0
            for item in  self.zeros :
                if(item==zPoint):
                    self.zeros.remove(item)
                    self.zerosXY.remove(self.zerosXY[i])

                i = i + 1

        else :
            i=0
            for item in self.poles :
                if(item == zPoint):
                    self.poles.remove(item)
                    self.polesXY.remove(self.polesXY[i])
                i = i + 1
    def addFromTxt(self):

        x=float(self.xTxtBox.text())
        y=float(self.yTxtBox.text())

        distance = (x ** 2 + y ** 2)**.5
        if distance > 1.0:
            self.isPointAddable = False
            mytext = "Error: out of range"

        else :
            mytext = 'x = %f, y = %f' % (
                x, y)
            self.isPointAddable=True

            if (self.zeroRadio.isChecked()):
                self.addPoint(x, y, "Zero")
                self.addPoint(x, -1 * y, "Zero")
                self.updateCircle()
            elif self.poleRadio.isChecked():
                self.addPoint(x, y, "Pole")
                self.addPoint(x, -1 * y, "Pole")
                self.updateCircle()

        self.lbl_point.setText(mytext)

    def readFilter(self,name):
        root=ET.parse(name).getroot()
        zeros , poles = [],[]
        for child in root :
            if child.tag =="zero":
                x,y= child.text.split(',')
                zeros.append([float(x),float(y)])
            elif child.tag == "pole":
                x,y=child.text.split(',')
                poles.append([float(x),float(y)])

        return zeros,poles

    def saveFilter(self):

        root = ET.Element("filter")
        for zero in self.zeros:
            x=zero.real
            y=zero.imag
            ET.SubElement(root, "zero").text ="%f,%f" % (x, y)
        for pole in self.poles:
            x=pole.real
            y=pole.imag
            ET.SubElement(root, "pole").text ="%f,%f" % (x, y)




        tree = ET.ElementTree(root)
        tree.write("newFilter.xml")

    def browse(self):

        filePath,_ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', "~/", "*.xml")
        zeros,poles=self.readFilter(filePath)
        self.zeros, self.zerosXY, self.polesXY, self.poles = [], [], [], []
        self.isPointAddable=True
        for zero in zeros:
            x,y = zero[0],zero[1]
            self.isPointAddable = True
            distance = np.sqrt(x ** 2 + y ** 2)
            if distance > 1.0:
                self.isPointAddable = False
            self.addPoint(x, y, "Zero")
            self.addPoint(x, y * -1, "Zero")
        for pole in poles:
            x, y = pole[0], pole[1]
            self.isPointAddable = True
            distance = np.sqrt(x ** 2 + y ** 2)
            if distance > 1.0:
                self.isPointAddable = False
            self.addPoint(x, y, "Pole")
            self.addPoint(x, y * -1, "Pole")

        self.updateCircle()

    # def drawOnMotion(self,x,y,type):
    #
    #
    #
    #     print "drawOnmotion"
    #
    #     plt.close('all')
    #     self.clearLayout(self.zplaneLayout)
    #     circle1 = plt.Circle((0, 0), 1, fill=False, ls='dashed')
    #     f = plt.figure()
    #     a = f.add_subplot(111)
    #     plt.grid(True)
    #     a.add_artist(circle1)
    #     a.set_xlim(-1.1, +1.1)
    #     a.set_ylim(-1.1, +1.1)
    #     t1 = plt.plot(x, y, 'go', ms=10)
    #     plt.setp(t1, markersize=10.0, markeredgewidth=1.0, markeredgecolor='k', markerfacecolor='g')
    #
    #     # t2 = plt.plot(self.column(self.polesXY, 0), self.column(self.polesXY, 1), 'rx', ms=10)
    #     # plt.setp(t2, markersize=12.0, markeredgewidth=3.0, markeredgecolor='r', markerfacecolor='r')
    #     self.canvas = FigureCanvas(f)
    #     self.zplaneLayout.addWidget(self.canvas)
    #     self.canvas.draw()
    #     # self.canvas.mpl_connect('button_press_event', self.onMouseClick)
    #     # self.canvas.mpl_connect('button_release_event', self.onRelease)
    #     # self.canvas.mpl_connect('motion_notify_event', self.onMotion)
    #
    #     self.drawTransferFunction()
    #     self.fig = f
    #     self.axis = a
    #     return
    #
    #
    #
    #     # # self.clearLayout(self.zplaneLayout)
    #     # f = self.fig
    #     # a = self.axis
    #     # a
    #     #
    #     #
    #     # if (type =="Zero"):
    #     #     t1 = plt.plot(x, y, 'go', ms=10)
    #     #     plt.setp(t1, markersize=10.0, markeredgewidth=1.0, markeredgecolor='k', markerfacecolor='g')
    #     # else:
    #     #     t2 = plt.plot(x, y, 'rx', ms=10)
    #     #     plt.setp(t2, markersize=12.0, markeredgewidth=3.0, markeredgecolor='r', markerfacecolor='r')
    #     #
    #     #
    #     #
    #     # self.canvas = FigureCanvas(f)
    #     # # self.zplaneLayout.addWidget(self.canvas) #problem here
    #     # self.canvas.draw()
    #     # # self.canvas.mpl_connect('button_press_event', self.onMouseClick)
    #     # # self.canvas.mpl_connect('button_release_event', self.onRelease)
    #     # # self.canvas.mpl_connect('motion_notify_event', self.onMotion)
    #
    #     # self.drawTransferFunction()
    #     return
    #
    #
    # def drawOnMotion(self):
    #     plt.close('all')
    #     self.clearLayout(self.zplaneLayout)
    #     circle1 = plt.Circle((0, 0), 1, fill=False, ls='dashed')
    #     f = plt.figure()
    #     a = f.add_subplot(111)
    #     plt.grid(True)
    #     a.add_artist(circle1)
    #     a.set_xlim(-1.1, +1.1)
    #     a.set_ylim(-1.1, +1.1)
    #     t1 = plt.plot(self.column(self.zerosXY, 0), self.column(self.zerosXY, 1), 'go', ms=10)
    #     plt.setp(t1, markersize=10.0, markeredgewidth=1.0, markeredgecolor='k', markerfacecolor='g')
    #
    #     t2 = plt.plot(self.column(self.polesXY, 0), self.column(self.polesXY, 1), 'rx', ms=10)
    #     plt.setp(t2, markersize=12.0, markeredgewidth=3.0, markeredgecolor='r', markerfacecolor='r')
    #     self.canvas = FigureCanvas(f)
    #     self.zplaneLayout.addWidget(self.canvas)
    #     self.canvas.draw()
    #     # self.canvas.mpl_connect('button_press_event', self.onMouseClick)
    #     # self.canvas.mpl_connect('button_release_event', self.onRelease)
    #     # self.canvas.mpl_connect('motion_notify_event', self.onMotion)
    #
    #     self.drawTransferFunction()
    #     self.fig = f
    #     self.axis = a
    #     return
    #






def main():
    App = QtWidgets.QApplication(sys.argv)
    form = TFApp()
    form.show()
    App.exec_()


if __name__ == '__main__':
    main()
