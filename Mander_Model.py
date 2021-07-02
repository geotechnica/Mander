import matplotlib
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtGui import QIntValidator
from untitled_python import Ui_MainWindow
matplotlib.use('Qt5Agg')

class MplCanvas(FigureCanvas):
    def __init__(self,parent=None,width=6,height=4,dpi=100):
        fig = Figure(figsize=(width,height),dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        fig.tight_layout()

class untitled_python(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.canvas = MplCanvas(self,width=5.5, height=4, dpi=100)
        self.ui.gridLayout_3.addWidget(self.canvas,3,1,1,1)
        self.reference_plot = None

        self.ui.statusbar.setStyleSheet("color:rgb(0,0,255)")
        self.ui.statusbar.showMessage("Designed by Anil Odabas -anil.odabas@gmail.com-")

        self.Demircap = ["6", "8", "10", "12", "14", "16", "18", "20", "22", "24", "25", "26", "28", "30", "32", "34", "36", "38", "40", "45", "50"]

        self.ui.comboBox.addItems(self.Demircap)
        self.ui.comboBox.currentIndexChanged.connect(self.ls)

        self.ui.comboBox_2.addItems(self.Demircap)
        self.ui.comboBox_2.currentIndexChanged.connect(self.ts)

        self.ui.fc.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2, notation=QtGui.QDoubleValidator.StandardNotation))
        self.ui.fs.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2, notation=QtGui.QDoubleValidator.StandardNotation))
        self.ui.paspayi.setValidator(QIntValidator(0, 99, self))
        self.ui.b.setValidator(QIntValidator(0, 999, self))
        self.ui.d.setValidator(QIntValidator(0, 999, self))
        self.ui.dnx.setValidator(QIntValidator(0, 99, self))
        self.ui.dny.setValidator(QIntValidator(0, 99, self))
        self.ui.lnx.setValidator(QIntValidator(0, 99, self))
        self.ui.lny.setValidator(QIntValidator(0, 99, self))
        self.ui.s.setValidator(QIntValidator(0, 99, self))


        self.ui.fc.textChanged.connect(self.fc)
        self.ui.fs.textChanged.connect(self.fs)
        self.ui.paspayi.textChanged.connect(self.paspayi)
        self.ui.b.textChanged.connect(self.b)
        self.ui.d.textChanged.connect(self.d)
        self.ui.lnx.textChanged.connect(self.lnx)
        self.ui.lny.textChanged.connect(self.lny)
        self.ui.dnx.textChanged.connect(self.dnx)
        self.ui.dny.textChanged.connect(self.dny)
        self.ui.s.textChanged.connect(self.s)

        #Başlangıç Değerleri
        self.fc = 30
        self.fs = 420
        self.paspayi = 5
        self.b = 50
        self.d = 30
        self.lnx = 5
        self.lny = 3
        self.dnx = 4
        self.dny = 2
        self.s = 10
        self.ls = 6
        self.ts = 6


        #PushButton Signal Alınması
        self.ui.pushButton.clicked.connect(self.Model)

    def fc(self):
        self.fc = int(self.ui.fc.text())

    def fs(self):
        self.fs = int(self.ui.fs.text())

    def paspayi(self):
        self.paspayi = int(self.ui.paspayi.text())

    def b(self):
        self.b = int(self.ui.b.text())

    def d(self):
        self.d = int(self.ui.d.text())

    def lnx(self):
        self.lnx = int(self.ui.lnx.text())

    def lny(self):
        self.lny = int(self.ui.lny.text())

    def dnx(self):
        self.dnx = int(self.ui.dnx.text())

    def dny(self):
        self.dny = int(self.ui.dny.text())

    def s(self):
        self.s = int(self.ui.s.text())

    def ls(self):
        self.ls = int(self.ui.comboBox.currentText())

    def ts(self):
        self.ts = int(self.ui.comboBox_2.currentText())

    def update_plot(self):
        self.plotdata = (self.x[int(self.Ecc/0.001)],self.ffc[int(self.Ecc/0.001)])
        self.canvas.axes.set_facecolor((0,0,0))

    def Model(self):

        self.si = self.s-self.ts #clear vertical spacing between spiral bars
        self.bc = self.b-2*self.paspayi
        self.dc = self.d-2*self.paspayi

        self.wb = (self.bc-self.lnx*self.ls-self.ts)/(self.lnx-1)
        self.Ai = list()
        for i in range(self.lnx-1):
            self.Ai.append((self.wb**2)/6)
        self.Ai = np.sum(self.Ai)
        self.Ae = (self.bc*self.dc-self.Ai)*(1-(self.si/(2*self.bc)))*(1-(self.si/(2*self.dc))) # area of effectively confined concrete core

        #confinement effectiveness coefficient
        self.ro_cc = (self.lnx*self.lny*(np.pi*(self.ls**2)/4))/((np.pi*self.bc**2)/4)
        self.Ac = self.b*self.d
        self.Acc = self.Ac * (1-self.ro_cc)
        self.ke = self.Ae/self.Acc

        #f1y and f1x calculation

        self.Asx = self.dnx*(np.pi*(self.ts**2)/4)
        self.Asy = self.dny*(np.pi*(self.ts**2)/4)

        self.ro_x = self.Asx/(self.s*self.bc)
        self.ro_y = self.Asy/(self.s*self.dc)

        self.fyh = 1.15 * self.fs
        self.f1x = self.ke*self.ro_x*self.fyh
        self.f1y = self.ke*self.ro_y*self.fyh
        self.f1 = (self.f1x**2+self.f1y**2)**.5

        #fcc calculation
        self.fcc = .85*self.fc*(-1.254+2.254*((1+(7.94*self.f1/self.fc))**.5)-2*(self.f1/self.fc))

        self.Eo = 0.002
        self.femin = min(self.f1y,self.f1x)
        self.Ecc = self.Eo*(1+5*((self.fcc/(0.85*self.fc))-1))
        self.Ecu = 0.004+self.femin/(4*self.fc)
        self.young_c = 4700*((self.fc)**0.5)

        self.r=(self.young_c/(self.young_c-(self.fcc/self.Ecc)))
        self.x=list()
        self.ffc = list()
        self.step = int(self.Ecu/0.001)+2
        self.ss = list()

        for i in range(0,self.step,1):
            self.x.append((i*0.001)/self.Ecc)
            self.ss.append(i*0.001)
            self.ffc.append((self.fcc*((i*0.001)/self.Ecc)*self.r)/(self.r-1+self.x[i]**self.r))

        self.plotdata = (self.ss[int(self.Ecc/0.001)],self.ffc[int(self.Ecc/0.001)])
        self.update_plot()

        self.canvas.axes.plot(self.ss,self.ffc)
        self.canvas.axes.set_facecolor((0,0,0))
        self.canvas.axes.yaxis.grid(True,linestyle='--')
        self.canvas.axes.set_ylabel("Stress (MPa)")
        self.canvas.axes.set_xlabel("Strain")
        self.canvas.axes.xaxis.grid(True, linestyle='--')
        self.update_plot()
        self.canvas.draw()


app = QtWidgets.QApplication([])
win = untitled_python()
win.show()
app.exec_()