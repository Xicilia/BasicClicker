from datetime import datetime
import os

class Logger:
    
    _LOGFILENAME = "log.txt"
    _ERRORLOGSFILENAME = "errors.txt"
    
    def __init__(self):
        pass

            
    def _getLogTime() -> str:
        
        return datetime.now().strftime('%d.%m.%Y - %H:%M:%S')
    
    def log(logText: str):
        
        with open(Logger._LOGFILENAME, "a") as logFile:
            
            logFile.write(f"{Logger._getLogTime()} {logText}\n")
            
    def errorLog(error: Exception):
        
        with open(Logger._ERRORLOGSFILENAME, "a") as logFile:
            
            logFile.write(f"{Logger._getLogTime()} {error.__class__}: {error}\n")