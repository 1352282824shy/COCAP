from flask import Blueprint,jsonify,request
from settings import MONGO_DB,RET
from bson import ObjectId

users = Blueprint("users",__name__)

@users.route("/reg",methods=["POST"])
def reg():
    user_info = request.form.to_dict()
    user_info["avatar"] = "mama.jpg" if user_info.get("gender") == "1" else "baba.jpg"

    user_info["friend_list"] = []
    user_info["bind_toy"] = []

    res = MONGO_DB.users.insert_one(user_info)

    RET["code"] = 0
    RET["msg"] = "用户注册成功"
    RET["data"] = {"user_id":str(res.inserted_id)}

    return jsonify(RET)


@users.route("/login",methods=["POST"])
def login():
    user_info = request.form.to_dict()
    print(user_info)

    #{username:",password:"}
    user = MONGO_DB.users.find_one(user_info,{"password":0})
    print(user)
    user["_id"] = str(user.get("_id"))

    RET["code"] = 0
    RET["msg"] = "用户登录"
    RET["data"] = user

    return jsonify(RET)


@users.route("/auto_login",methods=["POST"])
def auto_login():
    user_id = request.form.to_dict()
    user_id["_id"] = ObjectId(user_id.get("_id"))

    user = MONGO_DB.users.find_one(user_id,{"password":0})
    user["_id"] = str(user_id.get("_id"))


    RET["code"] = 0
    RET["msg"] = "用户自动登录"
    RET["data"] = user

    return jsonify(RET)
