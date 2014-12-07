#-*-coding: utf-8 -*-

import os

from tornado.options import options, define

define('debug', default=True, help='server in debug mode or not.', type=bool)
define('server_port', default=8000, help='server run on the given port.', type=int)
define('mongodb_host', default='127.0.0.1', help='mongodb server ip.', type=str)
define('mongodb_port', default=27017, help='mongodb server port.', type=int)
define('mongodb_user', default=None, help='mongodb server username.', type=str)
define('mongodb_password', default=None, help='mongodb server user password.', type=str)
define('redis_host', default='127.0.0.1', help='redis server ip.', type=str)
define('redis_port', default=6379, help='redis server port.', type=int)
define('mysql_host', default='127.0.0.1', help='mysql server ip.', type=str)
define('mysql_port', default=3306, help='mysql server port.', type=int)
define('mysql_user', default='admin', help='mysql server username.', type=str)
define('mysql_password', default='admin', help='mysql server user password.', type=str)
define('xsrf_cookies', default=True, help='', type=bool)
define('cookie_secret', default='FWSD343DKJBU8734NG5JH098FGFTEST', help='', type=str)
define('template_path', default=os.path.join(os.path.dirname(__file__), 'templates'), type=str)
define('static_path', default=os.path.join(os.path.dirname(__file__), 'static'), type=str)

_app_settings = {}
_initialized = False

def init_app_settings():
    """ 命令行参数优先, 会覆盖配置文件中的参数。
    """
    global _app_settings
    if _initialized:
        return _app_settings
    # 只为了获取 options.config, 后边会再次调用.

    options.run_parse_callbacks()
    _app_settings = options.as_dict()
#    for i in _app_settings:
#        print i, _app_settings[i]
    return _app_settings
