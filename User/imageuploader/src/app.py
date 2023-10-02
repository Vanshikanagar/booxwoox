import json
import boto3
import base64
import email
from utility import validateToken, USERID, USERTYPE


def lambda_handler(event, context):
    # Validate User First
    try:
        authToken = event['headers']['authToken']
        folder = event['headers']['folderName']
    except:
        try:
            authToken = event['headers']['authtoken']
            folder = event['headers']['foldername']
        except:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Token Not Found"}),
            }
    # Step 2: Verify Tokens
    info = validateToken(authToken)
    role = info[USERTYPE]
    
    if role == -1:
        return{
            "statusCode": 400,
            "body": json.dumps({"message": "Token Not Found", "role": role}),
        }


    s3 = boto3.client("s3")
    print(event)
    # decoding form-data into bytes
    post_data = base64.b64decode(event['body'])
    # fetching content-type
    try:
        content_type = event["headers"]['Content-Type']
    except:
        content_type = event["headers"]['content-type']
    # concate Content-Type: with content_type from event
    ct = "Content-Type: "+content_type+"\n"

    # parsing message from bytes
    msg = email.message_from_bytes(ct.encode()+post_data)

    # checking if the message is multipart
    print("Multipart check : ", msg.is_multipart())

    # if message is multipart
    if msg.is_multipart():
        multipart_content = {}
        # retrieving form-data
        for part in msg.get_payload():
            # checking if filename exist as a part of content-disposition header
            if part.get_filename():
                # fetching the filename
                file_name = part.get_filename()
            multipart_content[part.get_param(
                'name', header='content-disposition')] = part.get_payload(decode=True)

        # filename from form-data
        file_name = folder+"/" + \
            json.loads(multipart_content["Metadata"])["filename"]
        mimetype = json.loads(multipart_content["Metadata"])["mimetype"]
        print(mimetype)
        print(multipart_content)
        # u uploading file to S3
        s3_upload = s3.put_object(
            Bucket="book-images-uploaded", Key=file_name, Body=multipart_content["file"], ContentType=mimetype)

        # on upload success
        return {
            'statusCode': 200,
            'body': json.dumps({
                "message": "File Uploaded Successfully!",
                "url": "https://book-images-uploaded.s3.ap-south-1.amazonaws.com/"+file_name,
            })
        }
    else:
        # on upload failure
        return {
            'statusCode': 500,
            'body': json.dumps('Upload failed!')
        }

  

  
  
  
  