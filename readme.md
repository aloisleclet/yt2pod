# yt2pod

Generate rss podcast feeds from your favorites youtube channel for your favorite podcast app

# how to use

1. Install on your server

```
cd ~
git clone https://github.com/aloisleclet/yt2pod 
chmod +x ./install.sh
./install.sh
```

2. Setup server

```
mkdir /var/www/html/yt2pod
touch /var/www/html/yt2pod/feed.xml
chmod 755 /var/www/html/yt2pod/feed.xml
```

3. link server and your domain

4. Manage your channels

```
./yt2pod.py add https://www.youtube.com/@underscore_
./yt2pod.py remove @underscore_
./yt2pod.py list 
./yt2pod.py update
./yt2pod.py help
```

5. Auto update with a cron

```
crontab -e 
0 16 * * mon /path/to/yt2pod/yt2pod.py update 
```

6. Link your favorite podcast app with the serverPublicUrl

7. Enjoy
