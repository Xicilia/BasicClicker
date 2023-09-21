from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from listeners import KeyboardEvent


class HotkeysDialog(QDialog):
    
    def __init__(self, parent = None):
        
        super().__init__(parent)
        
        self.setWindowTitle("Управление кликером")
        self.setFixedSize(QSize(350, 300))
    
        self.current = None
    
    def initUI(self, hotkeys: dict):
        
        self.hotkeys = hotkeys
        layout = QVBoxLayout()
        
        self.listen = QLabel(f"Запись: {self.hotkeys['listen'].capitalize()}")
        self.listen.setObjectName("listen")
        self.listen.setFont(QFont("Comic Sans MS", 18))

        layout.addWidget(self.listen, alignment = Qt.AlignmentFlag.AlignCenter)

        self.play = QLabel(f"Запуск: {self.hotkeys['play'].capitalize()}")
        self.play.setObjectName("play")
        self.play.setFont(QFont("Comic Sans MS", 18))

        layout.addWidget(self.play, alignment = Qt.AlignmentFlag.AlignCenter)
        
        self.playloop = QLabel(f"Запуск в цикле: {self.hotkeys['playloop'].capitalize()}")
        self.playloop.setObjectName("playloop")
        self.playloop.setFont(QFont("Comic Sans MS", 18))
        
        layout.addWidget(self.playloop, alignment = Qt.AlignmentFlag.AlignCenter)
        
        self.queue = [self.listen, self.play, self.playloop]
        self.currentIndex = -1
        
        self.setLayout(layout)  
        self.next()
        
    def next(self):
        
        if self.current:
            self.current.setStyleSheet(None)
        
        self.currentIndex += 1
        if self.currentIndex == len(self.queue):
            self.currentIndex = 0
        
        self.current = self.queue[self.currentIndex]
        self.current.setStyleSheet("border: 1px solid black;")
    
    def _keyIsOtherControl(self, key):
        """Checks that other controls is using given key"""
        for control, controlKey in self.hotkeys.items():
            if control != self.current.objectName() and key == controlKey:
                return True
            
        return False
                    
    def handleKey(self, event: KeyboardEvent):
        
        if self._keyIsOtherControl(event.key):
            return
        
        self.hotkeys[self.current.objectName()] = event.key
        
        oldText = self.current.text()
        
        newText = oldText[ : len(oldText) - oldText[::-1].find(" ")] + event.key.capitalize()
        self.current.setText(newText)
        
        self.next()