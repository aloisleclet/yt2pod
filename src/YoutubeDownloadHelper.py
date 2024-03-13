import yt_dlp
import json
import jsonpickle
import datetime

class YoutubeDownloadHelper:
    def __init__(self):
        pass

    def getLastNUrlFromChannel(self, n, channel):
        urls = [] 

        print("Get last {n} video urls from {url}".format(url = channel.url, n = n))
        with yt_dlp.YoutubeDL({'outtmpl': '%(id)s%(ext)s', 'quiet': True, 'max_downloads': n, 'playlistend': n}) as ydl:
            url = "{url}/videos".format(url = channel.url)
            dict = ydl.extract_info(url, download=False)

            for entry in dict['entries']:
                url = "https://www.youtube.com/?v={id}".format(id = entry['id'])
                urls.append(url)
        return urls

    def getDataFromUrl(self, url):
        ydl_opts = {
            'quiet': True,
            'format': 'mp3/bestaudio/best',
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            v = ydl.extract_info(url, download=False)
            data = ydl.sanitize_info(v)

            size = int(data['filesize'] / 1000000)

            # process upload date str to datetime obj
            y = int(data['upload_date'][0:4]) 
            m = int(data['upload_date'][4:6]) 
            d = int(data['upload_date'][6:]) 

            uploadDatetime = datetime.datetime(y, m, d)

            datas = {'id': data['id'], 'title': data['title'], 'channelUrl': data['channel_url'], 'uploadDatetime': uploadDatetime, 'description': data['description'], 'duration': data['duration_string'], 'size': size} 
            return (datas)

    def downloadAudioFromUrl(self, url, destDir):
        ydl_opts = {
            'quiet': True,
            'format': 'mp3/bestaudio/best',
            'outtmpl': '{destDir}/%(id)s'.format(destDir = destDir),
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3'
            }]
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download([url])

