import os
import sys

class Config:
    def __init__(self):

        self.rssDir = ""
        self.storageDir = ""
        self.audioDir = ""
        self.storageMaxSize = 0 #in MB
        self.serverPublicUrl = ""
        self.updateLastAudioN = 0

        
        self.configFile = self.getConfigPath()
        self.readFile(self.configFile)
        

    def getConfigPath(self):
        path = "{root}/yt2pod.conf".format(root = '/'.join(sys.argv[0].split("/")[0: -2]))
        return path

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

