# -*- coding: utf-8 -*-

from Foundation import *
from ScriptingBridge import *
import threading
import twitter

from utils import md5
import config


iTunes = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
twitter = twitter.Api(**config.TWITTER_CONFIG)

previous = None

def construct_string(info):
  base = u'#nowplaying'
  string = u'{base}'.format(base = base)
  if info.get('title'):
    string += u' {title}'.format(title = info.get('title'))

  if info.get('artist'):
    string += u' - {artist}'.format(artist = info.get('artist'))

  if info.get('album'):
    string += u' [{album}]'.format(album = info.get('album'))

  return string if string != base else None

def itunes_checker():

  global previous

  title = iTunes.currentTrack().name()
  artist = iTunes.currentTrack().artist()
  album = iTunes.currentTrack().album()

  info = {'title': title, 'artist': artist, 'album': album}

  song = construct_string(info).encode('utf8')

  if song:
    hashed = md5(song)
    if hashed != previous:
      previous = hashed
      twitter.PostUpdate(song)


    

def worker(interval, fnx):
  threading.Timer(interval, worker, [interval, fnx]).start()
  fnx()


if __name__ == '__main__':
  worker(1, itunes_checker)
