import requests,os,time
from settings import MUSIC_PATH
from settings import IMAGE_PATH
from settings import MONGO_DB

base_url = "http://audio.xmcdn.com/"
url = "http://m.ximalaya.com/m-revision/page/track/queryTrackPage/%s"

content_list = ["/ertong/424529/7713660","/ertong/424529/7713675",
                "/ertong/424529/7713577","/ertong/424529/7713571",
                "/ertong/424529/7713546","/ertong/424529/7713539"]

def xiaopapa(clist):

    my_content = []

    for i in clist:
        audio_id = i.rsplit("/",1)[-1]

        res = requests.get(url%(audio_id))

        res_dict = res.json().get("data").get("trackDetailInfo").get("trackInfo")

        cover_url = base_url + res_dict.get("cover")
        audio_url = res_dict.get("playPath")
        audio = requests.get(audio_url)
        cover = requests.get(cover_url)

        from uuid import uuid4

        filename = uuid4()
        image = os.path.join(IMAGE_PATH,f"{filename}.jpg")
        music = os.path.join(MUSIC_PATH,f"{filename}.mp3")

        with open(music,"wb") as f:
            f.write(audio.content)

        with open(image,"wb") as cf:
            cf.write(cover.content)

        muisc_info = {
            "title":res_dict.get("title"),
            "intro":res_dict.get("intro"),
            "cover":f"{filename}.jpg",
            "audio":f"{filename}.mp3",
        }

        my_content.append(muisc_info)
        time.sleep(1)


    MONGO_DB.content.insert_many(my_content)


xiaopapa(content_list)