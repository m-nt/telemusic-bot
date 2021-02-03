import requests as req
from bs4 import BeautifulSoup as BS
import re as Regex
import time
import os
import sys


def exit(status):
    print(status)
    os._exit(1)


# regexes for code
Find_Sites_Regex = r'a href=\"((https|http)://[a-zA-Z %&0-9/._-]*/)'
Song_Regex = r'((https|http)://[a-zA-Z %+!0-9/._-]*\.mp3)'
Google_Correct_Regex = r'Showing results for:[a-zA-Z0-9<>/ =\"._-]*(\?[a-z0-9A-Z=&;:%+]*)'

# exeptions
exeptions = ["https://www.mp3", "http://www.mp3"]


# SearchKey = "دانلود آهنگ داریوش"
Header = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",

    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'scheme': 'https'
}

# create Session
session = req.Session()
session.headers.update(Header)


def RunExeptions(stre):
    str, hip = stre
    hip += ""
    for i in exeptions:
        if i == str:
            return ""
    return str


def GetSongsUrl(session, url, timeout):
    try:
        requ = session.get(url, headers=Header, timeout=timeout)
        return (requ.text, requ)
    except req.exceptions.RequestException as e:
        open("log.txt", "a").write("[ERROR]"+str(e)+"\n")
        return ("Not Found", "<Response Failed>")
        #trashcode [0]


def CacheSearch(SearchKey: str):
    key = SearchKey.replace(" ", ".")
    links = {}
    with open("Links.txt", mode="r") as file:
        items = file.read()
    qr = Regex.findall(key, items, flags=Regex.I + Regex.M)
    if len(qr) <= 0:
        return None
    else:
        with open("Links.txt", mode="r") as file:
            items = file.readlines()
        for item in items:
            qr = Regex.findall(key, item, flags=Regex.I + Regex.M)
            if len(qr) > 0:
                result = item.split("[seprator]")
                links[result[0]] = result[1]
    return links


def Search(key: str, cache: bool):
    if cache:
        cachee = CacheSearch(key)
        if cachee != None:
            return cachee
        else:
            return None
    # ******************** resolving the search text ********************
    # top nominated sites
    url = "https://google.com/search?q="+"دانلود آهنگ "+key

    request = session.get(url)
    print(request.status_code)
    if request.status_code == 429:
        return Search(key, cache=False)
    GoogleResult = Regex.findall(Find_Sites_Regex, request.text)

    # ******************** crawling to links to finding songs ********************
    links = {}
    if len(GoogleResult) > 0:
        for i in range(0, len(GoogleResult)):

            site_url, hip = GoogleResult[i]
            # time.sleep(0.5)
            url_for_song, status_code = GetSongsUrl(session, site_url, 2)
            find_song = Regex.findall(Song_Regex, url_for_song)
            leng = 10  # int(sys.argv[2])
            if len(find_song) < leng:
                leng = len(find_song)
            for i in range(0, leng):
                song_url = RunExeptions(find_song[i])
                if song_url != "":
                    songNameDirty = Regex.findall(r'\/([a-zA-Z0-9-_% .]*)\.mp3', song_url)
                    if len(songNameDirty) > 0:
                        songName = Regex.sub(r'[0-9-_% .]+', '_', songNameDirty[0])
                    else:
                        songName = songNameDirty
                    open("Links.txt", "a").write("{}[seprator]{}\n".format(songName, song_url))
                    links[songName] = song_url
    return links
