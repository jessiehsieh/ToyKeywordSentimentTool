import boto3
import logging
import os
from datetime import datetime
from botocore.vendored import requests

logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-10s %(message)s")
LOG = logging.getLogger("handler.py")
LOG.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))

api_key = os.environ['api_key']
now_str = str(datetime.today()).replace(' ', ',')

def lambda_handler(event, context):
    
    if event['Records'][0]['eventName']!='MODIFY':
        response = "Not a modification in records"
        LOG.info(response)
        return response
    
    LOG.info(event)
    #key_before = event['Records'][0]['dynamodb']['OldImage']
    
    if 'NewImage' not in event['Records'][0]['dynamodb']:
        response = "No change in the tracked records."
        LOG.info(response)
        return response
        
    key_after = event['Records'][0]['dynamodb']['NewImage']
    LOG.info(key_after)
    
    latest_keyphrase = key_after['keyphrase']['S']
    LOG.info(latest_keyphrase)
    
    
    if key_after['s3_path']['S']=='':
        
        LOG.info("""Getting news for keyword - %s"" % (latest_keyphrase)""")


        url = (f'https://newsapi.org/v2/everything?q={latest_keyphrase}&from=2022-04-02&sortBy=popularity&apiKey={api_key}')

        response = requests.get(url)

        print(response.json)
        
        return "response returned"
    
    else:
        
        return "s3 path exists already"