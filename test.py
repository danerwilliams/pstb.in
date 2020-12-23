#!/usr/bin/env python3

import boto3
import requests

r = requests.post('https://ez02ob0o22.execute-api.us-west-1.amazonaws.com/api/upload', files={'file': open('test.png', 'rb'), 'name': 'test.png'})

print(r.text)