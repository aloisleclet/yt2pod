import yt_dlp
import json
import jsonpickle
import datetime

class YoutubeDownloadHelper:
    def __init__(self):
        pass

    def getLastNVideoIdFromChannel(self, n, channel):
        ids = [] 

        print("Get last {n} video urls from {url}".format(url = channel.url, n = n))
        with yt_dlp.YoutubeDL({'outtmpl': '%(id)s%(ext)s', 'quiet': True, 'max_downloads': n, 'playlistend': n}) as ydl:
            url = "{url}/videos".format(url = channel.url)
            dict = ydl.extract_info(url, download=False)

            for entry in dict['entries']:
                print(entry['is_live'])
                if (entry['is_live'] == 'False'):
                    print("https://www.youtube.com/{id}".format(id = entry['id']))
        return ids

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

            datas = {'id': data['id'], 'title': data['title'], 'channelUrl': data['channel_url'], 'uploadDate': data['upload_date'], 'description': data['description'], 'duration': data['duration_string'], 'size': size} 
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

