import urllib, os
import time

print "Warning: This script may not download every single xml file due to possible server errors.  Check the downloads manually when complete to make sure all of them are there and manually download any that are missing.\n\nThis script runs slow on purpose to limit the # of requests to NFL.com to 30 per minute.  You can speed it up by removing the sleep line if you wish, though it's possible your IP may be banned if you have too many requests in a short period of time."

download_folder = "nfl-schedules"
root_url = "http://www.nfl.com/ajax/scorestrip?"

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

def download_xml(season, week, season_type):
    # download xml file schedule from NFL.com
    url = root_url + "season=" + str(season) + "&seasonType=" + season_type + "&week=" + str(week)
    filename = download_folder + "/" + str(season) + "-" + str(week) + "-" + season_type + ".xml"
    urllib.urlretrieve(url, filename)

    # delete file if it contains no games
    file = open(filename, 'r')
    if not "gms" in file.read():
        os.remove(filename)
    file.close()

    # be nice and sleep 2 seconds between requests
    time.sleep(2)

for season in range(1970,2015):
    season_type = "REG"
    for week in range(1,18):
        download_xml(season, week, season_type)
    season_type = "PRE"
    for week in range(1,5):
        download_xml(season, week, season_type)
    season_type = "POST"
    for week in range(15,23):
        download_xml(season, week, season_type)
