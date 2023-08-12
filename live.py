import sys, json, requests;
from os.path import exists, realpath, dirname, join;
from configparser import ConfigParser;
from setup import *;

# Only necessary to set default encoding in Python 2.* - doesn't work on Python 3.*
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except Exception:
    pass

config_object = ConfigParser()

config_path = join(dirname(realpath(__file__)), 'config.ini')

# Run setup from setup.py if config hasn't been created
if not exists(config_path):
    runSetup()

config_object.read(config_path)

config = config_object["config"]
accessToken = config["accessToken"]
clientId = config["clientId"]
userId = config["userId"]

# Define headers
headers = {
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Client-ID': clientId,
    'Authorization': 'Bearer ' + accessToken,
}
try:
    response = requests.get('https://api.twitch.tv/helix/streams/followed?user_id=' + userId, headers=headers)

    data = response.json()
    numStreams = len(data["data"])

except (KeyError, ValueError):
    print("Error - make sure the config is configured correctly.")
    sys.exit(1)

for i in range (0, numStreams):
    channelName = data["data"][i]["user_name"];
    channelGame = data["data"][i]["game_name"];
    channelTitle = data["data"][i]["title"];
    channelViewers = str(data["data"][i]["viewer_count"]);
    streamType = data["data"][i]["type"];

    # Check if stream is actually live or VodCast
    if(streamType != "live"):
        continue

    #Formatting
    print ("{}\t{}\t{}\t{}".format(
	channelName,
	channelGame,
    channelTitle,
	channelViewers
    ))
