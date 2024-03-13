from Storage import Storage
from Config import Config

class AudioRepository:
    def __init__(self):
        self.storage = Storage()

    def getAll(self):
        return self.storage.get('audios')
    
    def getByUrl(self, videoUrl):
        data = self.storage.get('audios')
        dataRes = [] 

        for audio in data:
            if (audio['videoUrl'] == videoUrl):
                return (audio) 
        return 0

    def removeByUrl(self, videoUrl):
        data = self.storage.get('audios')
        dataRes = [] 

        for audio in data:
            if (audio['videoUrl'] != videoUrl):
                dataRes.append(audio) 

        self.storage.set('audios', dataRes)


    def add(self, audio):
        data = self.storage.get('audios')
        data.append(audio)
        self.storage.set('audios', data)
