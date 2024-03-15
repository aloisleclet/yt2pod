class Audio:
    def __init__(self, audioDict):
        self.id = audioDict['id']
        self.path = audioDict['path']
        self.url = audioDict['url']

        self.channelName = audioDict['channelName']
        self.title = audioDict['title']
        self.uploadDate = audioDict['uploadDate']
        self.description = audioDict['description']
        self.duration = audioDict['duration']
        self.size = audioDict['size']
