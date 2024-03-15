from Config import Config

from Repositories.ChannelRepository import ChannelRepository
from Repositories.AudioRepository import AudioRepository
from Repositories.FeedRepository import FeedRepository

from Helpers.YoutubeDownloadHelper import YoutubeDownloadHelper
from Helpers.RSSHelper import RSSHelper
from Helpers.UtilsHelper import UtilsHelper

from Entities.Feed import Feed
from Entities.Audio import Audio
from Entities.Channel import Channel

import datetime
import os

class Core:
    
    def __init__(self):
        self.config = Config()

        self.channelRepository = ChannelRepository()
        self.audioRepository = AudioRepository()
        self.feedRepository = FeedRepository()

        self.ydl = YoutubeDownloadHelper()
        self.rss = RSSHelper()
        self.utils = UtilsHelper()

    def addChannel(self, channelUrl):
        name = channelUrl.split('https://www.youtube.com/')[1]
        channel = Channel({'url':channelUrl, 'name': name})
        self.channelRepository.create(name, channel)
        print('Channel {name} added.'.format(name = name))

    def removeChannel(self, channelName):
        self.channelRepository.delete(channelName)
        print('Channel {name} removed.'.format(name = channelName))

    def listChannel(self):
        channels = self.channelRepository.readAll()

        n = 0

        for channel in channels:
            n += 1
            print('{name}\t{url}'.format(name = channel.name, url = channel.url))

        if (n == 0):
            print("No channel found\n\nAdd channel:\n\t./yt2pod add https://www.youtube.com/@exampleChannel")

    def update(self):
        print('Update in progress')
        
        channels = self.channelRepository.readAll()

        for channel in channels:
            print('Scrap last url from {name}'.format(name = channel.name))
            ids = self.ydl.getLastNVideoIdFromChannel(self.config.updateLastAudioN, channel)
            
            uniqIds = []

            for id in ids:
                if (self.audioRepository.read(id) == False): 
                    uniqIds.append(id)

            for id in uniqIds:
                url = 'https://www.youtube.com/?v={id}'.format(id = id)
                data = self.ydl.getDataFromUrl(url)

                # get current size
                audios = self.audioRepository.readAll()
                currentSize = self.utils.getSizeFromAudios(audios) 
                sizeLeft = int(self.config.storageMaxSize) - currentSize
                fileSize = int(data['size'])
                
                isAudioToDelete = len(audios) > 0 

                while (sizeLeft < fileSize and isAudioToDelete == True):
                    isAudioToDelete = self.dropLastOutdatedAudio() 
                    # update size left
                    audios = self.audioRepository.readAll()
                    currentSize = self.utils.getSizeFromAudios(audios) 
                    sizeLeft = int(self.config.storageMaxSize) - currentSize

                if (sizeLeft < fileSize):
                    print('Error: {url} Storage Max Size < file Size'.format(url = url))
                    return
                # add the new audio
               
                print('Download {url}'.format(url = url))
                # create audio Object
                title = data['title']
                path = "{audioDir}/{id}.mp3".format(audioDir = self.config.audioDir, id = data['id'])
                rssUrl = "{serverPublicUrl}/audios/{id}.mp3".format(serverPublicUrl = self.config.serverPublicUrl, id = data['id'])

                description = data['description']
                uploadDate = data['uploadDate']
                duration = data['duration']
                size = data['size'] 

                audio = Audio({'id': id, 'path': path, 'url': rssUrl, 'channelName': channel.name, 'title': title, 'uploadDate': uploadDate, 'description': description, 'duration': duration, 'size': size}) 
               
                self.audioRepository.create(id, audio)
                self.ydl.downloadAudioFromUrl("https://www.youtube.com/?v={id}".format(id = id), self.config.audioDir)

            feed = self.feedRepository.read(channel.name)

            if (feed == False):
                url = "{serverPublicUrl}/feeds/{name}.xml".format(serverPublicUrl = self.config.serverPublicUrl, name = channel.name)
                feed = Feed({"url": url, "channelName": channel.name, "description": channel.description})
                self.feedRepository.create(channel.name, feed)

            # get audios to generate feed file

            feedsAudios = []
            audios = self.audioRepository.readAll()

            for audio in audios:
                if (audio.channelName == feed.channelName):
                    feedsAudios.append(audio)

            self.rss.build(feed, feedsAudios)
        
        print('Update complete.');

    def dropLastOutdatedAudio(self):
        audios = self.audioRepository.readAll()

        if (len(audios) == 0):
            return False

        # find oldest 
        oldestAudio = Audio({'id': '', 'path': '', 'url': '', 'channelName': '', 'title': '', 'uploadDate': datetime.datetime.now().strftime("%Y%m%d"), 'description': '', 'duration': '', 'size': ''})

        for audio in audios:

            d1 = self.utils.strToDate(audio.uploadDate)
            d2 = self.utils.strToDate(oldestAudio.uploadDate)
          
            if (d1 < d2):
                oldestAudio = audio
       
        if (oldestAudio.uploadDate == datetime.datetime.now().strftime("%Y%m%d")):

            print(audios)
            oldestAudio = audios[0]

        # drop it 
        print ("Storage Max Size overflow: removing {path}".format(path = oldestAudio.path))
        self.audioRepository.delete(oldestAudio.id)
        os.remove(oldestAudio.path)

        return True
