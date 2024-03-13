from ChannelRepository import ChannelRepository
from AudioRepository import AudioRepository
from Config import Config

from YoutubeDownloadHelper import YoutubeDownloadHelper
from RSSHelper import RSSHelper

from Storage import Storage
from Audio import Audio
from Channel import Channel

import datetime
import os

class Core:
    
    def __init__(self):
        self.channelRepository = ChannelRepository()
        self.audioRepository = AudioRepository()

        self.config = Config()
        self.ydl = YoutubeDownloadHelper()
        self.rss = RSSHelper()
        self.storage = Storage()

    def addChannel(self, channelUrl):
        name = channelUrl.split('https://www.youtube.com/')[1]
        channel = Channel(channelUrl, name)
        self.channelRepository.add(channel)
        print('Channel {name} added.'.format(name = name))

    def removeChannel(self, channelName):
        self.channelRepository.removeByName(channelName)
        print('Channel {name} removed.'.format(name = channelName))

    def listChannel(self):
        channels = self.channelRepository.getAll()

        for channel in channels:
            print('{name}\t{url}'.format(name = channel.name, url = channel.url))

    def update(self):
        print('Update in progress')
        
        channels = self.channelRepository.getAll()

        for channel in channels:
            print('Scrapping last url from {name}'.format(name = channel.name))
            urls = self.ydl.getLastNUrlFromChannel(self.config.updateLastAudioN, channel)
            
            # filter urls to avoid duplicate

            urlsFiltered = []

            for url in urls:
                if (self.audioRepository.getByUrl(url) == 0): 
                    urlsFiltered.append(url)

            for url in urlsFiltered:
                print('Downloading {url}'.format(url = url))
                data = self.ydl.getDataFromUrl(url)

                while (data['size'] + self.storage.getSize() > self.config.storageMaxSize):
                    self.dropLastOutdatedAudio() 

                # add the new audio
               
                # create audio Object
                title = data['title']
                path = "{audioDir}/{id}.mp3".format(audioDir = self.config.audioDir, id = data['id'])
                rssUrl = "{rootUrl}/{id}.mp3".format(rootUrl = self.config.rootUrl, id = data['id'])

                description = data['description']
                uploadDatetime = data['uploadDatetime']
                duration = data['duration']
                size = data['size'] 

                audio = Audio(url, path, rssUrl, channel, title, uploadDatetime, description, duration, size) 
                
                self.audioRepository.add(audio)
                self.ydl.downloadAudioFromUrl(url, self.config.audioDir)

        self.rss.build()
        print('Update complete.');

    def dropLastOutdatedAudio(self):
        audios = self.audioRepository.getAll()

        # find oldest 
        oldestAudio = {'uploadDatetime': datetime.datetime.now().strftime("%Y-%m-%d")}

        for audio in audios:

            d1 = audio['uploadDatetime'][:10].split('-')
            d2 = oldestAudio['uploadDatetime'][:10].split('-')
          
            if (datetime.date(int(d1[0]), int(d1[1]), int(d2[2])) < datetime.date(int(d2[0]), int(d2[1]), int(d2[2]))):
                oldestAudio = audio
        
        if (oldestAudio['uploadDatetime'] == datetime.datetime.now().strftime("%Y-%m-%d")):
            oldestAudio = audios[0]

       # drop it 
        print ("Storage Max Size overflow: removing {path}".format(path = oldestAudio['path']))
        self.audioRepository.removeByUrl(oldestAudio['videoUrl'])
        os.remove(oldestAudio['path'])
