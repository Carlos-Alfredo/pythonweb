import json
from datetime import datetime

def lambda_handler(event, context):
    # Getting the current date and time
    dt = datetime.now()
    
    # getting the timestamp
    ts = datetime.timestamp(dt)
    return {
        'statusCode': 200,
        'body': json.dumps(ts)
    }
