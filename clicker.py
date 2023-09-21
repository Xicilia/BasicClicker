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
    
    def __init__(self, appendEndWait: bool):

        self.playInfo: PlayInfo = PlayInfo(False, False)
        self.paused = False
        
        #times to play in non-loop variant
        self.times: int = 1
        #remaining times to play. Equals times at the start. If playing is looped becomes -1
        self.currentTimes: int = 0
        
        #is clicker listening to mouse events
        self.listening: bool = False 
        
        #handled mouse events list
        self._events: list[MouseEvent] = [] 
        
        self.mouseController: mouse.Controller = mouse.Controller()
        
        #for correct hotkeys handle
        self._lastTimePressedControlButton: float = 0
        
        #current play speed
        self.speed: int = 1
        
        self._playerThread: threading.Thread = threading.Thread(target=self.playerManager, daemon=True)
        
        self.appendEndWait = appendEndWait
        
        self._playEndCallback = None
        
    def onClickEventListener(self, event: MouseEvent):
        
        appending = True
        if len(self._events):
            
            lastEventTime = self._events[-1].time 
            appending = event.time - lastEventTime > 150   
        
        if appending: self._events.append(event)
        print("event append")
    
    def _printEvents(self): #for debug
        
        for event in self._events:
            
            print(f"Mouse click at ({event.x};{event.y}), time: {event.time}")
    
    def playerManager(self):

        while True:

            if self.playInfo.playing: 

                self._playOnce()
                
                #if player isn't looped then stop playing
                if not self.playInfo.loop: 
                    
                    self.currentTimes -= 1
                    
                    if not self.currentTimes:
                        self.playInfo.playing = False    
                        if self._playEndCallback: self._playEndCallback()
                
            time.sleep(1  / 60)    
    
    def _playOnce(self):
        
        currentEventIndex = 0
        sleepTime = 0
        lastTimeClicked = 0
        
        while self.playInfo.playing and currentEventIndex != len(self._events):
            
            now = time.time() * 1000
            
            if (now - lastTimeClicked) > (sleepTime / self.speed):
                
                currentEvent = self._events[currentEventIndex]
                
                #print(currentEvent.button)
                if currentEvent.button != None:
                    
                    self.mouseController.position = (currentEvent.x, currentEvent.y)
                    self.mouseController.click(currentEvent.button)
                    
                # sleep time is difference in time between current event and next event in the list
                sleepTime = self._events[currentEventIndex + 1].time - currentEvent.time if currentEventIndex != len(self._events) - 1 else 0

                currentEventIndex += 1
                
                lastTimeClicked = now
                
            time.sleep(1 / 60)
            
    def handleListen(self):
        
        if self.paused: return
        
        if self.playInfo.playing: return
        
        self.listening = not self.listening
        
        if not self.listening:
            print("recording stopped")
            
            if self.appendEndWait and len(self._events) != 0:
                self._events.append(MouseEvent(0, 0, None, time.time() * 1000))
            
            self._printEvents()
            
        else:
            
            self._events = []
            print("recording started")   
    
    def handlePlayOnce(self, callback):
        
        if self.paused: return
        
        #if player is not enabled, enables it
        if self._changePlayingType():
            
            self.playInfo.playing = True
            self.playInfo.loop = False
            
            self.currentTimes = self.times
            
            self._playEndCallback = callback
            
            print("started playing")
    
    def handlePlayLoop(self):
        
        if self.paused: return
        
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
    
    def changeSpeed(self, value: int):
        
        self.speed = value
        
        print(f"speed set to {self.speed}")
    
    def start(self):
        self._playerThread.start()

        