from Config import Config

from Helpers.StorageHelper import StorageHelper

from Entities.Feed import Feed

class FeedRepository:
    def __init__(self):
        self.config = Config()
        self.storage = StorageHelper(self.config.storageDir, 'feeds')

    def create(self, id, feed):
        return self.storage.create(id, feed)

    def read(self, id):
        feedDict = self.storage.read(id)
        
        if (feedDict != {}):
            return Feed(feedDict)
        else:
            return False
  
    def update(self, id, feed):
        return self.storage.update(id, feed)

    def delete(self, id):
        return self.storage.delete(id)

    def readAll(self):
        feeds = []

        for dict in self.storage.readAll():
            feeds.append(Feed(dict))

        return feeds
