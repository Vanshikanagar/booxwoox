import json
from db import connectSessionsDb,connectBooksDb


def lambda_handler(event, context):
    #print(event)
    
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
    
    conn = connectSessionsDb()
    cur = conn.cursor()

    auth_query = "SELECT role FROM tbl_users_sessions WHERE token= '%s'" % authToken
    cur.execute(auth_query)
    det = cur.fetchone()
    print(det)
    if not det:
        cur.close()
        conn.close()
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid Token"}),
        }
    if det["role"] == -1:
        cur.close()
        conn.close()
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid User"}),
        }

    params = json.loads(event['body'])
    book_id = params['id']
    print(book_id)

    book_query = "SELECT * FROM tbl_books WHERE id= '%s'" % book_id
    conn = connectBooksDb()
    cur = conn.cursor()
    
    try:
        cur.execute(book_query)
        res = cur.fetchone()
        res["created_date"] =  res["created_date"].strftime("%m/%d/%Y, %H:%M:%S")
        res["genre"] = res["genre"].split(",")
        res["tags"] = res["tags"].split(",")
    except Exception as e:
        print(e)
        return{
            "statusCode": 400,
            "body":json.dumps({"Internal Server Error"})
        }

    conn.close()
    cur.close()

    return {
        "statusCode": 200,
        "body": json.dumps(res),
    }