######################
# Imports
######################
import logging
import random
import string
import re
import boto3
from botocore.exceptions import ClientError
from chalice import Chalice


########################
# Globals
########################
app = Chalice(app_name='pstbin')
s3 = boto3.client('s3')


#########################
# Utilities
#########################
def get_id_length(folder = '')->int:
    '''calculates an id length recommendation based on bucket capacity'''
    bucket = boto3.resource('s3').Bucket('www.pstb.in')

    if folder:
        capacity = sum(1 for _ in bucket.objects.filter(Prefix= folder + '/')) # counts number of objects in a specified folder
    else:
        capacity = sum(1 for _ in bucket.objects.filter(Delimiter='/')) # counts number of objects in root of bucket

    recommended_length = 8
    # C^R(n,r) = (n+r-1)!/r!(n-1)!  , where there are n=26 letters + 10 integers and r = length
    max_capacities = [666, 8436, 82251, 658008, 4496388, 26978328]
    for index, max_capacity in enumerate(max_capacities):
        if capacity < max_capacity//2: #keep bucket under half of maximum capacity
            recommended_length = index + 2
            break

    return recommended_length

def get_random_id(length=8)->str:
    '''Generates a random id for the file to be uploaded'''
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def format_target_url(url)->str:
    '''cleans up input url aka github.com returns https://github.com, return None if invalid url'''
    regex = re.compile(r'(https?://)?(.*)')
    match = regex.search(url)
    if match:
        url = match.group(2)
    else:
        return None

    return 'http://' + url


########################
# API Routes
########################
@app.route('/shorten', methods=['POST'], cors=True, content_types=['application/x-www-form-urlencoded', 'text/plain'])
def get_shortened_url():
    '''returns shortened url for the desired '''
    # post request data
    body = app.current_request.raw_body.decode("utf-8")

    # randomly generate new id until one is available
    length = get_id_length() # url redirect objects are stored in top level folder of bucket
    while True:
        short = get_random_id(length)
        try: # name is already used
            boto3.resource('s3').Object('www.pstb.in', short).load()
        except ClientError as e: # name hasn't been used yet
            break

    target_url = format_target_url(body)
    if not target_url:
        return {'statusCode': 69, 'body': {'error': 'invalid url'}}

    with open('/tmp/totally_arbitrary_file', 'w') as _:
        try:
            s3.upload_file('/tmp/totally_arbitrary_file', 'www.pstb.in', short, ExtraArgs = {'WebsiteRedirectLocation': target_url, 'Tagging': 'url'})
        except:
            return {'statusCode': 69, 'body': {'error': 'invalid url'}} 

    return {
            'statusCode': 200, 
            'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS, POST, PUT'
                       },
            'body': {'url': 'pstb.in/' + short}
           }

@app.route('/upload', methods=['POST'], cors=True)
def get_s3_presigned_url():
    '''returns the presigned url for uploading file to the s3 bucket'''
    body = app.current_request.json_body
    length = get_id_length('f') # pasted files are stored in the f folder of bucket
    while True:
        name = get_random_id(length) 
        if '.' in body['name']:
            name += '.' + body['name'].split('.')[1]
        try: # name is already used
            boto3.resource('s3').Object('www.pstb.in', name).load()
        except ClientError as e: # name hasn't been used yet
            break

    try: 
        result = {
                  'signed_url': s3.generate_presigned_url(
                                                    ClientMethod = 'put_object',
                                                    Params       = {
                                                                    'Bucket': 'www.pstb.in',
                                                                    'Key': 'f/' + name,
                                                                    'ContentType': body['type']
                                                                    },
                                                    ExpiresIn    = 3600
                                                  ),
                  'url': 'pstb.in/f/' + name
                 }
    except ClientError as e:
        result = {"error": "could not generate s3 presigned url"}
        response = {
                    'statusCode': 69,
                    'headers': {
                                'Access-Control-Allow-Headers': 'Content-Type',
                                'Access-Control-Allow-Origin': '*',
                                'Access-Control-Allow-Methods': 'OPTIONS, POST, PUT'
                               },
                    'body': result
                   }

    response = {
                'statusCode': 200,
                'headers': {
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'OPTIONS, POST, PUT'
                           },
                'body': result
               }

    return response

