from Storage import Storage
from Config import Config
from Channel import Channel

class ChannelRepository:
    def __init__(self):
        self.storage = Storage()

    def add(self, channel):
        channels = self.storage.get('channels')
        print(channels)
        channels.append(channel)
        self.storage.set('channels', channels)

    # return list<Channel>
    def getAll(self):
        channels = self.storage.get('channels')
        channelsRes = []

        for channelDict in channels:
            channelsRes.append(Channel(channelDict['url'], channelDict['name']))
        
        return channelsRes
   
    def removeByName(self, name):
        data = self.storage.get('channels')
        dataRes = [] 
            
        # filter the named channel
        for channelDict in data:
            channel = Channel(channelDict['url'], channelDict['name'])

            if (channel.name != name):
                dataRes.append(channel) 

        self.storage.set('channels', dataRes)
