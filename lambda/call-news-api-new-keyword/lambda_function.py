import boto3
import logging
import os
from datetime import datetime
import urllib3

logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-10s %(message)s")
LOG = logging.getLogger("handler.py")
LOG.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))

api_key = os.environ['api_key']
time_now = datetime.now()



def lambda_handler(event, context):

    event_name = event['Records'][0]['eventName']

    if 'NewImage' not in event['Records'][0]['dynamodb']:
        response = "No change in the tracked records."
        LOG.info(response)
        return response
    
    if event_name not in ['INSERT', 'MODIFY']:
        LOG.info(event)

        # {'Records': [{'eventID': '3b1a17999024e18d4ba3e0d760801d03', 'eventName': 'INSERT', 'eventVersion': '1.1', 'eventSource': 'aws:dynamodb', 'awsRegion': 'eu-west-1', 'dynamodb': {'ApproximateCreationDateTime': 1648935792.0, 'Keys': {'keyphrase': {'S': 'example new record'}}, 'NewImage': {'keyphrase': {'S': 'example new record'}}, 'SequenceNumber': '335700000000023132824619', 'SizeBytes': 54, 'StreamViewType': 'NEW_AND_OLD_IMAGES'}, 'eventSourceARN': 'arn:aws:dynamodb:eu-west-1:644211746806:table/keyword-result/stream/2022-04-02T21:10:33.897'}]}

        response = "Not a modification in records"
        LOG.info(response)
        return response

    elif event_name == 'MODIFY': 
        key_before = event['Records'][0]['dynamodb']['OldImage']
        LOG.info(key_before)
        old_date_str = key_before['date']['S']
        old_datetime = datetime.strptime(old_date_str, "%Y-%m-%d")
        if (time_now - old_datetime).days < 3:
            response = "Keyword Analysis updated recently"
            LOG.info(response)
            return response

    else:
        key_after = event['Records'][0]['dynamodb']['NewImage']
        keyphrase = key_after['keyphrase']['S']
        
        http = urllib3.PoolManager()
        r = http.request('GET', f'https://newsapi.org/v2/everything?q={keyphrase}&from=2022-04-02&sortBy=popularity&apiKey={api_key}')
        
        print(r.data)
        return "response returned"
   