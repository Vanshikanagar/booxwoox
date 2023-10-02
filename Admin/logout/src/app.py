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

    Q1 = f"DELETE FROM `tbl_users_sessions` WHERE (`userid` = '{id}');"
    Q2 = f"UPDATE `tbl_users` SET `is_active` = '0' WHERE (`user_id` = '{id}');"

    conn = connectUserDb()
    cur = conn.cursor()
    try:
        cur.execute(Q1)
        conn.commit()
        cur.execute(Q2)
        conn.commit()
    except Exception as e :
        conn.close()
        return message(400,e)
    
    conn.close()
    

    return {
        "statusCode": 200,
        "body":json.dumps("Logged out.")
    }

