#!/bin/bash

# dependencies
sudo apt-get install ffmpeg
sudo apt-get install apache2
sudo apt-get install git
sudo apt-get install python3
sudo apt-get install jq
sudo apt-get install cron

# pip dependencies
pip install yt-dlp
pip install jsonpickle

# utils

#main


# ask config

updateLastN="10"
storageMaxSize="4000"
serverPublicUrl="https://yt2pod.domain.com"

echo -n "Server public Url of your VPS (ex: https://yt2pod.domain.fr):"
read serverPublicUrl
echo -n "Update channel on X last Videos (ex: 10):"
read updateLastN
echo -n "Max storage Size in MB (ex: 1000):"
read storageMaxSize

# create files and dirs

rootPath=$(pwd)

touch "${rootPath}/feed.xml" || exit
touch "${rootPath}/storage.json" || exit
touch ./yt2pod.conf || exit

audioDir="${rootPath}/audios"
mkdir ${audioDir} || exit

feedPath="${rootPath}/feed.xml"
storagePath="${rootPath}/storage.json"

echo "${audioDir}"
echo "${feedPath}"
echo "${storagePath}"

# set rights

chmod +x "${feedPath}"
chmod +x "${storagePath}"
chmod +x "${audioDir}"
chmod +x ./src/yt2pod.py
chmod +x ./yt2pod.conf

# write config file

echo "rssFile: ${feedPath}" >> ./yt2pod.conf 
echo "storageFile: ${storagePath}" >> ./yt2pod.conf 
echo "audioDir: ${audioDir}" >> ./yt2pod.conf 
echo "serverPublicUrl: ${serverPublicUrl}" >> ./yt2pod.conf 
echo "updateLastN: ${updateLastN}" >> ./yt2pod.conf 
echo "storageMaxSize: ${storageMaxSize}" >> ./yt2pod.conf 

# init storage

echo "\"{\\\"storage\\\": {\\\"channels\\\": [], \\\"audios\\\": []}}\"" > ${storagePath}

echo "Install done."
