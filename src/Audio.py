class Audio:
    def __init__(self, videoUrl, path, url, channel, title, uploadDatetime, description, duration, size):
        self.videoUrl = videoUrl
        self.path = path
        self.url = url

        self.channel = channel
        self.title = title
        self.uploadDatetime = uploadDatetime
        self.description = description
        self.duration = duration
        self.size = size
