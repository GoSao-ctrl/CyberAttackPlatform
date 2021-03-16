# coding=utf-8
import os
import tornado.web
from backend.handler import GeneralHandler, InstructionAnalysis


class Application(tornado.web.Application):
    """
    tornado 框架程序启动初始化类
    """

    def __init__(self):
        """
         初始化加载
        """
        # 通用模块数据操作类
        # self.flow_op = FlowOperation()
        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            'template_path': os.path.join(os.path.dirname(__file__), "Html"),
            'debug': True,
        }
        urls = [
            (r'/', GeneralHandler.MainHandler),
            (r'/index/(.*)', GeneralHandler.SubPageHandler),
            (r'/Command/(.*)', InstructionAnalysis.HandlerManager)
            # zj add url
            # (r'/login/(.*)', LoginHandler.HandlerManager, dict(operation=self.user_op)),

        ]
        print("tornado init...")
        tornado.web.Application.__init__(self, urls, **settings)
