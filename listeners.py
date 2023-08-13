from pynput import mouse, keyboard
from dataclasses import dataclass
from typing import Union, Callable
import time
import threading

@dataclass
class MouseEvent:
    
    x: int
    y: int
    button: mouse.Button
    time: float
   
    
@dataclass
class KeyboardEvent:
    
    key: Union[keyboard.KeyCode, keyboard.Key]
    time: float


class ListenerManager:
    
    def __init__(self):
        
        self._callbacks = []
        
    def addCallback(self, callback: Callable):
        
        self._callbacks.append(callback)
    
    def removeCallback(self, callback: Callable):
        
        self._callbacks.remove(callback)


class KeyboardListenerManager(ListenerManager):
    
    def __init__(self):
        
        super().__init__()
        
        self._listener = self._getListener()
    
    def _getListener(self):
        
        listener = keyboard.Listener(on_press=self._onPress)
        listener.daemon = True
        return listener
    
    def triggerCallbacks(self, key):
        
        self._onPress(keyboard.KeyCode(char=key))
    
    def _onPress(self, key):
        
        for callback in self._callbacks:
            
            callback(KeyboardEvent(key, time))
            
    def startListening(self):
        
        self._listener.start()
        
    def stopListening(self):
        
        self._listener.stop()
        self._listener = self._getListener() #for next start
        
    def getThread(self) -> keyboard.Listener:
        return self._listener
    
class MouseListenerManager(ListenerManager):
    
    def __init__(self):
        
        super().__init__()
        
        self._listener = mouse.Listener(on_click=self._onClick)
        self._listener.daemon = True
        
        self._lastTimeClicked = 0
    
    def _onClick(self, x: int, y: int, button: mouse.Button, pressed: bool):
        
        now = time.time() * 1000
        
        #prevent extra handled clicks
        if now - self._lastTimeClicked < 200:
            return
        
        self._lastTimeClicked = now
        
        for callback in self._callbacks:
            
            callback(MouseEvent(x, y, button, pressed))
    
    def startListening(self):
        
        self._listener.start()
        
    def stopListening(self):
        
        self._listener.stop()
        self._listener = self._getListener() #for next start
        
    def getThread(self) -> mouse.Listener:
        return self._listener

            

def _testKeyboardCallback(event: KeyboardEvent):
    
    if type(event.key) is keyboard.Key:
        print(f'pressed control button {event.key.value}')
    else:
        print(f"pressed key: {event.key.char}")

def _testMouseCallback(event: MouseEvent):
    
    print(f"mouse click at ({event.x};{event.y})")


if __name__ == "__main__":
    
    keyboardManager = KeyboardListenerManager()
    
    mouseManager = MouseListenerManager()
    
    keyboardManager.startListening()
    keyboardManager.addCallback(_testKeyboardCallback)
    
    mouseManager.startListening()
    mouseManager.addCallback(_testMouseCallback)
    
    while True:
        pass