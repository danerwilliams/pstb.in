#!/usr/bin/env python3
import boto3
import requests
import json
import requests
import re

def format_target_url(url)->str:
    '''cleans up input url aka github.com returns https://github.com, return None if invalid url'''
    regex = re.compile(r'(https?://)?(.*)')
    match = regex.search(url)
    if match:
        url = match.group(2)
    else:
        return None

    try: #first try https
        requests.get('https://' + url)
        return 'https://' + url
    except:
        try: # then try http
            requests.get('http://' + url)
            return 'http://' + url
        except: # otherwise invalid
            return None

    return None


    
def main():
    print(format_target_url('github.com'))
    print(format_target_url('pstb.in/fuck'))
    print(format_target_url('sdfjslkdf;;ljaw;ljf'))
    # s3 = boto3.client('s3')
    # bucket = boto3.resource('s3').Bucket('www.pstb.in')
    # print(sum(1 for _ in bucket.objects.filter(Delimiter='/'))) # counts number of objects in root of bucket
    # with open('/tmp/test', 'w') as _:
    #     response = s3.upload_file('/tmp/test', 'www.pstb.in', 'newtest', ExtraArgs = {'WebsiteRedirectLocation': 'github.com'})
    # print(response)

    # tructus = {'type': 'image/png', 'name': 'test.png'}
    # response = requests.post('https://1vey8nkf2j.execute-api.us-west-1.amazonaws.com/api/', json=tructus)
    # guy = response.json()
    # print(guy)

    # headers = {'Content-Type': 'image/png', 'x-amz-website-redirect-location': 'https://github.com'}
    # f = open('./test.png', 'rb')
    # result = requests.put(guy['body']['url'], headers=headers, data=f)
    # print(result.text)

    # tructus = {'type': '', 'name': 'test'}
    # response = requests.post('https://1vey8nkf2j.execute-api.us-west-1.amazonaws.com/api/', json=tructus)
    # guy = response.json()
    # print(guy)

    # headers = {'x-amz-website-redirect-location': 'https://github.com'}
    # f = open('./test', 'rb')
    # result = requests.put(guy['body']['url'], headers=headers, data=f)
    # print(result.text)

    # tructus = {'type': 'image/png', 'name': 'test.png'}
    # response = requests.post('https://1vey8nkf2j.execute-api.us-west-1.amazonaws.com/api/', json=tructus)
    # guy = response.json()
    # print(guy)

    # headers = {'Content-Type': 'image/png'}
    # f = open('./test.png', 'rb')
    # result = requests.put(guy['body']['url'], headers=headers, data=f)
    # print(result)


if __name__ == '__main__':
    main()