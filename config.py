# coding=utf-8
from tornado.options import define
import os
# 服务地址配置
define("host_ip", default="127.0.0.1:8090", help="the ip of server eg. 192.168.1.150:80")
define("port", default=8090, help="run on the given port", type=int)
def print_success():
    print("tornado options has been defined.")

