import json
from db import connectOrderDb, connectUserDb
from utility import validateToken, USERID, USERTYPE

def adminUser(userID):
    conn = connectOrderDb()
    cur = conn.cursor()

    query = "SELECT id, borrower_id, lender_id, borrower_location, lender_location, book_id, status, payment, duration, payment_status, payment_id, order_id, cp_id, order_type, date FROM tbl_order WHERE lender_id=%s OR borrower_id=%s " % (userID, userID)

    try:
        cur.execute(query)
        tmp = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        return 400

    if not tmp:
        return 400

    for rows in tmp:
        rows["date"] =  rows["date"].strftime("%m/%d/%Y, %H:%M:%S")

    return tmp

def normalUser(id):
    conn = connectOrderDb()
    cur = conn.cursor()

    query = "SELECT id, borrower_id, lender_id, borrower_location, lender_location, book_id, status, payment, duration, payment_status, payment_id, order_id, cp_id, order_type, date FROM tbl_order WHERE lender_id=%s OR borrower_id=%s " % (id, id)

    try:
        cur.execute(query)
        tmp = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        return 400

    if not tmp:
        return 400

    for rows in tmp:
        rows["date"] =  rows["date"].strftime("%m/%d/%Y, %H:%M:%S")

    return tmp

def cpUser(id):
    conn = connectOrderDb()
    cur = conn.cursor()

    query = "SELECT id, borrower_id, lender_id, borrower_location, lender_location, book_id, status, cp_id, order_type FROM tbl_order WHERE cp_id=%s " % id

    try:
        cur.execute(query)
        tmp = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        return 400

    if not tmp:
        return 400

    return tmp

def lambda_handler(event, context):

    try:
        authToken = event['headers']['authToken']
    except:
        try:
            authToken = event['headers']['authtoken']
        except:
            return{
                "statusCode": 400,
                "body": json.dumps({"message": "Token not found"}),
            }

    info = validateToken(authToken)
    role = info[USERTYPE]
    id = info[USERID]

    if role == 0:
        params = json.loads(event['body'])
        userID = params['user_id']

        res = adminUser(userID)
    elif role == 2:
        res = normalUser(id)
    elif role == 1:
        res = cpUser(id)
    else:
        return{
                "statusCode": 400,
                "body": json.dumps({"message": "Invalid User"}),
            }

    if res == 400:
        return{
            "statusCode": 400,
            "body":json.dumps({"Internal Server Error"})
        }
    else:
        return {
        "statusCode": 200,
        "body": json.dumps(res),
    }