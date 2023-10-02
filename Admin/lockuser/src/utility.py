# Function that validates the authtoken and returns roles
# Return values: meanig
# -1 : Invalid Token
# 0 : 
# 1 : 
# 2 : 

from pymysql import connect
from db import connectUserDb
import json

USERTYPE = "role"
USERID = "userId"


import re
def validateEmail(email):
    regex_email = "^[\\w!#$%&'*+/=?`{|}~^-]+(?:\\.[\\w!#$%&'*+/=?`{|}~^-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,6}$"
    return re.fullmatch(regex_email, email)


def validatePhone(phone):
    regex_phone = "(0|91)?[6-9][0-9]{9}"
    return re.fullmatch(regex_phone, phone)


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

def message(N, msg):
    return {
        "statusCode": N,
        "body": json.dumps({"message": f"{msg}"}),
    }