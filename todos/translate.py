import os
import json

from todos import decimalencoder
import boto3

dynamodb = boto3.resource('dynamodb')
translateService = boto3.client(service_name='translate')

def get (event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    if event['pathParameters']['languague'] == 'en':
        target = 'en'
    elif event['pathParameters']['languague'] == 'fr':
        target = 'fr'
    else:
        target = 'auto'
    
    resultFinal = translateService.translate_text(Text = result['Item']['text'], SourceLanguageCode='auto', TargetLanguageCode=target)
                                                                          

    result['Item']["text"] = resultFinal.get('TranslatedText')

    #create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

<<<<<<< HEAD
    return response
    
=======
    return response
>>>>>>> main
