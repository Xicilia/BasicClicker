from PyQt6.QtWidgets import QApplication
from clicker import Clicker
from gui import MainWindow
from listeners import KeyboardListenerManager, MouseListenerManager, KeyboardEvent, MouseEvent
import sys
from util import getFilePathFromData
import json
from typing import Optional
from dialogs import *
from logger import Logger
import ctypes


class ControlsManager:
    
    _CONTROLSFILENAME = "controls.json"
    
    def __init__(self):
        
        self.controlsGrid = ControlsManager._getControlsFromFile(getFilePathFromData(ControlsManager._CONTROLSFILENAME))
    
    def _getControlsFromFile(controlsFileName: str):
        
        with open(controlsFileName, "r") as jsonFile:
            
            try:
                
                controlsObject = json.load(jsonFile)
                
                return controlsObject
                
            except Exception as e:
                
                Logger.log("Can't read controls.json, something's wrong with content.")
                Logger.errorLog(e)
                sys.exit()
        
    
    def getControls(self):
        return self.controlsGrid
    
    def updateControls(self):
        
        with open(getFilePathFromData(ControlsManager._CONTROLSFILENAME), "w") as jsonFile:
            
            try:
                
                json.dump(self.controlsGrid, jsonFile, indent=4)
                
            except Exception as e:
                
                Logger.log("Can't update controls.json.")
                Logger.errorLog(e)
                sys.exit()
        
    def getControlByChar(self, char: str) -> Optional[str]:
        """
        Returns control action binded to given char if any.
        """
        for control, key in self.controlsGrid.items():
            
            if key == char:
                
               return control
            
        return None


class App(QApplication):
    
    def __init__(self) -> None:
        
        super().__init__([])
        
        icon = QIcon()
        icon.addFile(getFilePathFromData("icon.ico"))
        
        self.setWindowIcon(icon)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('estellia.JClicks.1')
        
        self.controlsManager = ControlsManager()
        
        self.mouseListener = MouseListenerManager()
        self.mouseListener.addCallback(self._handleMouse)
        
        self.keyboardListener = KeyboardListenerManager()
        self.keyboardListener.addCallback(self._handleKeyboard)
        
        self.clicker: Clicker = Clicker(False)
        self.gui: MainWindow = MainWindow()
        
        self.gui.onSpeedChange = self.changeClickerSpeed
        self.gui.endTimeHandleChange = self.changeEndTimeHandle
        self.gui.onHotkeysDialogOpened = self.hotkeysDialogOpened
        self.gui.onHotkeysDialogClosed = self.hotkeysDialogClosed
    
    def _handleMouse(self, controlEvent: MouseEvent):
        pass
    
    def _handleKeyboard(self, controlEvent: KeyboardEvent):
        
        control = self.controlsManager.getControlByChar(controlEvent.key)
        
        if control == "listen":
            
            self.clicker.handleListen()
            
            if self.clicker.listening:
                self.mouseListener.addCallback(
                    self.clicker.onClickEventListener
                )
            else:
                self.mouseListener.removeCallback(
                    self.clicker.onClickEventListener
                )
                
            self.gui.handleListenChange(self.clicker.listening)
        
        elif control == "play":
            
            def playEndCallback():
                print("play ended")
                self.gui.handlePlayChange(False, False)
            
            self.clicker.handlePlayOnce(playEndCallback)
            self.gui.handlePlayChange(self.clicker.playInfo.playing, False)
        
        elif control == "playloop":
            
            self.clicker.handlePlayLoop()

            self.gui.handlePlayChange(self.clicker.playInfo.playing, True)

    def changeEndTimeHandle(self, handling: bool):
        
        if not self.clicker.playInfo.playing:
            self.clicker.appendEndWait = handling
    
    def changeClickerSpeed(self, value: int):
        self.clicker.changeSpeed(value)
    
    def hotkeysDialogOpened(self, dialog: HotkeysDialog):
        self.pauseClicker()
        
        dialog.initUI(self.controlsManager.getControls())

        self.keyboardListener.addCallback(dialog.handleKey)
    
    def hotkeysDialogClosed(self, dialog: HotkeysDialog):
        print("closed")
        self.keyboardListener.removeCallback(dialog.handleKey)
        self.controlsManager.updateControls()
        self.resumeClicker()
    
    def pauseClicker(self):
        self.clicker.paused = True
        
    def resumeClicker(self):
        self.clicker.paused = False
        
    def start(self):
        

        self.keyboardListener.startListening()
        self.mouseListener.startListening()
        
        self.clicker.start()

        self.gui.show()
        
        self.exec()
        sys.exit()