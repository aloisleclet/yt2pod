from Config import Config

from Helpers.StorageHelper import StorageHelper

from Entities.Channel import Channel

class ChannelRepository:
    def __init__(self):
        self.config = Config()
        self.storage = StorageHelper(self.config.storageDir, 'channels')

    def create(self, id, channel):
        return self.storage.create(id, channel)

    def read(self, id):
        channelDict = self.storage.read(id)
        return Channel(channelDict)
  
    def update(self, id, channel):
        return self.storage.update(id, channel)

    def delete(self, id):
        return self.storage.delete(id)

    def readAll(self):
        channels = []

        for dict in self.storage.readAll():
            channels.append(Channel(dict))

        return channels
