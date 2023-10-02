import json
from db import connectUserDb, connectServiceDb
from utility import message, USERID,USERTYPE, validateToken
import datetime

def lambda_handler(event, context):
    try:
        authToken = event['headers']['authToken']
    except:
        try:
            authToken = event['headers']['authtoken']
        except:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Token Not Found"}),
            }
    
    info = validateToken(authToken)
    role = info[USERTYPE]
    id = info[USERID]

    if role != 0:
        return message(403,"Not Superuser")

    params = json.loads(event['body'])
    try:
        userid = params["id"]
        lock = params["is_locked"]
    except:
        return message(400,"Invalid input1")

    try:
        lock = int(lock)
        if lock != 0 and lock != 1:
            return message(400,"Invalid Input2")
    except:
        return message(400,"Invalid Input3")
    
    msg = ""
    if lock == 0:
        msg = "User Unlocked"
    elif lock == 1:
        msg = "User Locked"
    else:
        return message(400,"Invalid Input4")

    now = datetime.datetime.now()
    Q1 = f"UPDATE `tbl_users` SET `is_locked` = '{lock}',`modified_by` = '{id}',`modifed_date`='{now}' WHERE (`user_id` = '{userid}');"
    Q2 = f"DELETE FROM `tbl_users_sessions` WHERE (`userid` = '{userid}');"

    conn = connectUserDb()
    cur = conn.cursor()
    try:
        cur.execute(Q1)
        conn.commit()
        try:
            cur.execute(Q2)
            conn.commit()
        except:
            pass
    except Exception as e:
        conn.close()
        return message(400,e)
    conn.close()
    return message(200,msg)

