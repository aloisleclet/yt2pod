class Feed:
    def __init__(self, feedDict):
        self.url = feedDict['url']
        self.channelName = feedDict['channelName']
        self.description = feedDict['description']

