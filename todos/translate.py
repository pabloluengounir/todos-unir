import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    comprehend = boto3.client(service_name='comprehend')
    translate = boto3.client(service_name='translate')

    # fetch todo from the database
    item = json.dumps(table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )['Item'], indent=4)
    text = json.loads(item)['text']
    languages = json.dumps(comprehend.detect_dominant_language(Text=text))
    languages = json.loads(languages)["Languages"]
    fromLanguage = languages[0]
    fromLanguage = fromLanguage['LanguageCode']
    result = translate.translate_text(Text=text, 
            SourceLanguageCode=fromLanguage, TargetLanguageCode=event['pathParameters']['language'])
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result.get('TranslatedText'),
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
