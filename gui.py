from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from pynput import keyboard

class MainWindow(QMainWindow):
    
    def __init__(self, app):
        
        super().__init__(None, Qt.WindowType.WindowStaysOnTopHint)
        
        self.app = app
        
        self.controlsGrid = {
            self.app.controlsGrid['listen']: self.handleListenChange,
            self.app.controlsGrid['play']: self.handlePlayChange,
            self.app.controlsGrid['playloop']: self.handlePlayChange
        }
        
        self.app.keyboardListener.addCallback(self.handleHotkey)
        
        #self.setFixedSize(QSize(600, 400))
        
        self.setWindowTitle("Clicker")
        
        self.mainLayout = QGridLayout()
        
        
        self.listeningStateLabel = QLabel("Запись: НЕТ")
        self.listeningStateLabel.setFont(QFont("Comic Sans MS", 24))
        self.mainLayout.addWidget(self.listeningStateLabel, 0, 0)
        
        #self.mainLayout.addWidget(QPushButton(text="test"), 1, 1)
        
        self.playingStateLabel = QLabel("Запущен: НЕТ")
        self.playingStateLabel.setFont(QFont("Comic Sans MS", 24))
        self.mainLayout.addWidget(self.playingStateLabel, 0, 2)
        
        #self.loopCheckbox = QCheckBox(text="Повторять")
        #self.loopCheckbox.setFont(QFont("Comic Sans MS", 18))
        #self.mainLayout.addWidget(self.loopCheckbox, 1, 0)
        
        #timesEditLabel =  QLabel(text = "Количество повторений:")
        #timesEditLabel.setFont(QFont("Comic Sans MS", 14))
        
        #self.timesEdit = QLineEdit()
        #self.timesEdit.setFont(QFont("Comic Sans MS", 14))
        #self.timesEdit.clearFocus()
        
        #self.mainLayout.addWidget(timesEditLabel, 1, 1)
        #self.mainLayout.addWidget(self.timesEdit, 1, 2)
        
        self.speedSlider = QSlider(Qt.Orientation.Horizontal)
        self.speedSlider.setMinimum(1)
        self.speedSlider.setMaximum(10)
        
        self.speedLabel = QLabel(text="Скорость: 1")
        self.speedLabel.setFont(QFont("Comic Sans MS", 18))
        
        self.mainLayout.addWidget(self.speedLabel, 2, 0)
        self.mainLayout.addWidget(self.speedSlider, 2, 1)
        
        self.speedSlider.valueChanged.connect(self.speedChange)
        
        widget = QWidget()
        widget.setLayout(self.mainLayout)
        self.setCentralWidget(widget)
    
    def handleListenChange(self):

        if self.app.clicker.listening:
            
            self.listeningStateLabel.setText("Запись: ДА")
            
        else:
            
            self.listeningStateLabel.setText("Запись: НЕТ")
    
    def handlePlayChange(self):
        
        if self.app.clicker.playInfo.playing:
            
            self.playingStateLabel.setText("Запущен: ДА" + (" (в цикле)" if self.app.clicker.playInfo.loop else ""))
            
        else:
            
            self.playingStateLabel.setText("Запущен: НЕТ")
    
    def handleHotkey(self, event):
        
        if not type(event.key) is keyboard.KeyCode:
            print('not implemented')
            return
        
        for control in self.controlsGrid.keys():
            
            if event.key.char == control:
                self.controlsGrid[control]()
                  
    def speedChange(self):
        
        self.app.clicker.changeSpeed(self.speedSlider.value())
        self.speedLabel.setText(f"Скорость: {self.speedSlider.value()}")

