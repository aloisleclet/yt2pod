# script_yt2pod

daily audio of your favorites youtube channel on your favorite podcast app

# how to use

1. install on vps

```
sudo apt-get install ffmpeg
sudo apt-get install apache2
sudo apt-get install git
sudo apt-get install python3
sudo apt-get install jq
sudo apt-get install cron
sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
sudo chmod a+rx ~/usr/local/bin/yt-dlp
cd ~
git clone https://github.com/aloisleclet/script_yt2pod 
```

2. set right

```
cd script_yt2pod
chmod +x script.py
```

3. add your favorite channels
```
vim ./channels.txt
```


4. set cron
```
crontab -e 
0 16 * * mon /home/me/script_yt2pod/yt2pod.py /home/me/script_yt2pod/channels.txt http://yt2pod.yoursite.com
```

5.
```
mkdir /var/www/html/yt2pod
```

6. link your favorite podcast app with the rss feed

7. Enjoy: you now have audio of your favorites channel daily updated.  
