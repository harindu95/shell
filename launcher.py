from PyQt4.QtGui import *
from PyQt4.QtCore import *
import functools
import os
def getLaunchers():
    apps = []
    for filename in os.listdir('/usr/share/applications'):
        try:
            with  open('/usr/share/applications/' + filename,'r') as file:
                text = file.readlines()
                try:
                    launcher=  extractData(text)
                    if(launcher):
                        apps.append(launcher)
                except ValueError,e:
                    print e
        except IOError:
            pass

    return apps

def extractData(txt):
    app = {"Exec":'','Icon':'','Comment':''}
    for line in txt:
        if 'Name' in line and not 'Name' in app.keys():
            app['Name'] = line[line.index('=')+1:].replace('\n','')
        elif 'Comment' in line and app['Comment']=='' :
            app['Comment'] = line[line.index('=')+1:].replace('\n','')
        elif 'Exec' in line:
            app['Exec'] = line[line.index('=')+1:].replace('\n','')
        elif 'Icon' in line:
            app['Icon'] = line[line.index('=')+1:].replace('\n','')
    if app['Exec'] == '':
        return None
    return app

class AppButton(QToolButton):

    """Docstring for MyClass. """

    def __init__(self,name,command,icon,comment,widget):
        """TODO: to be defined. """
        QPushButton.__init__(self,widget)
        if 'GTK;' in icon:
            icon = icon.split(';')[-1]
        if(icon.startswith('/')):
            self.setIcon(QIcon(icon))
        else:
            self.setIcon(QIcon(self.icon_fullpath(icon)))
            
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon);
        # Qt.ToolButton
        self.setStyleSheet('QToolButton { background:none; border:none; color:white;font-size:10px} QToolButton:hover { background:black; color:white;}')
        self.setIconSize(QSize(80,80))
        self.cmd =  functools.partial(os.system,command + '&')
        
        self.name = name
        self.command = command
        self.icon = icon
        self.comment = comment
        self.clicked.connect(self.cmd)
        self.setText(name)
        
    def icon_fullpath(self,icon):
        import gtk
        
        icon_theme = gtk.icon_theme_get_default()
        icon_info = icon_theme.lookup_icon(icon, 64, 0)
        
        if icon_info == None:
            return '/usr/share/icons/Numix/32/status/dialog-question.svg'
        # print icon_info.get_filename()
        return icon_info.get_filename()

