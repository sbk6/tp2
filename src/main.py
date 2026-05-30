import json

def lambda_handler(event, context):
    # Log the incoming event
    print("Received event:", json.dumps(event))

    # Process the event (for example, extract a message)
    message = event.get('message', 'No message provided')

    # Create a response
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Hello, you sent from lambda: {message}'
        })
    }

    # Log the response
    print("Response:", json.dumps(response))

    return response