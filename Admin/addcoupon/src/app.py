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
        coupon = params["coupon"]
        amount = params["amount"]
        unit = params["unit"]
    except:
        return message(400,"Invalid input1")

    try:
        quantity = params["quantity"]
        quantity = int(quantity)
    except:
        quantity = 1

    if (unit == "rupee"):
        unit = "rs"
    elif( unit == "percent"):
        unit = "%";
    else:
        return message(400,"Invalid unit parametre")

    try:
        amount = int(amount)
    except:
        message(400,"Invalid amount")
    
    if len(coupon) > 16:
        return message(400,"coupon length is too long")


    Q = f"INSERT INTO `tbl_coupon` (`value`, `created_by`, `amount`, `quantity`, `unit`) VALUES ('{coupon}', '{id}', '{amount}', '{quantity}', '{unit}');"
    try:
        valid = params["validity"]
        Q = f"INSERT INTO `tbl_coupon` (`value`, `created_by`, `amount`, `quantity`, `unit`,`valid_upto`) VALUES ('{coupon}', '{id}', '{amount}', '{quantity}', '{unit}','{valid}');"
    except:
        pass


    conn = connectServiceDb()
    cur = conn.cursor()
    
    try:
        cur.execute(Q)
        conn.commit()
    except Exception as e :
        conn.close()
        return message(400,e)
    
    conn.close()
    msg = f"Coupon added successfully"
    
    return message(200,msg)

