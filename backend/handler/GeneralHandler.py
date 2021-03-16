import tornado.web
from tornado.options import options
import socket


class MainHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.render("index.html")


class SubPageHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, which):
        print(which)
        self.render(which, host_ip=options.host_ip or socket.gethostbyname(socket.gethostname()))
