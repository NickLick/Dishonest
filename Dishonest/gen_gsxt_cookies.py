#实现生成cookie
from Dishonest.settings import MYSQL_HOST,MYSQL_PORT,MYSQL_PASSWORD,MYSQL_DB,MYSQL_USER
import random

class GenGsxtCookie(object):
    def __init__(self):
        #建立数据库连接
        pass

    def push_cookie_to_db(self):
        # 实现一个方法，把一套的代理ip，user-agent，cookie绑定在一起的信息放到db中

