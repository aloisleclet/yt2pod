#!/bin/bash

# dependencies
sudo apt-get install -y python3
sudo apt-get install -y pip
sudo apt-get install -y ffmpeg 
sudo apt-get install -y apache2
sudo apt-get install -y jq
sudo apt-get install -y cron

# pip dependencies
pip install yt-dlp --break-system-packages
pip install jsonpickle --break-system-packages

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

rootPath="/var/www/html/yt2pod"
currentPath=$(pwd)

mkdir ${rootPath} || exit
audioDir="${rootPath}/audios"
mkdir ${audioDir} || exit

touch "${rootPath}/feed.xml" || exit
touch "${currentPath}/storage.json" || exit
touch "${currentPath}/yt2pod.conf" || exit

feedPath="${rootPath}/feed.xml"
storagePath="${currentPath}/storage.json"

echo "create ${audioDir}"
echo "create ${feedPath}"
echo "create ${storagePath}"

# set rights

chmod +x "${feedPath}"
chmod +x "${storagePath}"
chmod +x "${audioDir}"
chmod +x ./src/yt2pod
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
