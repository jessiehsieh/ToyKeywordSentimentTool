from pandas import DataFrame
import boto3
client = boto3.client('comprehend')

def get_analysis(all_text: str):

    result = client.detect_key_phrases(Text= document[i:i+limit], LanguageCode='en')['KeyPhrases']

    df_keywords = pd.DataFrame(result)[['Score','Text']].rename(columns = {
            'Score':'confidence',
            'Text' : 'keyword'
        }).sort_values('Score', ascending=False).head(20)

    sentiment= client.detect_sentiment(Text=event['inputTranscript'],LanguageCode='en')['Sentiment']
    positive_score= client.detect_sentiment(Text=event['inputTranscript'],LanguageCode='en')['SentimentScore']['Positive']
    negative_score= client.detect_sentiment(Text=event['inputTranscript'],LanguageCode='en')['SentimentScore']['Negative']
    neutral_score= client.detect_sentiment(Text=event['inputTranscript'],LanguageCode='en')['SentimentScore']['Neutral']

    df_keywords.loc[:,'Sentiment Info'] = None
    df_keywords.loc[0,'Sentiment Info'] = f"Overall: {sentiment}"
    df_keywords.loc[1,'Sentiment Info'] = f"Score, positive: {positive_score}"
    df_keywords.loc[2,'Sentiment Info'] = f"Score, negative: {negative_score}"
    df_keywords.loc[3,'Sentiment Info'] = f"Score, neutral: {neutral_score}"

    return df_keywords.to_html()
