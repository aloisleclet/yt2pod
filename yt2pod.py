#!/bin/python3

import random
import subprocess
import sys

destPath = "/var/www/html/yt2pod";

mp3Url = "https://yt2pod.aloisleclet.fr"
rssUrl = "https://yt2pod.aloisleclet.fr/feed.xml"
channelFilePath = sys.argv[1];

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
    <title>personnal podcast | RSS</title>
    <link>https://www.youtube.com/</link>
    <description>personnal podcast RSS</description>
    <language>fr-fr</language>"""
   
    for rssEp in rssEps:
        rss += rssEpGen(rssEp)
    
    rss += "\t</channel>\n</rss>"
    
    with open('./files/feed.xml', 'w') as f:
        f.write(rss)

# main

#for each channel url get 10 last video url

def getLastUrls(channels, n):
    urls = [];

    for url in channels:
        print("extract recent videos from {url}".format(url = url))
        command = "yt-dlp --no-warning --playlist-end {n} {url} -j | jq -r .webpage_url".format(url = url, n = n)

        output = subprocess.check_output(command, shell=True)
        lines = str(output.decode("utf-8")).split("\n");

        for line in lines:
            if (line.count("https://www.youtube.com") > 0):
                urls.append(line);
 
    print(urls);
    return (urls)

def getDataFromUrl(url):
    command = "yt-dlp {url} --print '%(channel)s - %(duration>%H:%M:%S)s - %(title)s - %(title)s.mp3'".format(url = url)
    print(command)
    output = subprocess.check_output(command, shell=True)
    datas = str(output.decode("utf-8")).split(" - ")
    title = datas[2]+" "+datas[1]
    link = "{mp3Url}/{filename}".format(mp3Url = mp3Url, filename = datas[3])
    description = datas[0]
    return ({"title": title, "link": link, "description": description})

def download(urls):
    random.shuffle(urls);
    for url in urls:
        print("extract audio from {url}".format(url = url))
        command = "yt-dlp --extract-audio --audio-format mp3 {url} -o '{dest}/%(title)s.%(ext)s'".format(url = url, dest = destPath)
        print(command)
        output = subprocess.check_output(command, shell=True)
       
        # get datas for rss 
        data = getDataFromUrl(url)
        rssEps.append(data)

channels = getChannels()
videoUrls = getLastUrls(channels, 10)

download(videoUrls)
rssGen()
