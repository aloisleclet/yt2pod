import os

class Config:
    def __init__(self):
        self.configFile = "../yt2pod.conf"

        self.rssFile = ""
        self.storageFile = ""
        self.storageMaxSize = 0 #in MB
        self.audioDir = ""
        self.rootUrl = ""
        self.updateLastAudioN = 0

        self.readFile(self.configFile)

    def readFile(self, configPath):

        # read config file
        with open(configPath, "r") as f:
            lines = f.readlines()
            
            # parse config file
            for line in lines:
                l = line.split(":")
                key = l[0]
                value = l[1].strip().replace('\\n', '')

                if (key == 'rssFile'):
                    self.rssFile = value
                elif (key == 'storageFile'):
                    self.storageFile = value
                elif (key == 'audioDir'):
                    self.audioDir = value
                elif (key ==  'serverPublicUrl'):
                    self.rootUrl = value
                elif (key ==  'updateLastN'):
                    self.updateLastAudioN = int(value)
                elif (key ==  'storageMaxSize'):
                    self.storageMaxSize = int(value)

