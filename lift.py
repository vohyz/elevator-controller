#coding=utf-8
#edit by ZYX
#2019-4-25
import time
import sys
import gc
from functools import partial
from PyQt5 import QtWidgets,QtCore,QtGui
from Interface import Ui_MainWindow

storeys=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],]
class myWindow(QtWidgets.QMainWindow):
    fl = 1
    fl_2 = 1
    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.ui.button = QtWidgets.QPushButton(self.ui.centralwidget)
        self.ui.button.setText("警报\n ！！！")

        self.ui.button.setStyleSheet(
            "background-color: rgb(255, 80, 80);border-width: 1px;border-style: solid;border-color: rgb(255, 170, 150);")
        self.ui.button.setFont(font)
        self.ui.button.setGeometry(QtCore.QRect(900, 360, 100, 100))
        self.ui.button.clicked.connect(lambda: self.on_Click1())

        for i in range(0,10):
            self.ui.centralwidget.findChild(QtWidgets.QPushButton,tup3[i]).clicked.connect(partial(self.open,i+1))
        for i in range(0,38):
            self.ui.centralwidget.findChild(QtWidgets.QPushButton,tup2[i]).clicked.connect(partial(self.on_Clickout,i+1))
        for i in range(0,100):
            self.ui.centralwidget.findChild(QtWidgets.QPushButton,tup[i]).clicked.connect(partial(self.on_Click,i+1))

    def open(self,number):
        for i in range(1,6):
            if int(number)==2*i-1:
                lifti[i-1].calltowait=1
                lifti[i-1].waitcount=1
            elif int(number)==2*i:
                lifti[i-1].calltowait=0
                lifti[i-1].waitcount=4


    def on_Clickout(self,number): #电梯外按钮函数以及核心调度函数
        self.ui.centralwidget.findChild(QtWidgets.QPushButton, tup2[number - 1]).setStyleSheet(
            "background-color: rgb(255, 150, 80);border-width: 1px;border-style: solid;border-color: rgb(255, 170, 150);") #按钮颜色设置
        self.ui.centralwidget.findChild(QtWidgets.QPushButton, tup2[number - 1]).setEnabled(False)                         #按下后不可再按
        if number > 0 and number <= 19:#上升
            self.fl = 20-number
            minDic = [20, 20, 20, 20, 20]
            for i in range(0, 5):#按电梯距离排序
                minDic[i] = abs(int(lifti[i].seat) - int(self.fl))
            for i in range(0, 5):#按排序后的电梯距离顺序查找电梯
                sg = minDic.index(min(minDic))
                minDic[sg] = 20
                if lifti[sg].notbroken and(lifti[sg].isRest or (lifti[sg].willDown ==21 and lifti[sg].isUp and int(lifti[sg].seat) <= int(self.fl))or (lifti[sg].willUp and lifti[sg].willUp<int(self.fl))):
                    storeys[sg][int(self.fl) - 1] = 1#判断该电梯是否应该响应这次按键
                    lifti[sg].willUp = int(self.fl)
                    lifti[sg].willDown = 21
                    break

        elif number > 19 and number <= 38:#下降
            self.fl = 40 - number
            minDic = [20, 20, 20, 20, 20]
            for i in range(0, 5):#按电梯距离排序
                minDic[i] = abs(int(lifti[i].seat) - int(self.fl))
            for i in range(0, 5):#按排序后的电梯距离顺序查找电梯
                sg = minDic.index(min(minDic))
                minDic[sg] = 20
                if lifti[sg].notbroken and(lifti[sg].isRest or (lifti[sg].willUp==0 and lifti[sg].isDown and int(lifti[sg].seat) >= int(self.fl))or (lifti[sg].willDown!=21 and lifti[sg].willDown> int(self.fl))):
                    storeys[sg][int(self.fl) - 1] = 1#判断该电梯是否应该响应这次按键
                    lifti[sg].willDown = int(self.fl)
                    lifti[sg].willUp = 0
                    break



    def on_Click(self,number):
        self.timethread1=timeThread(number)
        self.timethread1.start()
        self.ui.centralwidget.findChild(QtWidgets.QPushButton, tup[number - 1]).setStyleSheet(
            "background-color: rgb(120, 220, 50);border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);")
        if number > 0 and number <= 20:
            storeys[0][20-number] = 1

        elif number > 20 and number <= 40:
            storeys[1][40-number] = 1

        elif number > 40 and number <= 60:
            storeys[2][60-number] = 1

        elif number > 60 and number <= 80:
            storeys[3][80-number] = 1

        elif number > 80 and number <= 100:
            storeys[4][100-number] = 1




    def on_Click1(self):
        self.ui.linelabel3.setHidden(True)
        self.ui.showtext()
        self.fl = self.ui.content
        if self.fl == 0:
            self.ui.linelabel3.setHidden(False)
            return 0
        lifti[int(self.fl)-1].notbroken = 0
        for i in range(0,20):
            self.ui.centralwidget.findChild(QtWidgets.QPushButton, tup[(int(self.fl)-1)*20+i]).setEnabled(False)
        self.ui.centralwidget.findChild(QtWidgets.QLabel, tup1[int(self.fl)-1]).setStyleSheet(
            "border-width: 3px;border-style: solid;border-color: rgb(255, 20, 20);")



