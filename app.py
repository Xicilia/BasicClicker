from PyQt6.QtWidgets import QApplication
from clicker import Clicker
from gui import MainWindow
from listeners import KeyboardListenerManager, MouseListenerManager
import threading
import sys
import time
import json

#reads controls file and fills controls grid
def getControls(controlsFileName: str):
    
    with open(controlsFileName, "r") as jsonFile:
        
        try:
            
            controlsObject = json.load(jsonFile)
            
            return controlsObject
            
        except:
            
            print("something wrong with controls file. Exit in 3 seconds...")
            time.sleep(3)
            sys.exit()

class App(QApplication):
    
    def __init__(self) -> None:
        
        super().__init__([])
        
        self.controlsGrid = getControls("controls.json")
        
        self.mouseListener = MouseListenerManager()
        self.keyboardListener = KeyboardListenerManager()
        
        self.clicker = Clicker(self.keyboardListener, self.controlsGrid)
        self.clickerThread = threading.Thread(target=self.clicker.idle, daemon=True)
        self.gui = MainWindow(self)
        
    def start(self):
        
        self.gui.show()
        #self.clickerThread.start()
        self.keyboardListener.startListening()
        self.clicker.playerThread.start()
        self.exec()
        sys.exit()