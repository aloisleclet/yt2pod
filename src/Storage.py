import json
import jsonpickle
import os
import inspect
from Config import Config
from YoutubeDownloadHelper import YoutubeDownloadHelper

class Storage:
    def __init__(self):
        self.config = Config()
        self.path = self.config.storageFile
        self.data = ''

    # set key value(list)

    def set(self, key, value):
       
        # get current
        audios = self.get('audios')
        channels = self.get('channels')
       
        # replace the
        if key == 'audios':
            audios = value
        elif key == 'channels':
            channels = value
        else:
            print("[ERROR] invalid repo key: {key}".format(key))

        # update

        data = {"storage": {"channels": channels, "audios": audios}}
       
        dataJson = jsonpickle.encode(data, unpicklable=False)
        dataStr = json.dumps(dataJson, indent = 4)

        self.data = dataStr
    
        # write
        with open(self.path, "w+") as f:
            f.write(self.data)

    # get list

    def get(self, key):
        with open(self.path) as f:
            datasJsonStr = json.load(f)
            datas = jsonpickle.decode(datasJsonStr) 

            if (len(datas) == 0):
                datas = {"storage": {"channels": [], "audios": []}}
       
            return datas['storage'][key]

    def clear(self, key):
        self.set(key, []);

    def getSize(self):
        total = 0
        with os.scandir(self.config.audioDir) as it:
            for entry in it:
                total += entry.stat().st_size
        return total / 1000000

