import datetime

class UtilsHelper:

    def __init__(self):
        pass

    def xmlEscape(self, str):
        str = str.replace("&", "&amp;")
        str = str.replace("<", "&lt;")
        str = str.replace(">", "&gt;")
        str = str.replace('"', "&quot;")
        str = str.replace("'", "&apos;")
    
        return str

    def strToDate(self, dateStr):
        y = int(dateStr[0:4]) 
        m = int(dateStr[4:6]) 
        d = int(dateStr[6:]) 
        
        return datetime.date(y, m, d)

    def getSizeFromAudios(self, audios):
        currentSize = 0 

        for audio in audios:
            currentSize += audio.size

        return currentSize
