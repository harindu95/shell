from PyQt4.QtCore import *
from PyQt4.QtGui import *
class MyLayout(QGridLayout):

    def __init__(self):
        super(MyLayout, self).__init__()
        self.cols = 5
        self.row = 0
        self.col = 0

    def addWidget(self,item):
        super(MyLayout,self).addWidget(item,self.row,self.col)
        self.col +=1
        if self.col > self.cols:
            self.col = 0
            self.row +=1

    def insertWidget(self,item,row,col):
        super(MyLayout,self).addWidget(item,row,col)

