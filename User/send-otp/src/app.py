import json
import datetime
import uuid
from db import connectUserDb
from random import randint
from utility import validatePhone,message
import boto3

# sns = boto3.client('sns')

# def send_otp(otp,phone):
#     res = sns.publish(PhoneNumber = '+91'+phone, Message=f"{otp}")

def lambda_handler(event,context):
    print(event)
    params = json.loads(event['body'])
    
    
    try:
        phoneno = params['phoneno']
    except:
        return message(400,"Missing inputs")
    

    search_query = None
    
    if validatePhone(phoneno):
        search_query = "SELECT user_id from tbl_users WHERE phone= '%s'" % phoneno
    else:
        return message(400,f"Invalid Input {phoneno}")

    conn = connectUserDb()
    cur = conn.cursor()
    id = None
    try:
        cur.execute(search_query)
        res = cur.fetchone()
        id = res["user_id"]
    except :
        pass
    
    otp =randint(100000,999999)
    hash_id = str(uuid.uuid4())
    expiry = datetime.datetime.now() + datetime.timedelta(minutes = 2)

    update_Q = f"UPDATE `tbl_users` SET `otp` = '{otp}', `temp_token` = '{hash_id}', `otp_expiry`='{expiry}' WHERE (`user_id` = '{id}')"
    insert_Q = f"INSERT INTO `tbl_users` (`phone`, `otp`, `is_active`, `otp_expiry`, `role`, `temp_token`) VALUES ('{phoneno}', '{otp}', '0', '{expiry}', '2', '{hash_id}')"

    if (id != None):
        try:
            # send_otp(otp,phoneno)
            cur.execute(update_Q)
            conn.commit()
        except Exception as e:
            conn.close()
            return message(400,e)
    else:
        try:
            # send_otp(otp,phoneno)
            cur.execute(insert_Q)
            conn.commit()
        except Exception as e :
            conn.close()
            return message(400,e)
    conn.close()

    return{
            "statusCode": 200,
            "body": json.dumps({
                    "success": True,
                    "token": hash_id,
                    "otp":otp
                }),
        }
  
  

  
  
  
  