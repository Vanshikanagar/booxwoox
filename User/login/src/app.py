import json
import bcrypt
import datetime
import uuid
from db import connectUserDb
from utility import validateEmail,validatePhone,message

def lambda_handler(event,context):
    print(event)
    params = json.loads(event['body'])
    username = params['username']
    password = params['password']

    if username == None or password == None:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Bad request due to missing or invalid value of parameter."})
        }

    search_query = None
    if(validateEmail(username)):
        search_query = "SELECT user_id, email,password, phone,role, first_name from tbl_users WHERE email= '%s'" % username
    elif validatePhone(username):
        search_query = "SELECT user_id, email,password, phone,role, first_name from tbl_users WHERE phone= '%s'" % username
    else:
        return message(400,f"Invalid Input {username}")

    conn = connectUserDb()
    cur = conn.cursor()
    try:
        cur.execute(search_query)
        res = cur.fetchone()
    except Exception as e:
        print(e)
        conn.close()
        return{
            "statusCode":400,
            "body":json.dumps({"message":"SQL error Or email not registered"}),
        }
    
    
    if not res:
        conn.close()
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "user not registered!"}),
        }

    # if res['is_locked'].hex() == '01':
    #     conn.close()
    #     return {
    #         "statusCode": 400,
    #         "body": json.dumps({"message": "User Account is Locked"}),
    #     }

    role = res['role']
    

    if bcrypt.checkpw(password.encode('utf-8'),res['password'].encode('utf-8')):
        # set session in tbl_session
        print("correct password")
        session_query = "SELECT id FROM tbl_users_sessions WHERE userid = '%s'"% res['user_id']
        cur.execute(session_query)
        present = cur.fetchone()
        

    
        hash_id = str(uuid.uuid4())

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
            insert_q = "INSERT INTO tbl_users_sessions (token,userid,role) VALUES ('%s','%s',%s)" % (hash_id,res['user_id'],role)
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
    else:
        conn.close()
        return{
            "statusCode": 400,
            "body": json.dumps({
                    "success": False,
                    "message": "Wrong Password",
                }),
        }
  
  

  
  
  
  