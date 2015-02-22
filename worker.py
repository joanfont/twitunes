#!/usr/bin/python

from Foundation import *
from ScriptingBridge import *
import threading
import twitter

from utils import md5
import config


iTunes = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
twitter = twitter.Api(**config.TWITTER_CONFIG)

previous = None

def itunes_checker():

	global previous

	title = iTunes.currentTrack().name()
	artist = iTunes.currentTrack().artist()
	album = iTunes.currentTrack().album()

	info = {'title': title, 'artist': artist, 'album': album}

	song = '#nowplaying {title} - {artist} [{album}]'.format(**info)
	hashed = md5(song)

	if hashed != previous:
		previous = hashed
		twitter.PostUpdate(song)


		

def worker(interval, fnx):
  threading.Timer(interval, worker, [interval, fnx]).start()
  fnx()


if __name__ == '__main__':
	worker(1, itunes_checker)
