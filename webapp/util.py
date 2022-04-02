import boto3

def get_keyword_record_from_dynamodb(self, keyphrase):
    """

    Parameters
    ----------
    user_id : TYPE
    DESCRIPTION.

    Returns
    -------
    item : TYPE
    DESCRIPTION.

    """
    # Creating the DynamoDB Table Resource
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table("keyword-result")

    response = table.get_item(
            Key={
                    'keyphrase': keyphrase
                }
            )
    item = response.get('Item')

    return item
