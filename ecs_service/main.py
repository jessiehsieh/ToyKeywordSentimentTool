from typing import Optional

import boto3
from fastapi import FastAPI
import urllib3
from util import get_analysis

app = FastAPI()

BUCKET = "toy-keyword-sentiment-results"
api_key = os.environ['api_key']

@app.get("/")
def read_root():
    return "endpoint do not exist"


@app.get("/keyword/{keyphrase}")
def read_item(keyphrase: str):

    keyphrase_with_space = keyphrase.replace('_','')

    http = urllib3.PoolManager()
    r = http.request('GET', f'https://newsapi.org/v2/everything?q={keyphrase_with_space}&from=2022-04-02&sortBy=popularity&apiKey={api_key}')
    article_list = json.loads(r.data)['articles']
    text_document = []
    for article in article_list[0:10]:
        text_document.append(article['content'])
        text_document.append(article['description'])
        
    all_news = ' '.join(text_document)
    html = get_analysis(all_news)

    s3 = boto3.client('s3')
    s3.put_object(Bucket=BUCKET, Key=f'{keyphrase}.html', Body=html)

    return 200