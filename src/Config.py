import os

class Config:
    def __init__(self):
        self.configFile = "../yt2pod.conf"

        self.rssDir = ""
        self.storageDir = ""
        self.audioDir = ""
        self.storageMaxSize = 0 #in MB
        self.serverPublicUrl = ""
        self.updateLastAudioN = 0

        self.readFile(self.configFile)

    def readFile(self, configPath):

        # read config file
        with open(configPath, "r") as f:
            lines = f.readlines()
            
            # parse config file
            for line in lines:
                l = line.split(":", 1)
                key = l[0]
                value = l[1].strip().replace('\\n', '')

                if (key == 'rssDir'):
                    self.rssDir = value
                elif (key == 'storageDir'):
                    self.storageDir = value
                elif (key == 'audioDir'):
                    self.audioDir = value
                elif (key == 'serverPublicUrl'):
                    self.serverPublicUrl = value
                elif (key == 'updateLastN'):
                    self.updateLastAudioN = int(value)
                elif (key == 'storageMaxSize'):
                    self.storageMaxSize = int(value)

