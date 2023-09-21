from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import * 
from dialogs import *
from util import getFilePathFromData

def widgetFromLayout(layout: QLayout) -> QWidget:
    """
    Gets QLayout and returns QWidget with it
    """
    
    layoutWidget = QWidget()        
    layoutWidget.setLayout(layout)
    return layoutWidget

class MainWindow(QMainWindow):
    
    def __init__(self):
        
        super().__init__(None, Qt.WindowType.WindowStaysOnTopHint)
        
        self.setFixedSize(QSize(650, 150))
        
        self.setWindowTitle("JClicks")
        
        self.initUI()
        self.initCallbacks()
    
    def initCallbacks(self):
        
        self.onSpeedChange = lambda _: None
        self.endTimeHandleChange = lambda _: None
        self.onHotkeysDialogOpened = lambda _: None
        self.onHotkeysDialogClosed = lambda _: None
        
    def initUI(self):
        
        self.mainLayout = QVBoxLayout()
        
        self.listeningStateLabel = QLabel("Запись: НЕТ")
        self.listeningStateLabel.setFont(QFont("Comic Sans MS", 24))
        
        self.playingStateLabel = QLabel("Запущен: НЕТ")
        self.playingStateLabel.setFont(QFont("Comic Sans MS", 24))
        self.playingStateLabel.setFixedWidth(425) #TODO: remove hardcoded siz
        self.playingStateLabel.setContentsMargins(25, 0, 0, 0)

        statesLayout = QHBoxLayout()
        statesLayout.addWidget(self.listeningStateLabel, alignment=Qt.AlignmentFlag.AlignTop)
        statesLayout.addWidget(self.playingStateLabel, alignment=Qt.AlignmentFlag.AlignTop)
        
        self.mainLayout.addWidget(widgetFromLayout(statesLayout))
        
        self.speedLabel = QLabel(text="Скорость: 1")
        self.speedLabel.setFont(QFont("Comic Sans MS", 18))
        self.speedLabel.setContentsMargins(0, 0, 10, 0)
        
        self.speedSlider = QSlider(Qt.Orientation.Horizontal)
        self.speedSlider.setMinimum(1)
        self.speedSlider.setMaximum(10)
        self.speedSlider.valueChanged.connect(self.speedChange)
        
        self.endTimeCheckBox = QCheckBox(text="Учитывать время в конце")
        self.endTimeCheckBox.setFont(QFont("Comic Sans MS", 18))
        self.endTimeCheckBox.setContentsMargins(10, 0, 0, 0)
        self.endTimeCheckBox.stateChanged.connect(self.endTimeChange)
        
        speedAndTimeLayout = QHBoxLayout()
        speedAndTimeLayout.addWidget(self.speedLabel)
        speedAndTimeLayout.addWidget(self.speedSlider)
        speedAndTimeLayout.addWidget(self.endTimeCheckBox)
        
        self.mainLayout.addWidget(widgetFromLayout(speedAndTimeLayout))
        
        widget = QWidget()
        widget.setLayout(self.mainLayout)
        self.setCentralWidget(widget)

        changeHotkeysAction = QAction("Управление кликером", self)
        changeHotkeysAction.triggered.connect(self.changeHotkeysDialog)
        
        self.toolbar = self.addToolBar("Управление кликером")
        self.toolbar.setFont(QFont("Comic Sans MS", 10))
        self.toolbar.addAction(changeHotkeysAction)
    
    def changeHotkeysDialog(self):
        
        hotkeysDialog = HotkeysDialog(self)
        
        if self.onHotkeysDialogClosed:
            hotkeysDialog.finished.connect(lambda _: self.onHotkeysDialogClosed(hotkeysDialog))
            
        self.onHotkeysDialogOpened(hotkeysDialog)
        hotkeysDialog.exec()
    
        
    def endTimeChange(self):
        
        self.endTimeHandleChange(self.endTimeCheckBox.isChecked())
    
    def handleListenChange(self, state: bool):

        if state:
            
            self.listeningStateLabel.setText("Запись: ДА")
            
        else:
            
            self.listeningStateLabel.setText("Запись: НЕТ")
    
    def handlePlayChange(self, state: bool, loop: bool):
        
        if state:
            
            self.playingStateLabel.setText("Запущен: ДА" + (" (в цикле)" if loop else " "))
            
        else:
            
            self.playingStateLabel.setText("Запущен: НЕТ")
                  
    def speedChange(self):
        
        #self.app.clicker.changeSpeed(self.speedSlider.value())
        if self.onSpeedChange:
            self.onSpeedChange(self.speedSlider.value())
            self.speedLabel.setText(f"Скорость: {self.speedSlider.value()}")

