#coding:utf-8

import os
from urllib import quote
import sys
length = len(sys.argv)
per="0"
pit="5"
spd="5"
tex=quote("master,what can I do for you")
if length>=2:
	tex=quote(sys.argv[1])
if length>=3:
	per=sys.argv[2]
if length>=4:
	pit=sys.argv[3]
if length>=5:
	spd=sys.argv[4]

tok="25.14829744f664fbbd51fec8bcc415abc9.315360000.1797224096.282335-8133661"
url = "http://tsn.baidu.com/text2audio?tex="+tex+"&lan=zh&per="+per+"&pit="+pit+"&spd="+spd+"&cuid=***&ctp=1&tok="+tok
print "try to speak...\n"
#print url
os.system('mpg123 -p "http://172.16.123.238:8118"  "%s" ' %(url))
#tex是要合成的语音内容，per是声音的性别，1是男，0是女，默认是女，pit是音调，spd是语速，调节范围都是1-9，最后的tok是你通过你的id和key获取到的token

#curl https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=lb5xCu4TxlBR3b8gNCUoDhxh&client_secret=4e9f5ece9649f33c52fffec93a375844&