class lift:
    '电梯类'
    notbroken = 1 #是否损坏
    number = 0 #电梯编号
    seat = 1 #电梯当前楼层
    isStop = 0 #电梯是否在楼层停靠
    isUp = 0 #上升中
    isDown = 0 #下降中
    isRest = 1 #无命令
    willUp = 0 #命令往上
    willDown = 21 #命令往下
    waittime = 2 #等待时间
    runtime = 1 #楼层通过时间
    calltowait = 1 #开门信号
    waitcount = 1 #开门计数
    def __init__(self,number,seat = 1):
        self.number = number
        self.seat = seat
        self.isRest = 1
        self.draw()

    def isEmpty(self):
        for i in range(0,20):
            if storeys[self.number-1][i] == 1:
                return False
        return True

    def setCondition(self,condition):
        if condition == 1:
            self.isUp = 1
            self.isDown = 0
            self.isRest = 0
        elif condition == -1:
            self.isUp = 0
            self.isDown = 1
            self.isRest = 0
        elif condition == 0:
            self.isUp = 0
            self.isDown = 0
            self.isRest = 1

    def upTo(self,floor):
        self.isStop = 0
        application.ui.centralwidget.findChild(QtWidgets.QLabel, tup1[self.number - 1]).setStyleSheet("border-width: 3px;border-style: solid;border-color: rgb(204, 232, 207);")
        while self.seat < int(floor):
            self.setCondition(1)
            time.sleep(self.runtime)
            application.ui.centralwidget.findChild(QtWidgets.QPushButton, tup[20 * self.number - self.seat - 1]).setStyleSheet("background-color: rgb(114, 58, 255);border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);")
            application.ui.centralwidget.findChild(QtWidgets.QPushButton,tup[20 * self.number - self.seat ]).setStyleSheet("background-color: rgb(255, 255, 255);border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);")
            if self.willUp==0and self.willDown == 21 and storeys[self.number-1][self.seat]==1:
                self.wait()
            if self.willUp and storeys[self.number-1][self.seat]==1:
                self.wait()
            self.seat += 1
        if self.willUp:
            application.ui.centralwidget.findChild(QtWidgets.QPushButton, tup2[ 19-int(floor)]).setStyleSheet(
                "border-width: 1px;border-style: solid;border-color: rgb(255, 170, 150);")
            application.ui.centralwidget.findChild(QtWidgets.QPushButton, tup2[ 19-int(floor)]).setEnabled(True)
        elif self.willDown!=21:
            application.ui.centralwidget.findChild(QtWidgets.QPushButton, tup2[ 39-int(floor)]).setStyleSheet(
                "border-width: 1px;border-style: solid;border-color: rgb(255, 170, 150);")
            application.ui.centralwidget.findChild(QtWidgets.QPushButton, tup2[39 - int(floor)]).setEnabled(True)
        self.isStop = 1
        application.ui.centralwidget.findChild(QtWidgets.QLabel, tup1[self.number - 1]).setStyleSheet("border-width: 3px;border-style: solid;border-color: rgb(255, 170, 0);")


    def downTo(self,floor):
        self.isStop = 0
        application.ui.centralwidget.findChild(QtWidgets.QLabel, tup1[self.number - 1]).setStyleSheet("border-width: 3px;border-style: solid;border-color: rgb(204, 232, 207);")
        while self.seat > int(floor):
            self.setCondition(-1)
            time.sleep(self.runtime)
            application.ui.centralwidget.findChild(QtWidgets.QPushButton,tup[20 * self.number - self.seat + 1]).setStyleSheet("background-color: rgb(114, 58, 255);border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);")
            application.ui.centralwidget.findChild(QtWidgets.QPushButton,tup[20 * self.number - self.seat]).setStyleSheet("background-color: rgb(255, 255, 255);border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);")
            if self.willUp==0and self.willDown == 21 and storeys[self.number-1][self.seat]==1:
                self.wait()
            if self.willDown!=21 and storeys[self.number-1][self.seat]==1:
                self.wait()
            self.seat -= 1
        if self.willUp:
            application.ui.centralwidget.findChild(QtWidgets.QPushButton, tup2[19-int(floor)]).setStyleSheet(
                "border-width: 1px;border-style: solid;border-color: rgb(255, 170, 150);")
            application.ui.centralwidget.findChild(QtWidgets.QPushButton, tup2[19 - int(floor)]).setEnabled(True)
        elif self.willDown!=21:
            application.ui.centralwidget.findChild(QtWidgets.QPushButton, tup2[39-int(floor)]).setStyleSheet(
                "border-width: 1px;border-style: solid;border-color: rgb(255, 170, 150);")
            application.ui.centralwidget.findChild(QtWidgets.QPushButton, tup2[39 - int(floor)]).setEnabled(True)
        self.isStop = 1
        application.ui.centralwidget.findChild(QtWidgets.QLabel,tup1[self.number-1]).setStyleSheet("border-width: 3px;border-style: solid;border-color: rgb(255, 170, 0);")

    def draw(self):
        application.ui.centralwidget.findChild(QtWidgets.QPushButton, tup[20 * self.number - self.seat]).setStyleSheet("background-color: rgb(114, 58, 255);border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);")

    def wait(self):
        self.waitcount = 0
        self.calltowait = 1
        while self.calltowait:
            self.isStop = 1
            application.ui.centralwidget.findChild(QtWidgets.QLabel, tup1[self.number - 1]).setStyleSheet(
                "border-width: 3px;border-style: solid;border-color: rgb(255, 170, 0);")
            if int(self.waitcount) >= 4:
                self.calltowait = 0
            time.sleep(0.5)
            self.waitcount += 1
        self.isStop = 0
        application.ui.centralwidget.findChild(QtWidgets.QLabel, tup1[self.number - 1]).setStyleSheet("border-width: 3px;border-style: solid;border-color: rgb(204, 232, 207);")
        self.calltowait = 1


