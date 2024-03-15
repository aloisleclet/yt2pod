from Config import Config

from Helpers.StorageHelper import StorageHelper

from Entities.Audio import Audio

class AudioRepository:
    def __init__(self):
        self.config = Config()
        self.storage = StorageHelper(self.config.storageDir, 'audios')

    def create(self, id, audio):
        return self.storage.create(id, audio)

    def read(self, id):
        audioDict = self.storage.read(id)

        if (audioDict != {}):
            return audioDict
        else:
            return False
  
    def update(self, id, audio):
        return self.storage.update(id, audio)

    def delete(self, audio):
        return self.storage.delete(id)

    def readAll(self):
        audios = []

        for dict in self.storage.readAll():
            audios.append(Audio(dict))

        return audios
