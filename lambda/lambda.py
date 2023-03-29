import json 
import boto3
import random  
import string 
import os
import logging

logger = logging.getLogger()
logger.setLevel(int(os.environ.get('LOG_LEVEL')))

def lambda_handler(event, context):

    try:
        #Get BucketName & FQDNName from the Env
        bucketName = os.environ.get('BUCKET_NAME')
        fqdnName = os.environ.get('FQDN_NAME')

        if (bucketName is None or not bucketName.strip()):
            return{'statusCode':400,'body': json.dumps({'Configuration Error': 'BUCKET_NAME is empty'}) }
        if (fqdnName is None or not fqdnName.strip()):
            return{'statusCode':400,'body': json.dumps({'Configuration Error': 'FQDN_NAME is empty'}) }
            
        if (event is None or not 'body' in event or event['body'] is None):
            return{'statusCode':400,'body': json.dumps({'Configuration Error': 'BODY is not available in the event'}) }
        
        #Get Reqest Body and act-URL from event
        body = json.loads(event['body'])
        
        if (body is None or not body):
            return{'statusCode':400,'body': json.dumps({'Request Error': 'BODY is empty'}) }
            
        if (not 'act-URL' in body):
            return{'statusCode':400,'body': json.dumps({'Request Error': 'act-URL is missing in POST Body'}) }

        actURL = body['act-URL']
        if (actURL is None or not actURL.strip()):
            return{'statusCode':400,'body': json.dumps({'Request Error': 'act-URL is empty'}) }
        
        #Generate x digit random alphanumeric string as keyName
        keyName = specific_string(5)
        
        #Connect to S3 Bucket
        s3Bucket = boto3.client('s3')
        
        #Create Object with Redirection set
        putResponse = s3Bucket.put_object(Bucket=bucketName,
            ContentType='text/html',
            WebsiteRedirectLocation= actURL,
            Key=keyName
            )
        #Log details
        logger.info(actURL + " -> " + fqdnName + keyName)
        return {
            'statusCode': 200,
            'body': json.dumps({'sURL': fqdnName + keyName})
        }
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return{
             'statusCode': 400,
            'body': json.dumps({'Exception': str(e)})
        }
        
def specific_string(length):  
    # define the condition for random string  
    result = ''.join(random.choices(string.ascii_uppercase + string.digits, k = length))
    return(result)
