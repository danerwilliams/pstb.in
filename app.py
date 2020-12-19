import json
import logging
import random
import string
import boto3
from botocore.exceptions import ClientError
from chalice import Chalice


app = Chalice(app_name='imessage-viz')
s3_client = boto3.client('s3', region_name='us-west-1')


def get_random_id(length=8)->str:
    '''Generates a random id for the file to be uploaded'''
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@app.route('/', methods=['POST'], cors=True)
def get_presigned_url():
    '''returns the presigned url for uploading file to the s3 bucket'''
    file_spec = app.current_request.json_body
    name = get_random_id() + '.' + file_spec['name'].split('.')[1]

    try: 
        result = {'url': s3_client.generate_presigned_url(ClientMethod ='put_object',
                                                          Params = {'Bucket': 'imessage-viz',
                                                                    'Key': 'f/' + name,
                                                                    'ContentType': file_spec['type']
                                                                   },
                                                          ExpiresIn = 30
                                                         ),
                  'name:': name
                 }
    except ClientError as e:
        logging.error(e)
        return {"error": "could not generate s3 presigned url"}

    return result


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