class timeThread(QtCore.QThread):
    signal_time = QtCore.pyqtSignal(str, int)  # 信号
    number = 1
    def __init__(self,number,parent = None):
        super(timeThread, self).__init__(parent)
        self.number = number

    def run(self):
        application.ui.centralwidget.findChild(QtWidgets.QPushButton, tup[self.number - 1]).setEnabled(False)
        time.sleep(0.5)
        application.ui.centralwidget.findChild(QtWidgets.QPushButton, tup[self.number - 1]).setEnabled(True)


class liftThread1(QtCore.QThread):
    signal_time = QtCore.pyqtSignal(str, int)  # 信号
    threadID = 1
    fl = 1
    rest = 0
    def __init__(self, threadID,parent = None):
        super(liftThread1, self).__init__(parent)
        self.threadID = threadID

    def run(self):
        li = lifti[self.threadID-1]         #电梯和线程号绑定
        while True:
            while li.isEmpty() == False:    #检查电梯路径是否为空
                self.rest = 1
                if li.willUp:
                    for i in range(0, 20):
                        if storeys[self.threadID-1][i]:
                            self.fl = i + 1
                            storeys[self.threadID-1][i] = 0
                            self.rest = 0
                            break
                    if self.rest == 1:
                        li.setCondition(0)

                elif li.willDown:
                    i = 19
                    while i > 0:
                        if storeys[self.threadID-1][i]:
                            self.fl = i + 1
                            storeys[self.threadID-1][i] = 0
                            self.rest = 0
                            break
                        i -= 1
                    if self.rest == 1:
                        li.setCondition(0)
                elif li.isRest == 1:
                    for i in range(0, 20):
                        if storeys[self.threadID-1][i]:
                            self.fl = i + 1
                            storeys[self.threadID-1][i] = 0
                            break
                if int(li.seat) < int(self.fl):
                    li.upTo(self.fl)
                    li.wait()

                elif int(li.seat) >= int(self.fl):
                    li.downTo(self.fl)
                    li.wait()
            while li.isEmpty() == True:
                li.willDown = 21
                li.willUp = 0
                li.setCondition(0)
                time.sleep(0.1)

