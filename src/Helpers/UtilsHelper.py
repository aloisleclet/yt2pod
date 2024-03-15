import datetime

class UtilsHelper:

    def __init__(self):
        pass

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
