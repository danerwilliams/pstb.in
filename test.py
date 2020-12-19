#!/usr/bin/env python3
import boto3
import requests
import json

def main():
    s3 = boto3.client('s3')
    print(s3.get_bucket_acl(Bucket='imessage-viz'))

    tructus = {'type': 'image/png', 'name': 'FisherBasementLogo.png'}
    response = requests.post('https://68fwpup9dc.execute-api.us-west-1.amazonaws.com/api/', json=tructus)
    guy = response.json()

    headers = {'Content-Type': 'image/png'}
    f = open('./FisherBasementLogo.png', 'rb')
    result = requests.put(guy['body']['url'], headers=headers, data=f)


if __name__ == '__main__':
    main()