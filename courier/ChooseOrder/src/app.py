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

    if (role != 1):
        return message(400,"Invalid Token")

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
    
    params = json.loads(event['body'])

    try:
        orderid = params["id"]
    except:
        return message(404,"Input not found")

    Q = f"SELECT `payment_status`,`status`, `order_type` FROM tbl_order WHERE id = '{orderid}'"

    conn = connectServiceDb()
    cur = conn.cursor()

    try:
        cur.execute(Q)
        res = cur.fetchone()
        payment = res["payment_status"]
        order_status = res["status"]
        order_type = res["order_type"]
    except:
        conn.close()
        return message(400,"Server error 1 ")

    #--------------------------------CHECKING------------------------------

    if order_status == 2:
        if order_type == 1:
            pass
        elif order_type == 5:
            if payment !=  1:
                conn.close()
                return message(403,"Payment not done yet.")
        else:
            conn.close()
            return message(404,"Not applicable")
    elif order_status == 6:
        if order_type == 2:
            if payment != 1:
                conn.close(400,"Payment not done.")
        else:
            conn.close()
            return message(400,"Not applicable")
    else:
        conn.close()
        return message(400,"Not applicable")

    #------------------------CHECKING COMPLETE--------------------------

    Q2 = f"UPDATE `tbl_order` SET `status` = '3', `cp_id` = '{id}' WHERE (`id` = '{orderid}');"

    try:
        cur.execute(Q2)
        conn.commit()
    except:
        conn.close()
        return message(400,"Fatal Error")
    
    conn.close()

    return {
        "statusCode": 200,
        "body":json.dumps("Order Choosed. You can go for delivery now.")
    }

