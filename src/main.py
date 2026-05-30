import boto3
import os 
import json

TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')
IDENTIFIER = os.getenv('LEARNER_IDENTIFIER')
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'}

def lambda_handler(event, context):

    print("Event: ", json.dumps(event))
    

    for r in event.get("Records"):
        if "object" in r.get("s3"):
            filename = r.get("s3").get("object").get("key")
           
            print("uploaded filename: ", filename)

            ext = os.path.splitext(filename)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                print("file type not allowed: ", ext)
                return {
                    'statusCode': 400,
                    'body': json.dumps(f'file type not allowed: {ext}')
                }

            table = boto3.resource('dynamodb').Table(TABLE_NAME)
            item = {'pk': IDENTIFIER, 'filenames': filename}
            response = table.get_item(Key={'pk': IDENTIFIER, 'filenames': filename})
            if 'Item' in response:
                print("filename already exist in the database")
                return {
                'statusCode': 400,
                'body': json.dumps('filename already exist in the database')
                }
            else:
                table.put_item(Item=item)
                print("filename added to the database")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda loaded from src/main.py!')
        }