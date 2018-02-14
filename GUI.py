#!/usr/bin/python3
# -*- coding: utf-8 -*-
import glob
import os
import math
import sys
import random
from PyQt5.QtWidgets import (QWidget,QToolTip, QLabel,QPushButton, QApplication, QMessageBox,QMainWindow, QAction, qApp,QDesktopWidget,
                             QHBoxLayout, QGridLayout, QFileDialog)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QDrag
from PyQt5.QtCore import QCoreApplication, pyqtSignal, QObject, Qt, QMimeData
from PyQt5 import QtCore
ml = None
mas_card2 = []
mas_cold = []
mas_arr = []
class Label(QLabel):

    def __init__(self, title, parent):
        self.id = []
        self.m = 0
        self.value = 0
        self.opened = False
        self.presence = True
        self.posx = 0
        self.posy = 0
        self.ind_x = -1
        self.ind_y = -1
        super().__init__(title, parent)

    def mouseMoveEvent(self, event):
        global ml
        ml = self
        if ml.opened == True:
            ml.raise_()
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        else:
            return


    def mouseReleaseEvent(self, event):
        min = 100000
        x_cor = 0
        y_cor = 0
        ix, iy = event.globalX(), event.globalY()
        for iy_pos in range(7):
            for ix_pos in range(iy_pos+1):
               pos_card = xy_coor(ix_pos, iy_pos)
               pos_rost = math.sqrt((ix - pos_card[0])**2 + (iy - pos_card[1])**2)
               if pos_rost <= min:
                   min = pos_rost
                   x_cor = ix_pos
                   y_cor = iy_pos
        if event.button() == QtCore.Qt.LeftButton:
            ml1 = self
            if (ml1.value == 13) and (ml1.opened == True) and (ml1.ind_x != -1) and (ml1.ind_y != -1):
                print(ml1.ind_x, ml1.ind_y)
                ml1.presence = False
                ml1.resize(0, 0)
                ml1.move(0, 0)
                testcard(ml1.ind_y, ml1.ind_x)
                print('1if1')
            elif (ml1.value == 13) and (ml1.opened == True):
                ml1.presence = False
                ml1.resize(0, 0)
                ml1.move(0, 0)
                del mas_cold[-1]
                print('1if2')

        try:
            if (mas_arr[y_cor][x_cor].presence == True) and (mas_arr[y_cor][x_cor].opened == True) and \
                    (mas_arr[y_cor][x_cor].value + ml.value == 13) and (ml.ind_x == -1) \
                    and (ml.ind_y == -1):
                mas_arr[y_cor][x_cor].resize(0, 0)
                mas_arr[y_cor][x_cor].move(0, 0)
                mas_arr[y_cor][x_cor].presence = False
                mas_cold[-1].resize(0,0)
                testcard(y_cor, x_cor)
                del mas_cold[-1]
                print('try1if1')
            elif (mas_arr[y_cor][x_cor].presence == True) and (mas_arr[y_cor][x_cor].opened == True)\
                    and (mas_arr[y_cor][x_cor].value + ml.value == 13) and (ml1.opened == True)\
                and (ml.ind_x != -1):
                x = ml.ind_x
                y = ml.ind_y
                mas_arr[y][x].presence = False
                mas_arr[y][x].resize(0, 0)
                mas_arr[y][x].move(0, 0)
                testcard(y, x)
                mas_arr[y_cor][x_cor].resize(0, 0)
                mas_arr[y_cor][x_cor].move(0, 0)
                mas_arr[y_cor][x_cor].presence = False
                testcard(y_cor, x_cor)


            else:
                if (ml.opened == True):
                    ml.move(ml.posx, ml.posy)
                elif (mas_arr[y_cor][x_cor].opened == True):
                    mas_arr[y_cor][x_cor].move(mas_arr[y_cor][x_cor].posx, mas_arr[y_cor][x_cor].posy)
                elif (mas_arr[y_cor][x_cor].opened == True) and (ml.opened == True):
                    mas_arr[y_cor][x_cor].move(mas_arr[y_cor][x_cor].posx, mas_arr[y_cor][x_cor].posy)
                    ml.move(ml.posx, ml.posy)
        except:
            return
    c = 0
    for i in mas_arr:
        if i.presence == False:
            c+=1
    if c == len(mas_arr):
        print("WIN")


    def mousePressEvent(self, event):
        self.offset = event.pos()

