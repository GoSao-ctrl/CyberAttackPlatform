from abc import ABCMeta
import tornado.web
from backend.operation import ControlNode
import json


class Handler:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def can_handle(self, method_type):
        return method_type and method_type in ["GetCommand"]

    def handle(self, req_handler, page_id, arg):
        self.do_handle(req_handler, page_id, arg)
        req_handler.flush()
        req_handler.finish()

    def do_handle(self, req_handler, page_id, arg):
        _id = "".join([req_handler.request.remote_ip, page_id])
        print(page_id)
        if page_id == "GetCommand":
            type = arg["type"]
            ip = arg["ip"]
            port = arg["port"]
            if port != "":
                obj = ControlNode.ControlNodeHandle(type, ip, port)
            else:
                obj = ControlNode.ControlNodeHandle(type, ip)
        req_handler.write(obj)


class ExceptionHandler(Handler):
    def can_handle(self, method_type):
        return True

    def do_handle(self, req_handler, page_id, arg):
        req_handler.write("501, Not Implemented!")


class HandlerManager(tornado.web.RequestHandler):
    handlers = [Handler(), ExceptionHandler()]

    def data_received(self, chunk):
        pass

    def initialize(self):
        # self.operation = operation
        pass

    def get(self, page_id):
        self.render("index.html")

    def post(self, page_id):
        post_data = self.get_argument("arg")
        # post_data =self.get_argument()
        arg = json.loads(post_data)
        for handler in HandlerManager.handlers:
            if handler.can_handle(page_id):
                # if not handler.accessor:
                #     handler.accessor = self.operation
                try:
                    handler.handle(self, page_id, arg)
                except Exception as err:
                    print(err)
                return
