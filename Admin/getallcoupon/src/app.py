import json

from pymysql import NULL
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

    

    Q = f"SELECT * FROM tbl_coupon;"


    conn = connectServiceDb()
    cur = conn.cursor()
    
    try:
        cur.execute(Q)
        res = cur.fetchall()
    except Exception as e :
        conn.close()
        return message(400,e)
    conn.close()

    # for i in res:
    #     if(i["valid_upto"] != None or i["valid_upto"] != NULL):

    # msg = f"Coupon added successfully"
    
    return {
        "statusCode": 200,
        "body": json.dumps(res,default=str),
    }
