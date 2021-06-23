import tornado.web
from tornado.options import options
import socket
from backend.handler import DB_OP


class MainHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.render("index.html")


class SubPageHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get(self, which):
        print("reading:" + which)
        DB_OP.DBOperation().log_insert_sql_one("AttackUser1", "enter " + str(which), "success", "none")
        self.render(which, host_ip=options.host_ip or socket.gethostbyname(socket.gethostname()))
