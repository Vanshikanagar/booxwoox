# Role of cp : 1

from pymysql import connect
from db import connectUserDb
import json

USERTYPE = "role"
USERID = "userId"

def validateToken(authToken):
    conn = connectUserDb()
    cur = conn.cursor()

    query = "SELECT userid, role FROM tbl_users_sessions WHERE token ='%s'" % authToken
    cur.execute(query)
    res = cur.fetchone()
    flag = 1
    response = {USERTYPE: -1, USERID: None}
    if not res:
        response[USERTYPE] = -1
        response[USERID] = None
    elif res["role"] == 0:
        response[USERTYPE] = 0
        response[USERID] = res['userid']
    elif res["role"] == 1:
        response[USERTYPE] = 1
        response[USERID] = res['userid']
    elif res["role"] == 2:
        response[USERTYPE] = 2
        response[USERID] = res['userid']
    else:
        flag = 0

    if flag:
        cur.close()
        conn.close()
        return response