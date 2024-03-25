from Config import Config
from Helpers.UtilsHelper import UtilsHelper

class RSSHelper:
    def __init__(self):
        self.config = Config()
        self.utils = UtilsHelper()
        self.lang = "us-en"

    def createEpisode(self, audio):

        title = self.utils.xmlEscape(audio.title)
        description = self.utils.xmlEscape(audio.description)
        

        episode = """\n\t\t<item>
\t\t\t<title>{title}</title>
\t\t\t<link>{link}</link>
\t\t\t<enclosure url="{link}" type="audio/mpeg"/>
\t\t\t<description>{description} upload {uploadDate}</description>
\t\t</item>\n""".format(title = title, link = audio.url, description = description, uploadDate = audio.uploadDate)
        return episode

    def build(self, feed, audios):

        title = self.utils.xmlEscape(feed.channelName)
        description = self.utils.xmlEscape(feed.description)

        rss = """<?xml version='1.0' encoding='UTF-8'?>
<rss version='2.0'>
\t<channel>
\t\t<title>{title}</title>
\t\t<link>{url}</link>
\t\t<description>{description}</description>
\t\t<language>{lang}</language>""".format(title = title, url = feed.url, description = description, lang = self.lang)
       
        audios.reverse()

        for audio in audios:
            rss += self.createEpisode(audio)
        
        rss += "\t</channel>\n</rss>"
       
        path = "{path}/{name}.xml".format(path = self.config.rssDir, name = feed.channelName)

        with open(path, "w+") as f:
            f.write(rss)
