from flask import Flask,request,jsonify
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from geventwebsocket.websocket import WebSocket
import json
from settings import MONGO_DB
from bson import ObjectId
from ai.baidu import text2audio,_get_xxtx
from redismsg import set_redis

ws_app = Flask(__name__)

user_socket_dict={}

@ws_app.route("/app/<app_id>")
def app(app_id):
    user_socket = request.environ.get("wsgi.websocket") # type: WebSocket
    if user_socket:
        user_socket_dict[app_id] = user_socket
    print(user_socket_dict)
    while 1:
        try:
            user_msg = user_socket.receive()
            print(user_msg) #{to_user:"toy_id",chat:"asdf.mp3",from_user:""}
            msg_dict = json.loads(user_msg)
            toy_socket = user_socket_dict.get(msg_dict.get("to_user"))
            msg_dict["chat"] = _get_xxtx(msg_dict.get("to_user"),msg_dict.get("from_user"))
            toy_socket.send(json.dumps(msg_dict))
            msg_dict["friend_type"] = "app"
            set_redis(msg_dict.get("to_user"),msg_dict.get("from_user"))
        except :
            from settings import RET
            RET["code"] = 0
            RET["msg"] = "websocket已断开连接"
            RET["data"] = {}
            return jsonify(RET)


@ws_app.route("/toy/<toy_id>")
def toy(toy_id):
    user_socket = request.environ.get("wsgi.websocket")  # type: WebSocket
    if user_socket:
        user_socket_dict[toy_id] = user_socket
    print(user_socket_dict)
    while 1:
        try:
            user_msg = user_socket.receive()
            print(user_msg) #{to_user:"toy_id",music:"asdf.mp3"}
            msg_dict = json.loads(user_msg)
            toy_socket = user_socket_dict.get(msg_dict.get("to_user"))

            if msg_dict.get("friend_type") == "toy":
                msg_dict["chat"] = _get_xxtx(msg_dict.get("to_user"), msg_dict.get("from_user"))

            msg_dict["friend_type"] = "toy"
            toy_socket.send(json.dumps(msg_dict))
            set_redis(msg_dict.get("to_user"), msg_dict.get("from_user"))
        except:
            return "websocket已断开连接"




if __name__ == '__main__':

    http_serv = WSGIServer(("0.0.0.0",3721),ws_app,handler_class=WebSocketHandler)
    http_serv.serve_forever()
