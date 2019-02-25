from settings import SPEECH,VOICE,CHATS_PATH,MONGO_DB
from uuid import uuid4
from bson import ObjectId
from ai.to_tuling import tuling
import os
from pypinyin import lazy_pinyin,TONE2
from my_simnet import my_simnet


def text2audio(text):
    filename = f"{uuid4()}.mp3"
    result = SPEECH.synthesis(text, 'zh', 1,VOICE)
    file_path = os.path.join(CHATS_PATH,filename)

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open(file_path, 'wb') as f:
            f.write(result)

    return filename


def get_file_content(filePath):
    os.system(f"ffmpeg -y  -i {filePath} -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filePath}.pcm")
    with open(f"{filePath}.pcm", 'rb') as fp:
        return fp.read()

def audio2text(filepath):
    # 识别本地文件
    res = SPEECH.asr(get_file_content(filepath), 'pcm', 16000, {
        'dev_pid': 1536,
    })

    print(res.get("result")[0])

    return res.get("result")[0]


def my_nlp_lowB(Q,nid):
    # Q = 我要给爸爸发消息
    if "发消息" in Q:
        pinyin_Q = "".join(lazy_pinyin(Q, style=TONE2))
        toy = MONGO_DB.toys.find_one({"_id":ObjectId(nid)})
        for friend in toy.get("friend_list"):
            pinyin_nick = "".join(lazy_pinyin(friend.get("friend_nick"),style=TONE2))
            pinyin_name = "".join(lazy_pinyin(friend.get("friend_name"),style=TONE2))
            if pinyin_nick in pinyin_Q or pinyin_name in pinyin_Q :
                xs = f"可以按消息建给{friend.get('friend_nick')}发消息了"
                filename = text2audio(xs)
                return {"chat":filename,
                        "from_user":str(friend.get("friend_id")),
                        "friend_type":friend.get("friend_type")}

    # Q = 我要听小毛驴 我想听小毛驴 播放小毛驴
    if "我要听" in Q or "我想听" in Q or "播放" in Q :
        title = my_simnet(Q)
        if title:
            content = MONGO_DB.content.find_one({"title":title})
            return {"music":content.get("audio"),"from_user":"ai"}

    # if nlp.simnet("你是谁",Q).get("score")>0.68:
    #     xs = f"可以按消息建给{friend.get('friend_nick')}发消息了"
    #     filename = text2audio(xs)
    #     return {"chat": filename,
    #             "from_user": str(friend.get("friend_id")),
    #             "friend_type": friend.get("friend_type")}

    text = tuling(Q,nid)
    filename = text2audio(text)

    return {"chat": filename, "from_user": "ai"}


def _get_xxtx(to_user,from_user,recv=False):
    to_user_info = MONGO_DB.toys.find_one({"_id":ObjectId(to_user)})
    for friend in to_user_info.get("friend_list"):
        if friend.get("friend_id") == from_user:
            if recv:
                xxtx_str = f"以下是来自{friend.get('friend_nick')}的消息"
                filename = text2audio(xxtx_str)
                return filename

            xxtx_str = f"你有来自{friend.get('friend_nick')}的新消息"
            filename = text2audio(xxtx_str)
            return filename

    xxtx_str = f"你有来自陌生人的消息"
    filename = text2audio(xxtx_str)
    return filename
