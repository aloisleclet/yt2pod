from AudioRepository import AudioRepository
from Config import Config

class RSSHelper:
    def __init__(self):
        self.config = Config()
        self.audioRepository = AudioRepository()

        self.title = "yt2pod"
        self.url = self.config.rootUrl
        self.description = "a simple micro service to generate podcast readable rss feed from your favorite youtube channel, and use it from your favorite podcast app"
        self.lang = "us-en"

    def createEpisode(self, audio):

        uploadDateStr = audio['uploadDatetime']

        episode = """\n\t\t<item>
\t\t\t<title>{title}</title>
\t\t\t<link>{link}</link>
\t\t\t<description>{description} upload {uploadDate}</description>
\y\t</item>\n""".format(title = audio['title'], link = audio['url'], description = audio['description'], uploadDate = uploadDateStr)
        return episode

    def build(self):

        audios = self.audioRepository.getAll()

        rss = """<?xml version='1.0' encoding='UTF-8'?>
<rss version='2.0'>
\t<channel>
\t\t<title>{title}</title>
\t\t<link>{url}</link>
\t\t<description>{description}</description>
\t\t<language>{lang}</language>""".format(title = self.title, url = self.url, description = self.description, lang = self.lang)
        
        for audio in audios:
            rss += self.createEpisode(audio)
        
        rss += "\t</channel>\n</rss>"
        
        with open(self.config.rssFile, "w+") as f:
            f.write(rss)
