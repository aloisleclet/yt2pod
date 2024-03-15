from Config import Config

class RSSHelper:
    def __init__(self):
        self.config = Config()

        self.lang = "us-en"

    def createEpisode(self, audio):

        episode = """\n\t\t<item>
\t\t\t<title>{title}</title>
\t\t\t<link>{link}</link>
\t\t\t<enclosure url="{link}" type="audio/mpeg"/>
\t\t\t<description>{description} upload {uploadDate}</description>
\t\t</item>\n""".format(title = audio.title, link = audio.url, description = audio.description, uploadDate = audio.uploadDate)
        return episode

    def build(self, feed, audios):


        rss = """<?xml version='1.0' encoding='UTF-8'?>
<rss version='2.0'>
\t<channel>
\t\t<title>{title}</title>
\t\t<link>{url}</link>
\t\t<description>{description}</description>
\t\t<language>{lang}</language>""".format(title = feed.channelName, url = feed.url, description = feed.description, lang = self.lang)
        
        for audio in audios:
            rss += self.createEpisode(audio)
        
        rss += "\t</channel>\n</rss>"
       
        path = "{path}/{name}.xml".format(path = self.config.rssDir, name = feed.channelName)

        with open(path, "w+") as f:
            f.write(rss)
