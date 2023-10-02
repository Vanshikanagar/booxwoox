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
        bookid = params["id"]
    except:
        return message(400,"Invalid input1")

    Q = f"UPDATE `tbl_books` SET `is_approved` = '1' WHERE (`id` = '{bookid}');"
    
    conn = connectServiceDb()
    cur = conn.cursor()
    
    try:
        cur.execute(Q)
        conn.commit()
    except Exception as e :
        conn.close()
        return message(400,e)
    
    conn.close()
    msg = f"Book id {bookid} approved."
    
    return message(200,msg)

