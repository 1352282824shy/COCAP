from flask import Blueprint, jsonify, request
from settings import MONGO_DB, RET
from bson import ObjectId

devices = Blueprint("devices", __name__)


@devices.route("/validate_code", methods=["POST"])
def validate_code():
    code = request.form.to_dict()  # {device_key:asdfasdfasdf}
    res = MONGO_DB.devices.find_one(code, {"_id": 0})

    if res:
        RET["code"] = 0
        RET["msg"] = "设备已授权，开启绑定"
        RET["data"] = res
        # 添加好友逻辑
        toy = MONGO_DB.toys.find_one(code)
        if toy:
            toy["_id"] = str(toy.get("_id"))
            RET["code"] = 1
            RET["msg"] = "开启添加好友"
            RET["data"] = toy

    else:
        RET["code"] = 2
        RET["msg"] = "非授权设备"
        RET["data"] = {}

    return jsonify(RET)


@devices.route("/bind_toy", methods=["POST"])
def bind_toy():
    # toys.bind_user = "user_id"
    # users.bind_toy = ["toy_id"]
    # 1.device_key 2.fromdata 3. who bind toy
    toy_info = request.form.to_dict()

    #创建聊天窗口
    chat_window = MONGO_DB.chats.insert_one({"user_list": [], "chat_list": []})

    #通过user_id去查询用户信息 谁绑定玩具
    user_info = MONGO_DB.users.find_one({"_id": ObjectId(toy_info["user_id"])})

    toy_info["bind_user"] = toy_info.pop("user_id")
    toy_info["avatar"] = "toy.jpg"
    #自然逻辑 好友关系
    toy_info["friend_list"] = [
        {
            "friend_id": toy_info["bind_user"],
            "friend_name": user_info.get("nickname"),
            "friend_nick": toy_info.pop("remark"),
            "friend_avatar": user_info.get("avatar"),
            "friend_type": "app",
            "friend_chat": str(chat_window.inserted_id)
        }
    ]

    toy = MONGO_DB.toys.insert_one(toy_info)

    #用户添加绑定玩具 及 自然逻辑 好友关系
    user_info["bind_toy"].append(str(toy.inserted_id))
    user_add_toy = {
        "friend_id": str(toy.inserted_id),
        "friend_name": toy_info.get("toy_name"),
        "friend_nick": toy_info.get("baby_name"),
        "friend_avatar": toy_info.get("avatar"),
        "friend_type": "toy",
        "friend_chat": str(chat_window.inserted_id)
    }

    user_info["friend_list"].append(user_add_toy)

    MONGO_DB.users.update_one({"_id": ObjectId(toy_info["bind_user"])}, {"$set": user_info})
    MONGO_DB.chats.update_one({"_id": chat_window.inserted_id}, {"$set": {
        "user_list": [str(toy.inserted_id), str(user_info.get("_id"))]
    }})

    RET["code"] = 0
    RET["msg"] = "绑定玩具成功"
    RET["data"] = {}

    return jsonify(RET)


@devices.route("/toy_list", methods=["POST"])
def toy_list():
    # bind_toy : [Obj("toy_id"),"toy_id2"]

    user_id = request.form.get("user_id")
    user_info = MONGO_DB.users.find_one({"_id": ObjectId(user_id)})
    user_bind_toy = user_info.get("bind_toy")

    for index, item in enumerate(user_bind_toy):
        user_bind_toy[index] = ObjectId(item)

    toy_l = list(MONGO_DB.toys.find({'_id': {"$in": user_bind_toy}}))

    for index, toy in enumerate(toy_l):
        toy_l[index]["_id"] = str(toy.get("_id"))

    RET["code"] = 0
    RET["msg"] = "查看所有绑定玩具"
    RET["data"] = toy_l

    return jsonify(RET)


@devices.route("/device_login", methods=["POST"])
def device_login(): # {device_key:"device_key"}
    dev_info = request.form.to_dict()
    dev = MONGO_DB.devices.find_one(dev_info)
    # 校验设备DeviceKey是否有效
    if dev:
        toy = MONGO_DB.toys.find_one(dev_info)
        # 校验设备DeviceKey是否已经成为玩具
        if toy:
            return jsonify({"music": "Welcome.mp3","info":str(toy.get("_id"))})
        return jsonify({"music":"Nobind.mp3"})
    else:
        return jsonify({"music":"Nolic.mp3"})


@devices.route("/toy_info", methods=["POST"])
def toy_info():
    toy_id = request.form.get("toy_id")
    toy_info = MONGO_DB.toys.find_one({"_id":ObjectId(toy_id)})
    toy_info["_id"] = str(toy_info.get("_id"))

    RET["code"] = 0
    RET["msg"] = "查看最新玩具数据"
    RET["data"] = toy_info

    return jsonify(RET)