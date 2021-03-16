# encoding=utf-8
from build_sys_environment import join_in_python_search_path, define_tornado_options, set_python_charset

def start_tornado():
    # build system environment
    set_python_charset()
    join_in_python_search_path()
    define_tornado_options()

    # import tornado server
    from tornado.options import options
    from server import Application
    from tornado import httpserver
    from tornado.ioloop import IOLoop

    app = Application()
    server = httpserver.HTTPServer(app)
    server.listen(options.port)
    IOLoop.instance().start()
    print("server in position...")

if __name__ == '__main__':
    start_tornado()
