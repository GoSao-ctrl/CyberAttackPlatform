import os
import sys
import importlib


def set_python_charset():
    importlib.reload(sys)
    # sys.setdefaultencoding("utf-8")
    print("python coding has been set with", sys.getdefaultencoding())


def join_in_python_search_path():
    project_path = os.path.dirname(__file__)
    sys.path.append(project_path)
    print("nsds-stage2 basedir '" + project_path + "'", "has join in python search path.")


def define_tornado_options():
    import config
    config.print_success()
