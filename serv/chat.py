from flask import Blueprint,jsonify,send_file,request
from settings import MONGO_DB,RET,MUSIC_PATH,IMAGE_PATH,CHATS_PATH
from redismsg import get_reids_one,get_redis_all,get_redis_one_toy
import os,time
from uuid import uuid4
from bson import ObjectId

chat = Blueprint("chat",__name__)

@chat.route("/recv_msg",methods=["POST"])
def recv_msg():
    to_user = request.form.get("to_user")
    from_user = request.form.get("from_user")
    count,from_user = get_redis_one_toy(to_user,from_user) # 3

    if MONGO_DB.users.find_one({"_id":ObjectId(from_user)}):
        friend_type = "app"
    else:
        friend_type = "toy"

    chat_window = MONGO_DB.chats.find_one({"user_list":{"$all":[to_user,from_user]}})
    # chat = chat_window.get("chat_list")[-count:]
    chat_list = []
    for chat in reversed(chat_window.get("chat_list")):
        if chat.get("sender") != from_user:
            continue
        chat_list.append(chat)
        if len(chat_list) == count:
            break

    from ai.baidu import _get_xxtx
    xxtx = _get_xxtx(to_user,from_user,True)
    chat_list.append({"msg":xxtx})
    chat_list.reverse()

    ret = {
        "from_user":from_user,
        "friend_type":friend_type,
        "chat_list":chat_list
    }

    return jsonify(ret)


@chat.route("/chat_list",methods=["POST"])
def chat_list():
    to_user = request.form.get("to_user")
    from_user = request.form.get("from_user")

    print(to_user,from_user)
    chat_window = MONGO_DB.chats.find_one({"user_list":{"$all":[to_user,from_user]}})

    get_reids_one(to_user,from_user)

    RET["code"] =0
    RET["msg"] = "查询聊天内容"
    RET["data"] = chat_window.get("chat_list")[-10:]

    return jsonify(RET)


@chat.route("/chat_count",methods=["POST"])
def chat_count():
    user_id = request.form.get("user_id")
    to_user_msg = get_redis_all(user_id)

    RET["code"] = 0
    RET["msg"] = "查询未读消息"
    RET["data"] = to_user_msg

    return jsonify(RET)
