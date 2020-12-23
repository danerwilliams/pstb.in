######################
# Imports
######################
import cgi
from io import BytesIO
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
app.api.binary_types.append('multipart/form-data')
s3 = boto3.client('s3')
mimetypes = {
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'bmp': 'image/bmp',
    'tiff': 'image/tiff',
    'txt': 'text/plain',
    'pdf': 'application/pdf'
}



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

def parse_file(request):
    '''Parses out file from multipart/form-data file upload in post request'''
    rfile = BytesIO(request.raw_body)
    content_type = request.headers['content-type']
    _, parameters = cgi.parse_header(content_type)
    parameters['boundary'] = parameters['boundary'].encode('utf-8')
    parsed = cgi.parse_multipart(rfile, parameters)
    return parsed


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
            return {'statusCode': 69, 'body': {'error': 'failed to shorten url'}} 

    return {
            'statusCode': 200, 
            'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS, POST, PUT'
                       },
            'body': {'url': 'pstb.in/' + short}
           }

@app.route('/upload', methods=['POST'], cors=True, content_types=['multipart/form-data'])
def upload_file():
    '''returns shortened url for the desired '''
    body = parse_file(app.current_request)    
    source_name = body['name'][0]

    # randomly generate new id until one is available
    length = get_id_length('f') # pasted files are stored in the f folder of bucket
    extension = source_name.split('.')[-1]
    while True:
        name = get_random_id(length) 
        if '.' in source_name:
            name += '.' + extension
        try: # name is already used
            boto3.resource('s3').Object('www.pstb.in', name).load()
        except ClientError as e: # name hasn't been used yet
            break

    # Get mimetypes if common filetype to be displayed in browser
    global mimetypes
    type = 'binary/octet-stream' #default type
    if extension in mimetypes:
        type = mimetypes[extension]

    with open('/tmp/' + name, 'wb') as f:
        f.write(body['file'][0])
        try:
            s3.upload_file('/tmp/' + name, 'www.pstb.in', 'f/' + name, ExtraArgs = {'ContentType': type})
        except:
            return {'statusCode': 69, 'body': {'error': 'failed to upload file'}} 

    return {
            'statusCode': 200, 
            'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS, POST, PUT'
                       },
            'body': {'url': 'pstb.in/f/' + name}
           }

