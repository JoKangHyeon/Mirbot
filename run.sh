NOW=$(date +"%Y%m%d%H%M%S")
nohup python3 -u DiscordCore.py > logs/$NOW.log &
