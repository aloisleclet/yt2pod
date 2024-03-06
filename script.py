#!/bin/python3

import subprocess

mp3Url = "https://yt2pod.aloisleclet.fr/mp3/"
rssUrl = "https://yt2pod.aloisleclet.fr/feed.xml"

def rss_ep(title, link, description):
    ep = """\n<item>
    <title>{title}</title>
    <link>{link}</link>
    <description>{description}</description>
</item>\n""".format(title = title, link = link, description = description)

    return (ep)

# main

# dl and generate rss feed

def rss_gen():
    rss = """<?xml version='1.0' encoding='UTF-8'?>
    <rss version='2.0'>
    <channel>
    <title>personnal podcast | RSS</title>
    <link>https://www.youtube.com/</link>
    <description>personnal podcast RSS</description>
    <language>fr-fr</language>"""
    
    command = "yt-dlp --no-warning --playlist-end 2 https://www.youtube.com/playlist\?list\=PL_eK76Zdjlj5prJrDJjZRi7ZMTObW68px -j | jq -r .webpage_url"
    
    output = subprocess.check_output(command, shell=True)
    
    ids = []
    
    lines = str(output)
    lines = lines.split('\\n')
    
    for line in lines:
        if (line.count("https://www.youtube.com") > 0):
            id = line.split('https://www.youtube.com/watch?v=')[1]
            ids.append(id)
            yt2mp3Command = "yt-dlp --print '%(channel)s - %(duration>%H:%M:%S)s - %(title)s - %(title)s.%(ext)s' -o './files/%(title)s.%(ext)s' --extract-audio --audio-format mp3 https://www.youtube.com/watch?v={id}".format(id = id)
            
            data = subprocess.check_output(yt2mp3Command, shell=True)
            datas = str(data).split(" - ");
            title = datas[2]+" "+datas[1];
            link = "{mp3Url}/{filename}".format(mp3Url = mp3Url, filename = datas[3]);
            description = datas[0][2:]
    
            rss += rss_ep(title, link, description) 
    
    rss += "</channel></rss>"
    
    return (rss)

# write rss feed

with open('./files/feed.xml', 'w') as f:
    f.write(rss_gen())

