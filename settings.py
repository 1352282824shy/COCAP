# 目录配置
import os

MUSIC_PATH = "Music"
IMAGE_PATH = "Image"
CHATS_PATH = "Chats"

QRCODE_PATH = "QRcode"


#数据库配置
import pymongo
client = pymongo.MongoClient(host="127.0.0.1",port=27017)
MONGO_DB = client["ChunSheng"]

from redis import Redis
REDIS_DB = Redis(host="127.0.0.1",port=6379,db=10)


#Rest-Api
RET={
    "code":0,
    "msg":"",
    "data":{}
}


# 联图配置：
LT_URL="http://qr.liantu.com/api.php?text=%s"


# baiduAi配置
from aip import AipSpeech,AipNlp

""" 你的 APPID AK SK """
APP_ID = '15420336'
API_KEY = 'VwSGcqqwsCl282LGKnFwHDIA'
SECRET_KEY = 'h4oL6Y9yRuvmD0oSdQGQZchNcix4TF5P'

NLP =  AipNlp(APP_ID, API_KEY, SECRET_KEY)
SPEECH = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

VOICE = {
    'vol': 5,
    "spd": 4,
    "pit": 8,
    "per": 4
}

# 图灵配置:
TULING_STR = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": "%s"
            }
        },
        "userInfo": {
            "apiKey": "9a9a026e2eb64ed6b006ad99d27f6b9e",
            "userId": "%s"
        }
    }

TULING_URL = "http://openapi.tuling123.com/openapi/api/v2"


