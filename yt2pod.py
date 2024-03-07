#!/bin/python3

import random
import subprocess
import sys

ytdlpPath = "/usr/local/bin"
destPath = "/var/www/html/yt2pod";

channelFilePath = sys.argv[1]
rootUrl = sys.argv[2]

rssEps = [];


def rssEpGen(data):
    print("generate episode: {title}".format(title = data['title']))

    ep = """\t\n<item>
\t<title>{title}</title>
\t\t<link>{link}</link>
\t\t<description>{description}</description>
\t</item>\n""".format(title = data['title'], link = data['link'], description = data['description'])

    return (ep)

def getChannels():
    channels = [];
    with open(channelFilePath) as f:
        lines = f.readlines()
        for line in lines:
            channels.append(line[:-1] + "/videos")
    print("read {n} channels".format(n = len(channels)))
    return channels

def rssGen():
    rss = """<?xml version='1.0' encoding='UTF-8'?>
    <rss version='2.0'>
    <channel>
    <title>yt 2 podcast</title>
    <link>{link}</link>
    <description>youtube 2 podcast micro service</description>
    <language>fr-fr</language>""".format(link = rootUrl)
   
    for rssEp in rssEps:
        rss += rssEpGen(rssEp)
    
    rss += "\t</channel>\n</rss>"
    
    filename = "{dest}/feed.xml".format(dest = destPath)
    with open(filename) as f:
        f.write(rss)
# main

#for each channel url get 10 last video url

def getLastUrls(channels, n):
    urls = [];

    for url in channels:
        print("extract recent videos from {url}".format(url = url))
        command = "{path}/yt-dlp --no-warning --playlist-end {n} {url} -j | jq -r .webpage_url".format(url = url, n = n, path = ytdlpPath)

        output = subprocess.check_output(command, shell=True)
        lines = str(output.decode("utf-8")).split("\n");

        for line in lines:
            if (line.count("https://www.youtube.com") > 0):
                urls.append(line);
 
    print(urls);
    return (urls)

def getDataFromUrl(url):
    command = "{path}/yt-dlp {url} --print '%(channel)s - %(duration>%H:%M:%S)s - %(title)s'".format(url = url, path = ytdlpPath)
    print(command)

    channel = data[0]
    duration = data[1]
    title = data[2]
    filename = "{title}.mp3".format(title = title)

    output = subprocess.check_output(command, shell=True)
    datas = str(output.decode("utf-8")).split(" - ")
    title = "{channel} | {title} | {duration}".format(channel = channel, title = title, duration = duration)
    link = "{rootUrl}/{filename}".format(rootUrl = rootUrl, filename = filename)
    description = title + "\n" + link

    return ({"title": title, "link": link, "description": description})

def download(urls):
    random.shuffle(urls);
    for url in urls:
        print("extract audio from {url}".format(url = url))
        command = "{path}/yt-dlp --extract-audio --audio-format mp3 {url} -o '{dest}/%(title)s.%(ext)s'".format(url = url, dest = destPath, path = ytdlpPath)
        print(command)
        output = subprocess.check_output(command, shell=True)
       
        # get datas for rss 
        data = getDataFromUrl(url)
        rssEps.append(data)

channels = getChannels()
videoUrls = getLastUrls(channels, 10)

download(videoUrls)
rssGen()
