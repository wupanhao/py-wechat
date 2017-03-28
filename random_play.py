#!/usr/bin/python
#coding:utf-8
#Copyright:Panhao Wu
#Author:EkingHao
#Date:2016-12-24
#Version:1.0
import os
import argparse
import random
import subprocess
import thread
import re
def getfiles(rootDir, level=1): 
	global lists
#	if level==1: print rootDir 
	for item in os.listdir(rootDir): 
		path = os.path.join(rootDir, item) 
		if os.path.isdir(path): 
			getfiles(path, level+1) 
		else :
			lists.append(path)
	return lists

def search(lists,s):
	suggestions = []
        pattern = '.*'.join(s) # Converts 'djm' to 'd.*j.*m'
        regex = re.compile(pattern)     # Compiles a regex.
        for item in lists:
            match = regex.search(item)  # Checks if the current item matches the regex.
            if match:
#                suggestions.append((len(match.group()), match.start(), item))
		suggestions.append(item)
	if suggestions:
		return suggestions
	else :
		return lists
parser = argparse.ArgumentParser(description="play a song randomly")
parser.add_argument("-p","--path",help="the path of music directory")
parser.add_argument("-s","--search",help="the search string")
args=parser.parse_args()
if  args.path:
	lists=[]
	musics=[]
	getfiles(args.path)
	for item in lists:
		if os.path.splitext(item)[1]==".mp3":
			musics.append(item)
#		print os.path.splitext(item)	
#	print musics
	if args.search:
		musics=search(musics,args.search)
	n = random.randint(0,len(musics))
	music = musics[n]
	
	print music
#	print music.replace(' ','\ ')
#	os.system("nohup killall omxplayer.bin &")
#	subprocess.call("nohup killall omxplayer.bin &  ",shell=True)
#	subprocess.call("nohup  omxplayer " + music.replace(' ','\ ') + " &",shell=True)
else:
	print "please specify the directory!"
	print args.path
