from pynput import mouse, keyboard
import time
import threading
from dataclasses import dataclass
from typing import Optional
from listeners import MouseEvent

@dataclass
class PlayInfo:
    
    playing: bool #is clicker currently playing
    loop: bool #is clicker looped

class Clicker:
    
    def __init__(self, keyboardListener, controlsGrid):

        self.playInfo: PlayInfo = PlayInfo(False, False)
        
        self.listener = keyboardListener
        
        #times to play in non-loop variant
        self.times: int = 1
        #remaining times to play. Equals times at the start. If playing is looped becomes -1
        self.currentTimes: int = 0
        
        #is clicker listening to mouse events
        self.listening: bool = False 
        
        #handled mouse events list
        self._events: list[MouseEvent] = [] 
        #current event listener instance
        self._currentEventsListener: Optional[mouse.Listener] = None
        
        self.mouseController: mouse.Controller = mouse.Controller()
        
        #for correct hotkeys handle
        self._lastTimePressedControlButton: float = 0
        
        #current play speed
        self.speed: int = 1
        
        self.playerThread: threading.Thread = threading.Thread(target=self.playerManager, daemon=True)
        
        self.startKey = controlsGrid['play']
        #hotkeys with control functions associated with them
        self.controlsGrid = {
            controlsGrid['listen']: self._handleListening,
            controlsGrid['play']: self._handlePlayOnce,
            controlsGrid['playloop']: self._handlePlayLoop,
        }
        
        keyboardListener.addCallback(self.handleKeyboardEvent)
    
    #get event listener
    def _getListener(self) -> mouse.Listener:
        listener = mouse.Listener(on_click=self.onClickEventListener)
        listener.daemon = True
        return listener
        
    def onClickEventListener(self, x: int, y: int, button: mouse.Button, pressed: bool):
        
        if pressed:
            
            now = time.time() * 1000
            
            appending = True
            if len(self._events):
                
                lastEventTime = self._events[-1].time 
                appending = now - lastEventTime > 150   
            
            if appending: self._events.append(MouseEvent(x, y, button, now))
            print("event append")
    
    def _printEvents(self): #for debug
        
        for event in self._events:
            
            print(f"Mouse click at ({event.x};{event.y}), time: {event.time}")
    
    def playerManager(self):

        while True:

            if self.playInfo.playing: 

                self.playOnce()
                
                #if player isn't looped then stop playing
                if not self.playInfo.loop: 
                    
                    self.currentTimes -= 1
                    
                    if not self.currentTimes:
                        self.listener.triggerCallbacks(self.startKey)
                        self.playInfo.playing = False    
                
            time.sleep(1  / 60)    
    
    def playOnce(self):
        
        currentEventIndex = 0
        sleepTime = 0
        lastTimeClicked = 0
        
        while self.playInfo.playing and currentEventIndex != len(self._events):
            
            now = time.time() * 1000
            
            if (now - lastTimeClicked) > (sleepTime / self.speed):

                currentEvent = self._events[currentEventIndex]
            
                self.mouseController.position = (currentEvent.x, currentEvent.y)
                self.mouseController.click(currentEvent.button)
                
                # sleep time is difference in time between current event and next event in the list
                sleepTime = self._events[currentEventIndex + 1].time - currentEvent.time if currentEventIndex != len(self._events) - 1 else 0

                currentEventIndex += 1
                
                lastTimeClicked = now
                
            time.sleep(1 / 60)
            
    def _handleListening(self):
        
        if self.playInfo.playing: return
        
        if self._currentEventsListener and self._currentEventsListener.running:
            self._currentEventsListener.stop()
            print("recording stopped")
            
            self.listening = False
            
            self._printEvents()
            
        else:
            self.listening = True
            
            self._events = []
            self._currentEventsListener = self._getListener()
            self._currentEventsListener.start()
            print("recording started")   
    
    def _handlePlayOnce(self):
        
        #if player is not enabled, enables it
        if self._changePlayingType():
            
            self.playInfo.playing = True
            self.playInfo.loop = False
            
            self.currentTimes = self.times
            
            print("started playing")
    
    def _handlePlayLoop(self):
        
        #if player is not enabled, enables it with loop
        if self._changePlayingType():
            
            self.playInfo.playing = True
            self.playInfo.loop = True
            
            self.currentTimes = -1
            
            print("started playing with loop")
    
    #if player is playing - disables it and returns False, else returns True
    def _changePlayingType(self) -> bool:
        
        if self.listening or not len(self._events):
            
            print("not recorded")
            return False
        
        if self.playInfo.playing:
            
            self.playInfo.playing = False
            self.playInfo.loop = False
            print("stopped playing")
            
            return False
        
        return True
                        
    def _handlePlaying(self, isLoop: bool):
        
        if self.listening or not len(self._events):
             
            print("not recorded")
            return
        
        if self.playInfo.playing:
            
            self.playInfo.playing = False
            self.playInfo.loop = False
            print("stopped playing")
            
        else:
            
            self.playInfo.playing = True
            self.playInfo.loop = keyboard.is_pressed("f5")
            print("started playing" + (" with loop" if isLoop else ""))
    
    def increaseSpeed(self):
        
        if self.playInfo.playing: return
        
        self.changeSpeed(self.speed + 1)
        
    def decreaseSpeed(self):
        
        if self.playInfo.playing: return
        
        if self.speed > 1: self.changeSpeed(self.speed - 1)
    
    def changeSpeed(self, value: int):
        
        self.speed = value
        
        print(f"speed set to {self.speed}")
    
    def handleKeyboardEvent(self, event):
        
        if not type(event.key) is keyboard.KeyCode:
            print('not implemented')
            return
        
        for control in self.controlsGrid.keys():
            
            if event.key.char == control:
                self.controlsGrid[control]()
                  
    def idle(self):
        self.playerThread.start()
        
        print("started")
        while True:
                  
            time.sleep(1 / 60)
        

#clickerInstance = Clicker()

#clickerInstance.idle()

        