tup = ('label_21','label_22','label_23','label_24','label_25','label_26','label_27','label_28','label_29','label_30','label_31','label_32','label_33','label_34','label_35','label_36','label_37','label_38','label_39','label_40','label_41','label_42','label_43','label_44','label_45','label_46','label_47','label_48','label_49','label_50','label_51','label_52','label_53','label_54','label_55','label_56','label_57','label_58','label_59','label_60','label_61','label_62','label_63','label_64','label_65','label_66','label_67','label_68','label_69','label_70','label_71','label_72','label_73','label_74','label_75','label_76','label_77','label_78','label_79','label_80','label_81','label_82','label_83','label_84','label_85','label_86','label_87','label_88','label_89','label_90','label_91','label_92','label_93','label_94','label_95','label_96','label_97','label_98','label_99','label_100','label_101','label_102','label_103','label_104','label_105','label_106','label_107','label_108','label_109','label_110','label_111','label_112','label_113','label_114','label_115','label_116','label_117','label_118','label_119','label_120')
tup1 = ('label_200','label_300','label_400','label_500','label_600')
tup2 = ('outbutton_1','outbutton_2','outbutton_3','outbutton_4','outbutton_5','outbutton_6','outbutton_7','outbutton_8','outbutton_9','outbutton_10','outbutton_11','outbutton_12','outbutton_13','outbutton_14','outbutton_15','outbutton_16','outbutton_17','outbutton_18','outbutton_19','outbutton_20','outbutton_21','outbutton_22','outbutton_23','outbutton_24','outbutton_25','outbutton_26','outbutton_27','outbutton_28','outbutton_29','outbutton_30','outbutton_31','outbutton_32','outbutton_33','outbutton_34','outbutton_35','outbutton_36','outbutton_37','outbutton_38')
tup3 = ('labelbottom1','labelbottom2','labelbottom3','labelbottom4','labelbottom5','labelbottom6','labelbottom7','labelbottom8','labelbottom9','labelbottom0')
app = QtWidgets.QApplication([])
application = myWindow()

lifti = (lift(1),lift(2),lift(3),lift(4),lift(5))
threadi = (liftThread1(1),liftThread1(2),liftThread1(3),liftThread1(4),liftThread1(5))
for i in range(0,5):
    threadi[i].start()
application.show()
sys.exit(app.exec())
