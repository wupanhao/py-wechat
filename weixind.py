#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import web
import time
import hashlib
import subprocess
import thread
from lxml import etree
 
 
urls = (
'/weixin','WeixinInterface'
)

def _check_hash(data):
    #sha1加密算法
    signature=data.signature
    timestamp=data.timestamp
    nonce=data.nonce
    #自己的token
    token="wph" #这里改写你在微信公众平台里输入的token
    #字典序排序
    list=[token,timestamp,nonce]
    list.sort()
    sha1=hashlib.sha1()
    map(sha1.update,list)
    hashcode=sha1.hexdigest()
    #如果是来自微信的请求，则回复True
    if hashcode == signature:
        return True
    return False


class WeixinInterface:

    def reply(self,xml):
        content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        msg=content.split(" ",1)
        if msg[0] == "cmd":
		#if len(msg)>=2:
		stdout=subprocess.check_output(msg[1],shell=True)
#                print stdout
                return self.render.reply_text(fromUser,toUser,int(time.time()),stdout)
	elif msg[0] == "speak":
		stdout=thread.start_new_thread(os.system,("nohup ssh pi@localhost  python speak.py  " +  msg[1] +" &",))
		#stdout=subprocess.check_output("nohup ssh pi@localhost  python speak.py  " +  msg[1] + " &",shell=True)
		stdout="I have tried  to send this message "
		return self.render.reply_text(fromUser,toUser,int(time.time()),stdout)
	elif msg[0] == "random":
		subprocess.call("killall omxplayer.bin",shell=True)
		if len(msg) > 1:
			music=subprocess.check_output("python /home/pi/random_play.py -p /home/pi/kugou -s " + msg[1],shell=True)[:-1]
		else :
			music=subprocess.check_output("python /home/pi/random_play.py -p /home/pi/kugou ",shell=True)[:-1]
		stdout=thread.start_new_thread(os.system,('nohup  omxplayer "' + music + '" &',))
		return self.render.reply_text(fromUser,toUser,int(time.time()),music + "\n is on playing")
        else:
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"暂未定义的指令："+content+'''
\nUsage:
1):cmd + [shell command]
2):speak + [\\"the words you want to say \\"]
More to be added
''')


 
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
 
    def GET(self):
        #获取输入参数
	data = web.input()
	print data
        if _check_hash(data):
            return data.echostr

    def POST(self):        
        str_xml = web.data() #获得post来的数据
#	print str_xml
        xml = etree.fromstring(str_xml)#进行XML解析
        content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
	return self.reply(xml)
        #return self.render.reply_text(fromUser,toUser,int(time.time()),u"接收到的文字："+content) 

application = web.application(urls, globals())
if __name__ == "__main__":
    application.run()
