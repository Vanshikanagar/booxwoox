import json
from db import connectUserDb, connectServiceDb
from utility import message, USERID,USERTYPE, validateToken,validateEmail




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

    conn = connectUserDb()
    cur = conn.cursor()
    params = json.loads(event['body'])

    Q1  = f"SELECT `email`,`first_name`,`last_name`,`longitude`,`latitude`,`profile_pic` FROM tbl_users WHERE user_id = '{id}'"
    try:
        cur.execute(Q1)
        res = cur.fetchone()
    except Exception as e:
        conn.close()
        return message(400,e)
    

    try:
        email = params["email"]
        if (validateEmail(email)):
            pass
        else:
            conn.close()
            return message(400,"invalid mail")
    except:
        email = res["email"]
    
    try:
        firstname = params["firstname"]
        if (firstname.isalpha() == False):
            conn.close()
            return message(400,"Non alphabet firstname not allowed")
    except:
        firstname = res["first_name"]

    try:
        lastname = params["lastname"]
        if (lastname.isalpha() == False):
            conn.close()
            return message(400,"Non alphabet lastname not allowed")
    except:
        lastname = res["last_name"]

    try:
        latitude = params["latitude"]
    except:
        latitude = res["latitude"]

    try:
        longitude = params["longitude"]
    except:
        longitude = res["longitude"]

    try:
        img = params["profile_pic"]
    except:
        img = res["profile_pic"]

    #  20.5937° N  || 78.9629° E    
    # Epattern = r'(^[\d{0-2}]+).([\d{3-5}]+)° E'
    # Npattern = r'(^[\d{0-2}]+).([\d{3-5}]+)° N'

    Q = f"UPDATE `tbl_users` SET `latitude` = '{latitude}',`profile_pic`={img}, `longitude` = '{longitude}',`last_name`= '{lastname}',`first_name` = '{firstname}',`email` = '{email}'  WHERE (`user_id` = '{id}');"
    try:
        cur.execute(Q)
        conn.commit()
    except Exception as e :
        conn.close()
        return message(400,e)

    return {
        "statusCode": 200,
        "body":json.dumps("Profile Updated")
    }

