import json
# from Order.place_order.src.db import connectServiceDb
# import datetime
from db import connectUserDb, connectServiceDb
from utility import message, USERID,USERTYPE, validateToken
# import razorpay
# from secret import rajorpay_key_ID,rajorpay_secret



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
    
    if( role != 0):
        return message(400,"Not autherized")
    #print(event)
    #params = json.loads(event['body'])
    # event body is none for now
    #approve_status = params['is_approved']
    approve_status = 0 # to be commented out

    query = "SELECT id, author, book_title, img_url FROM tbl_books WHERE is_approved= '%s'" % approve_status
    conn = connectServiceDb()
    cur = conn.cursor()

    try:
        cur.execute(query)
        res = cur.fetchall()
    except Exception as e:
        print(e)
        return{
            "statusCode": 400,
            "body":json.dumps({"Error no books found!"})
        }
    
    conn.close()

    print(res)

    return {
        "statusCode": 200,
        "body":json.dumps(res)
    }

