#!/usr/local/bin/python3
""" Grabs all youtube videos in a given quality from https://2020.acmmmsys.org

To work properly this script requires:
  1. Two environment variables set (usr & pwd for attendees which you received from the conference organizers)
    i)  MMSYS2020_USR="..."
    ii) MMSYS2020_PWD="..."
  2. youtube-dl to be installed on your system ex.: `pip3 install youtube-dl`
"""
import os
import sys
import re
from http.client import HTTPSConnection
from base64 import b64encode
import youtube_dl

__author__ = "Dimitri Podborski"
__version__ = "1.0.0"

def getPage():
  usr = os.environ.get('MMSYS2020_USR')
  pwd = os.environ.get('MMSYS2020_PWD')
  if not usr or not pwd:
    print("please set MMSYS2020_USR and MMSYS2020_PWD environment variables")
    return None

  authorization = b64encode((usr+":"+pwd).encode()).decode("ascii")
  requestHeader = { "authorization" : "Basic {}".format(authorization) }
  connection = HTTPSConnection("2020.acmmmsys.org")
  connection.request('GET', '/attendee.php', headers=requestHeader)
  res = connection.getresponse()

  if not res.status == 200:
    print("Could not get the page. HTTP status code = {}".format(res.status))
    return None
  textBytes = res.read()
  return textBytes.decode()

def getYoutubeIDs(pageText):
  # simply search for youtu.be/xxxxsx stuff
  ytIDs = re.findall('https://youtu.be/(.*?)[\"\'\)]', pageText)
  return ytIDs


if __name__ == '__main__':
  pageText = getPage()
  if not pageText:
    sys.exit(1)

  youtubeIDs = getYoutubeIDs(pageText)

  ydl_opts = {
    'format': 'best',
    'container': 'mp4'
  }

  print("Download {} videos".format(len(youtubeIDs)))
  for id in youtubeIDs:
    print("Get: {}".format(id))
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([id])
    