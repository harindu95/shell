#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import functools
from flowlayout import FlowLayout
from launcher import *
# from MyLayout import *


# Create an PyQT4 application object.
a = QApplication(sys.argv)

# The QWidget widget is the base class of all user interface objects in PyQt4.
# w = QWidget()
# panel = QWidget()

class MyWidget(QWidget):

    def __init__(self,parent=None):
        super(MyWidget,self).__init__(parent)
        self.blur = QGraphicsBlurEffect()

    def paintEvent(self,event) :
        backgroundColor = QColor('#22222')
        backgroundColor.setAlpha(120);
        
        customPainter = QPainter(self);
        # customPainter.setGraphicsEffect(self.blur)
        customPainter.fillRect(self.rect(),backgroundColor);
 
w = QWidget()
panel = w
# w.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
# w.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
# Set window size.
w.resize(820, 540)
# w.setAttribute(Qt.WA_TranslucentBackground)
# Set window title
w.setWindowTitle("Shell")
# w.setAttribute(Qt.WA_TranslucentBackground)
# w.setWindowOpacity(0.8)
backgroundImage =os.popen("gsettings get org.gnome.desktop.background picture-uri").read()[8:-2]

w.setStyleSheet(" background-image:url('/home/harindu/Pictures/mbuntu-3.jpg'); color:white;background-position: center;")
# w.setStyleSheet("* { background-image:"+backgroundImage+"; background-color: rgba(30,30,30,80); color:white;}")
# w.setStyleSheet("background-color: rgba(255,255,255,0);");
# fb = AppButton('/usr/share/icons/Numix/48@2x/apps/facebook.svg',w)
launchers = getLaunchers()
btns = []
layout = FlowLayout(spacing=30)
appPanel = QScrollArea()
stackedLayout = QStackedLayout()
pages = [QWidget(),None]
i = 0
firstApp = None
# for app in launchers:
#     try:
#         if not app == {}:
#             btn = AppButton(app['Name'], app['Exec'], app['Icon'], panel)
#             if not firstApp:
#                 firstApp = btn
#             btns.append(btn)
#             i += 1
#             layout.addWidget(btn)
#           
#         # layout.addChildWidget()
#     except Exception, e:
#         print app, e
# btn.setStyleSheet("background-color: white;")
# btn.setWindowOpacity(1.0)
pages[0].setLayout(layout)
stackedLayout.addWidget(pages[0])
appPanel.setLayout(stackedLayout)

vbox = QVBoxLayout()
search = QLineEdit()


class WorkThread(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.kill = False
    
    def __del__(self):
        self.quit()
      

    def run(self):
        print "started thread"
        layout = []
        # widget =  QWidget()
        for btn in btns:
            if self.kill :
                self.terminate()
            if str(self.txt).lower() in str(btn.text()).lower():
                layout.append(btn) 

        # widget.setLayout(layout)
        self.emit(SIGNAL('update'), layout)

        self.terminate()

class GenericWorker(QObject):
    def __init__(self, function, *args, **kwargs):
        super(GenericWorker, self).__init__()

        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start.connect(self.run)

    start = pyqtSignal(str)

    # @pyqtSlot
    def run(self, some_string_arg):
        self.function(*self.args, **self.kwargs)

def searchApp(txt):
    layout = []
        # widget =  QWidget()
    for btn in btns:
                
        if str(txt).lower() in str(btn.text()).lower():
            layout.append(btn) 

        # widget.setLayout(layout)
    thread.emit(SIGNAL('update'), layout)

def updateUI(l):
    global pages,firstApp
    pages[1] = QWidget()
    layout = FlowLayout(spacing=30)
    if len(l)>0:
        firstApp = l[0]
    else: 
        firstApp = None
    for item in l:
        layout.addWidget(item)
    pages[1].setLayout(layout)
    stackedLayout.addWidget(pages[1])
    stackedLayout.setCurrentWidget(pages[1])


class ThreadPool():

    def __init__(self):
        self.threads = []
        self.counter = 0
        
    
    def getThread(self):
        self.threads.append(WorkThread())
        for thread in self.threads:
            if thread.isFinished():
                # thread.wait()
                print thread.txt
                # thread = WorkThread()
                # thread.
        return self.threads[ -1 ]

    def setTerminateFlag(self):
        for thread in self.threads:
            if thread.isRunning():
                thread.kill = True


wks = ThreadPool()
thread = QThread()
thread.start()
thread.connect(thread, SIGNAL("update"), updateUI )
def searchText(txt):

    # if  wk.is_alive():
    #     stop_threads = True
    #     wk.join()
    # wk = Thread()
    # wk.txt = txt
    # wk.start()
    # global wk
    # # layout = FlowLayout()
    # launchers = btns
    # i = 0
    # for btn in launchers:
    #     if i > 30:
    #         return
    #
    #     if not str(txt).lower() in str(btn.text()).lower():
    #         btn.hide()
    #         layout.removeWidget(btn)
    #     else:
    #         if btn in layout.children():
    #             layout.removeWidget(btn)
    #         layout.addWidget(btn)
    #         i += 1
    #         btn.show()

        # wk.wait()
    # wks.setTerminateFlag()
    wk =  GenericWorker(searchApp,txt)
   
    
    wk.moveToThread(thread)
    wk.start.emit(txt)
    # wk.start() 
    #
    # appPanel.setLayout(layout)

def editFinished():
   if firstApp:
       firstApp.click()

search.textChanged.connect(searchText)
search.returnPressed.connect(editFinished)
hbox = FlowLayout()
# hbox.addWidget(search)
searchbox = QWidget()
searchbox.setLayout(hbox)
gridlayout = QGridLayout()
gridlayout.setColumnStretch(0,1)
gridlayout.setColumnStretch(2,1)
gridlayout.setColumnStretch(1,5)
gridlayout.setRowStretch(0,1)
gridlayout.setRowStretch(1,20)
gridlayout.setRowStretch(2,4)
gridlayout.setRowStretch(3,20)
gridlayout.setHorizontalSpacing(20)
gridlayout.addWidget(search,1,1)
gridlayout.addWidget(appPanel,3,1)
# vbox.addWidget(searchbox)
# vbox.addWidget(appPanel)

panel.setLayout(gridlayout)
# Show window
# w.setWidget(panel)
# w.widgetResizable= True
search.setFocus()
w.show()
# w.setWindowState( Qt.WindowFullScreen)
# w.size(QSize(400,400))
sys.exit(a.exec_())
