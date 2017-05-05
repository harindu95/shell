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

class MyWidget(QWidget):

    def __init__(self,parent=None):
        super(MyWidget,self).__init__(parent)
        self.blur = QGraphicsBlurEffect()
        self.pixmap = QPixmap()
        backgroundImage =os.popen("gsettings get org.gnome.desktop.background picture-uri").read()[8:-2]
        self.pixmap.load(backgroundImage)

    def paintEvent(self,event) :
        # backgroundColor = QColor('#22222')
        # backgroundColor.setAlpha(120);
        # customPainter = QPainter(self);
        # customPainter.setGraphicsEffect(self.blur)
        # customPainter.fillRect(self.rect(),backgroundColor);
        paint = QPainter(self)
        widWidth = self.width()
        widHeight = self.height()
        self.pixmap = self.pixmap.scaled(widWidth, widHeight, Qt.KeepAspectRatioByExpanding)
        paint.drawPixmap(0, 0, self.pixmap)
 
w = MyWidget()
panel = w
# Set window size.
w.resize(820, 540)
# w.setAttribute(Qt.WA_TranslucentBackground)
# Set window title
w.setWindowTitle("Shell")

# fb = AppButton('/usr/share/icons/Numix/48@2x/apps/facebook.svg',w)
launchers = getLaunchers()
btns = []
layout = FlowLayout(spacing=30)
appPanel = QScrollArea()
# appPanel.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
stackedLayout = QStackedLayout()
pages = [QWidget(),None]
i = 0
firstApp = None
for app in launchers:
    try:
        if not app == {}:
            btn = AppButton(app['Name'], app['Exec'], app['Icon'], app['Comment'],panel)
            if not firstApp:
                firstApp = btn
            btns.append(btn)
            i += 1
            layout.addWidget(btn)
        # layout.addChildWidget()
    except Exception, e:
        print app, e
    

pages[0].setLayout(layout)
stackedLayout.addWidget(pages[0])
appPanel.setLayout(stackedLayout)

vbox = QVBoxLayout()
search = QLineEdit()
search.setPlaceholderText("Type to search")

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
    import re
    layout = []
    txt = str(txt).lower()
    pattern ='.*'+'.*'.join([c for c in txt])
    pattern = re.compile(pattern)
        # widget =  QWidget()
    for btn in btns:
        info = btn.name + btn.command + btn.comment
        info = info.lower()
        if pattern.match(info):
            if pattern.match(btn.name.lower()):
                layout.insert(0,btn)
            else:
                layout.append(btn) 

        # widget.setLayout(layout)
    thread.emit(SIGNAL('update'), layout)

def updateUI(l):
    global pages,firstApp
    pages[1] = QWidget()
    layout = FlowLayout(spacing=30)
    # layout = QVBoxLayout()
    if len(l)>0:
        firstApp = l[0]
    else: 
        firstApp = None
    for item in l:
        layout.addWidget(item)
    pages[1].setLayout(layout)
    
    stackedLayout.addWidget(pages[1])
    # stackedLayout.setSize(pages[1].baseSize())
    # pages[1].setMinimumSize(800,1200)
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
search.setStyleSheet("background:rgba(22,22,22,80);font:normal 14px;color:white;max-width:200px;margin:0 50px")
search.returnPressed.connect(editFinished)
hbox = QHBoxLayout()
hbox.addWidget(search)
searchbox = QWidget()
searchbox.setLayout(hbox)
gridlayout = QGridLayout()
gridlayout.setColumnStretch(0,1)
gridlayout.setColumnStretch(2,1)
gridlayout.setColumnStretch(1,5)
gridlayout.setRowStretch(0,1)
gridlayout.setRowStretch(1,2)
gridlayout.setRowStretch(2,1)
gridlayout.setRowStretch(3,20)
gridlayout.setHorizontalSpacing(20)
gridlayout.addWidget(searchbox,1,1)
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
