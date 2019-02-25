from flask import Blueprint,jsonify,send_file,request
from settings import MONGO_DB,RET,MUSIC_PATH,IMAGE_PATH,CHATS_PATH,QRCODE_PATH
import os,time
from uuid import uuid4
from ai.baidu import audio2text,my_nlp_lowB

gsa = Blueprint("gsa",__name__)

@gsa.route("/get_image/<filename>")
def get_image(filename):
    file_path = os.path.join(IMAGE_PATH,filename)
    return send_file(file_path)

@gsa.route("/get_qr/<filename>")
def get_qr(filename):
    file_path = os.path.join(QRCODE_PATH,filename)
    return send_file(file_path)

@gsa.route("/get_music/<filename>")
def get_music(filename):
    file_path = os.path.join(MUSIC_PATH,filename)
    return send_file(file_path)

@gsa.route("/get_chat/<filename>")
def get_chat(filename):
    file_path = os.path.join(CHATS_PATH,filename)
    return send_file(file_path)


@gsa.route("/uploader",methods=["POST"])
def uploader():
    audio = request.files.get("recorder")
    to_user = request.form.get("to_user")
    from_user = request.form.get("from_user")
    print(to_user,from_user)
    path = os.path.join(CHATS_PATH,audio.filename)
    audio.save(path)
    os.system(f"ffmpeg -i {path} {path}.mp3")

    # 消息存储记录 chats
    msg_dict = {
        "sender":from_user,
        "msg":f"{audio.filename}.mp3",
        "createtime":time.time()
    }

    MONGO_DB.chats.update_one({"user_list": {"$all": [to_user, from_user]}},
                              {"$push":{"chat_list":msg_dict}})

    RET["code"] = 0
    RET["msg"] = "上传音频文件"
    RET["data"] = {"filename":f"{audio.filename}.mp3"}

    return jsonify(RET)


@gsa.route("/toy_uploader",methods=["POST"])
def toy_uploader():
    audio = request.files.get("record")
    to_user = request.form.get("to_user")
    from_user = request.form.get("from_user")
    filename = f"{uuid4()}.wav"
    path = os.path.join(CHATS_PATH,filename)
    audio.save(path)
    # os.system(f"ffmpeg -i {path} {path}.mp3")

    msg_dict = {
        "sender":from_user,
        "msg":filename,
        "createtime":time.time()
    }

    MONGO_DB.chats.update_one({"user_list": {"$all": [to_user, from_user]}},
                              {"$push":{"chat_list":msg_dict}})

    return jsonify({"code":0,"filename":filename})


@gsa.route("/ai_uploader",methods=["POST"])
def ai_uploader():
    audio = request.files.get("record")
    to_user = request.form.get("to_user")
    from_user = request.form.get("from_user")
    filename = f"{uuid4()}.wav"
    path = os.path.join(CHATS_PATH,filename)
    audio.save(path)
    # os.system(f"ffmpeg -i {path} {path}.mp3")
    Q = audio2text(path)
    ret = my_nlp_lowB(Q,from_user)

    return jsonify(ret)