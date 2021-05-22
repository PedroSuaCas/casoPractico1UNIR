import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')
translateService = boto3.client(service_name='translate')

def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id'],
            'languague': event['pathParameters']['languague']
        }
    )
    resultFinal = translateService.translate_text(Text=result.Key.id,
                                  SourceLanguageCode="auto",
                                  TargetLanguageCode=result.Key.languague);
    

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(resultFinal['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response