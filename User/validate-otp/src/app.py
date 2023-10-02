import json
import datetime
from db import connectUserDb
import uuid
from utility import message


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
    

    params = json.loads(event['body'])
    try:
        otp1 = params["otp"]
    except:
        return message(400,"Missing Input")
    
    Q1 = f"SELECT user_id,otp,otp_expiry,role FROM tbl_users WHERE temp_token = '{authToken}' "
    conn = connectUserDb()
    cur = conn.cursor()

    try:
        cur.execute(Q1)
        res = cur.fetchone()
        id = res["user_id"]
        otp2 = res["otp"]
        expiry = res["otp_expiry"]
        role = res["role"]

    except:
        conn.close()
        return message(400,"Token not found")
    
    now = datetime.datetime.now()

    if otp1 != otp2:
        conn.close()
        return message(400,"Wrong otp")
    
    if (now> expiry):
        conn.close()
        return message(400,"Otp expired ")

    Q2 = f"UPDATE `tbl_users` SET `otp` = '', `is_active` = '1', `otp_expiry` = '', `temp_token` = '' WHERE (`user_id` = '{id}'); "
    hash_id = str(uuid.uuid4())

    try:
        cur.execute(Q2)
        conn.commit()
    except Exception as e:
        conn.close()
        return message(400,e)

    session_query = "SELECT id FROM tbl_users_sessions WHERE userid = '%s'"% id
    cur.execute(session_query)
    present = cur.fetchone()
        

    
        

    if present:
            # update
        update = conn.cursor()
        update_q = "UPDATE tbl_users_sessions SET token = '%s' WHERE id = '%s'" %(hash_id,present['id'])
        try:
            update.execute(update_q)
            conn.commit()
            update.close()
        except Exception as e:
            print(e)
            conn.close()
            return message(400,e)
        conn.close()
        return{
            "statusCode": 200,
            "body": json.dumps({
                    "authToken": hash_id,
                    "id":res['user_id']
                    }),
            }
    else:
        # insert
        insert = conn.cursor()
        res_uesr_id = res['user_id']
        insert_q = f"INSERT INTO tbl_users_sessions (token,userid,role) VALUES ('{hash_id}','{res_uesr_id}','{role}')"
        try:
            insert.execute(insert_q)
            conn.commit()
            insert.close()
        except Exception as e:
            print(e)
            conn.close()
            return{
                    "statusCode": 400,
                    "body": json.dumps({"message": e}),
                }

        conn.close()
        return{
            "statusCode":200,
            "body": json.dumps({
                        "authToken": hash_id,
                        "id": res['user_id']
                    }),
            }

  

  
  
  
  