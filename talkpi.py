#!/usr/bin/python
#coding:utf-8
#Copyright:Panhao Wu
#Author:EkingHao
#Date:2016-10-03
#Version:1.0
import os
import thread
import time
import argparse
import socket, fcntl, struct

def get_local_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))
        ret = socket.inet_ntoa(inet[20:24])
        return ret

parser = argparse.ArgumentParser(description="connect to another raspberrypi and talk with it")
#group = parser.add_mutually_exclusive_group()
parser.add_argument("-t","--test",action="store_true",help="test on local")
parser.add_argument("-lp","--localport",type=int,default=2333,help="local port to open,defaul 2333")
parser.add_argument("-i","--interface",default="eth0",help="by which you connect to host,such as wlan0,eth0")
parser.add_argument("--host",help="host to connect")
parser.add_argument("-u","--user",default="pi",help="user name to login with")
parser.add_argument("-k","--killall",action="store_true",help="kill all nc progress")
#parser.add_argument("-p","--port",type=int,default=2333,help="host port to open,default 2333")
#parser.add_argument("-pw","--passwd",action="store_true",help="use password")
args=parser.parse_args()

if args.killall:
	os.system("killall nc")
if args.test:
	r = os.system("arecord -D plughw:1,0 | aplay")
	if not r:
		print("test on local,now you can speak to your self to see if you can hear from the speaker ")
		print("press Ctrl-C to stop test")
elif args.host:
	localip=get_local_ip(args.interface)
	print localip
	#os.system("nc  %s 80 " % localip)
	#quit()
	print("try to open local port %s" % (args.localport))
	cmd="arecord -D plughw:1,0 | nc -l %s | aplay" % (args.localport)
	thread.start_new_thread(os.system,(cmd,))
	#time.sleep(1)
	print("try to login host %s and connect to local on port %s" %(args.host,args.localport) )
	cmd='ssh %s@%s "arecord -D plughw:1,0 | nc  %s %s | aplay"' % (args.user,args.host,localip,args.localport)
	os.system(cmd)
#	thread.start_new_thread(os.system,(cmd,))
#	time.sleep(5)
else :
	print("you must enter a host ip address,run like  'python %s --host 172.16.xxx.xxx'" % (__file__))

