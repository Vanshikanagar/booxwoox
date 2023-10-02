import json
import datetime
from db import connectServiceDb
from random import randint
from utility import message,validateToken,USERID,USERTYPE
# import boto3

    # order types :
        # 1 : borrow (lender to borrower) via CP
        # 2 : return (borrower to lender) via CP
        # 3 : borrow (lender to sender) self delivery
        # 4 : return (borrower to sender) self delivery
        # 5 : buy book (lender to borrower) via CP

    # Order status
        # 0 : order cenceled
        # 1 : order placed ( now time to pay) > sell -> payment
        # 2 : book avilable for delivary -> 
        # 3 : order choosed by cp 
        # 4 : book picked
        # 5 : deliverd ( requies opt verification ) can be skipd for order type : 3,6
        # 6 : return period ends
        # 7 : payment complete 

# sns = boto3.client('sns')
# def send_otp(otp,phone):
#     res = sns.publish(PhoneNumber = '+91'+phone, Message=f"{otp}")


def lambda_handler(event,context):
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
    id = int(info[USERID])

    if (role == -1):
        return message(400,"Invalid Token")

    
    params = json.loads(event['body'])
    
    
    try:
        img = params['img']
        order_id = params['id']
    except:
        return message(400,"Missing inputs")
    
    Q1 = f"SELECT `lender_id`,`borrower_id`,`cp_id`,`order_type`,`status`,`payment_status` FROM tbl_order WHERE id ='{order_id}' "

    conn = connectServiceDb()
    cur = conn.cursor()

    try:
        cur.execute(Q1)
        res = cur.fetchone()
    except:
        conn.close()
        return message(400,"Internal Server Error 1")

    Q3 = f"UPDATE `tbl_courier` SET `img1` = '{img}' WHERE `order_id` = '{order_id}'"
    #=================================  CHECKING ================================

    print(type(res["cp_id"]))
    print(type(id))
    print((res["cp_id"]) == id)

    if (res["cp_id"]) == id :
        if res["status"] == 3:
            if res["order_type"] == 1:
                sendto = res["lender_id"]
                status = 4
            elif res["order_type"] == 5:
                if res["payment_status"] != 1:
                    conn.close()
                    return message(400,"Payment Incomplete") 
                sendto = res["lender_id"]
                status = 4
            elif res["order_type"] == 2:
                if res["payment_status"] != 1:
                    conn.close()
                    return message(400,"Payment Incomplete")
                sendto = res["borrower_id"] 
                status = 4   
            else:
                conn.close()
                return message(400,"Not applicable 1")        
        elif res["status"] == 4:
            Q3 = f"UPDATE `tbl_courier` SET `img2` = '{img}' WHERE `order_id` = '{order_id}'"
            if res["order_type"] == 1:
                sendto = res["borrower_id"]
                status = 5
            elif res["order_type"] == 5: 
                sendto = res["borrower_id"]
                status = 5
            elif res["order_type"] == 2:
                sendto = res["lender_id"]  
                status = 5  
            else:
                conn.close()
                return message(400,"Not applicable 2")

    elif res["lender_id"] == id:
        if res["status"] == 6:
            if res["order_type"] == 4:
                sendto = res["borrower_id"]
                status = 5
        else:
            return message("Not applicable 3")

    elif res["borrower_id"] == id:
        if res["status"] == 2:
            if res["order_type"] == 3:
                sendto = res["lender_id"]
                status = 5
        else:
            return message("Not applicable 4")
    else:
        conn.close()
        return message(400,"Not applicable 5")

    # ======================== checking and setting varriable complete ====================

    otp =randint(100000,999999)
    expiry = datetime.datetime.now() + datetime.timedelta(minutes = 2)
    Q2 = f"UPDATE `tbl_order` SET `otp` = '{otp}', `expiry` = '{expiry}' WHERE (`id` = '{order_id}');"
    

    try:
        # send_otp(otp,sendto)
        cur.execute(Q2)
        conn.commit()
        cur.execute(Q3)
        conn.commit()
    except Exception as e:
        conn.close()
        return message(400,e)

    conn.close()
    return{
            "statusCode": 200,
            "body": json.dumps({
                    "success": True,
                    "otp": otp,
                    "msg":"otp sent"
                    })
        }