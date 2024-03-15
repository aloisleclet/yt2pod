# yt2pod

Generate rss podcast feeds from your favorites youtube channel for your favorite podcast app

# how to use

1. Install on your server

```
cd ~
git clone https://github.com/aloisleclet/yt2pod 
chmod +x ./install.sh
sudo ./install.sh
```

2. link server and your domain

3. Manage your channels

```
./yt2pod add https://www.youtube.com/@underscore_
./yt2pod remove @underscore_
./yt2pod list 
./yt2pod update
./yt2pod help
```

4. Auto update with a cron

```
crontab -e 
0 16 * * mon /path/to/yt2pod/yt2pod update 
```

5. add your RSS feed (ServerPublicUrl) to your favorite podcast app

6. Enjoy
