import json
from db import connectUserDb, connectServiceDb
from utility import message, USERID,USERTYPE, validateToken




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

    if (role == -1):
        return message(400,"Invalid Token")

    Q = f"SELECT `phone`,`email`,`first_name`,`last_name`,`credit`,`is_locked`,`longitude`,`latitude`,`profile_pic` FROM tbl_users WHERE `user_id` = '{id}'"
    conn = connectUserDb()
    cur = conn.cursor()

    try:
        cur.execute(Q)
        res = cur.fetchone()
    except Exception as e :
        conn.close()
        return message(400,e)
    conn.close()

    if res["is_locked"]:
        return message(400,"Your account is locked.")

    del res["is_locked"]

    return {
        "statusCode": 200,
        "body":json.dumps(res)
    }