class card:
    def __init__(self, m, val):
        self.id = ""
        self.m = m
        self.value = val
        self.opened = False
        self.presence = True
        self.ind_x = -1
        self.ind_y = -1

class dump:
    def __init__(self):
        self.content = []
        for m in ["пики", "черви", "крести", "бубны"]:
            for value in range(1, 14):
                c = card(m, value)
                self.content.append(c)
        j = 0
        for i in glob.glob('Новая папка/*.png'):
            self.content[j].id = i
            j+=1
        print(self.content[1].id)
        print(self.content[1].value)
        random.shuffle(self.content)


    def get_card(self):
        return self.content.pop()

class Gui(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        d = dump()

        global mas_card2
        for i in range(52):
            lbl = Label("арта", self)
            lbl.value = d.content[i].value
            lbl.m = d.content[i].m
            lbl.id = d.content[i].id
            lbl.resize(60,88)
            lbl.move(584, 556)
            pixmap = QPixmap(r"C:\Users\Niko\Desktop\shirt5.png")
            lbl.setPixmap(pixmap)
            mas_card2.append(lbl)


        global mas_arr
        mas_arr = []
        res = []
        for iy in range(7):
            row = []
            mas_arr.append(row)
            for ix in range(iy + 1):
                iix, iiy = xy_coor(ix, iy)
                res.append((iix, iiy, ix, iy))
                row.append(None)

        res.sort(key=lambda x : (-x[-1], x[-2]))
        for (iix, iiy, ix, iy) in res:
            a = mas_card2.pop()
            a.posx = iix
            a.posy = iiy
            a.move(iix, iiy)
            mas_arr[iy][ix]= a
            a.ind_x = ix
            a.ind_y = iy

        for i in mas_arr[-1]:
            i.opened = True
            ma = QPixmap(r"C:\Users\Niko\Desktop\{0}".format(i.id))
            i.setPixmap(ma)
        print(mas_arr[-1][1].id)

#-------------меню
        self.butn = QPushButton("NEXT", self)
        self.butn.move(650, 556)
        self.butn.clicked.connect(self.backup)

        dialog = QAction('&Open', self)
        #dialog.triggered.connect(self.showDialog)
        exitAction = QAction('&Exit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(dialog)

        self.statusBar().showMessage('beta2.3')

#-------------главное окно
        self.setGeometry(0, 0, 1366, 740)
        self.setWindowTitle('Game')
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.show()
        self.setStyleSheet("background-color: #008000")



    def backup(self):
        global mas_cold,mas_card2

        if (len(mas_cold) == 0) and (len(mas_card2) != 0):
            mas_cold.append(mas_card2[-1])
            del mas_card2[-1]
            mas_cold[-1].opened = True
            ma = QPixmap(r"C:\Users\Niko\Desktop\{0}".format(mas_cold[-1].id))
            mas_cold[-1].setPixmap(ma)
            mas_cold[-1].posx = 770
            mas_cold[-1].posy = 556
            mas_cold[-1].move(770, 556)
            mas_cold[-1].raise_()

        elif (len(mas_card2) != 0):

            mas_cold[-1].opened = False
            pixmap = QPixmap(r"C:\Users\Niko\Desktop\shirt2.png")
            mas_cold[-1].setPixmap(pixmap)
            mas_cold.append(mas_card2[-1])
            del mas_card2[-1]
            mas_cold[-1].opened = True
            ma = QPixmap(r"C:\Users\Niko\Desktop\{0}".format(mas_cold[-1].id))
            mas_cold[-1].setPixmap(ma)
            mas_cold[-1].posx = 770
            mas_cold[-1].posy = 556
            mas_cold[-1].move(770, 556)
            mas_cold[-1].raise_()
        elif len(mas_card2) == 0:
            for i in mas_cold:
                mas_card2.append(i)
            mas_card2.reverse()
            for k in range(len(mas_card2)):
                pixmap = QPixmap(r"C:\Users\Niko\Desktop\shirt2.png")
                mas_card2[k].setPixmap(pixmap)
                mas_card2[k].move(584, 556)

'''

        def showDialog(self):


        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home', "(*.png)")[0]
        if fname == "":
            return
        self.lbl.move(-50,100)
        pixmap = QPixmap(fname)
        self.lbl.setPixmap(pixmap)
        s = name_alf(fname)
        self.lbl_name.setText(str(s))
        self.lbl_name.move(400,100)
        qf2 = QFont("Times", 70, QFont.Bold)
        self.lbl_name.setFont(qf2)


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'RecAlph',
                                     "Are you sure you want to exit from RecAlph ?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
  '''

def test_over():
    pass

def testcard(i, j):
    try:
        if (mas_arr[i][j + 1].presence == False) and (mas_arr[i][j - 1].presence == False) and \
                (mas_arr [i][j-1] != mas_arr[i][-1]):
            mas_arr[i - 1][j - 1].opened = True
            ma = QPixmap(r"C:\Users\Niko\Desktop\{0}".format(mas_arr[i - 1][j - 1].id))
            mas_arr[i - 1][j - 1].setPixmap(ma)
            mas_arr[i - 1][j].opened = True
            ma = QPixmap(r"C:\Users\Niko\Desktop\{0}".format(mas_arr[i - 1][j].id))
            mas_arr[i - 1][j].setPixmap(ma)
            print('if1')
        elif (mas_arr[i][j - 1].presence == False) and (mas_arr [i][j-1] != mas_arr[i][-1]):
            mas_arr[i - 1][j - 1].opened = True
            ma = QPixmap(r"C:\Users\Niko\Desktop\{0}".format(mas_arr[i - 1][j - 1].id))
            mas_arr[i - 1][j - 1].setPixmap(ma)
            print('if2')
        elif (mas_arr[i][j + 1].presence == False):
            mas_arr[i - 1][j].opened = True
            ma = QPixmap(r"C:\Users\Niko\Desktop\{0}".format(mas_arr[i - 1][j].id))
            mas_arr[i - 1][j].setPixmap(ma)
            print('if3')
    except:
        if (mas_arr[i][j - 1].presence == False):
            mas_arr[i - 1][j - 1].opened = True
            ma = QPixmap(r"C:\Users\Niko\Desktop\{0}".format(mas_arr[i - 1][j - 1].id))
            mas_arr[i - 1][j - 1].setPixmap(ma)
            print('-if1')
        elif (mas_arr[i][j + 1].presence == False) and (mas_arr [i][j-1] != mas_arr[i][-1]) :
            mas_arr[i - 1][j].opened = True
            ma = QPixmap(r"C:\Users\Niko\Desktop\{0}".format(mas_arr[i - 1][j].id))
            mas_arr[i - 1][j].setPixmap(ma)
            mas_arr[i - 1][j].opened = True
            ma = QPixmap(r"C:\Users\Niko\Desktop\{0}".format(mas_arr[i - 1][j].id))
            mas_arr[i - 1][j].setPixmap(ma)
            print('-if2')

def xy_coor(ix,iy):
    delta_x=67
    delta_y=67
    n_row = 7
    shift_x = 650
    shift_y = 50
    x = (ix-iy/2) * delta_x + shift_x
    y = iy * delta_y + shift_y
    return (x,y)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui()
    sys.exit(app.exec_())


#Король
#Координаты