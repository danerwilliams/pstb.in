#!/usr/bin/env python3
import boto3
import requests
import json
import requests
import re

def get_id_length(folder = '')->int:
    '''calculates an id length recommendation based on bucket capacity'''
    bucket = boto3.resource('s3').Bucket('www.pstb.in')
    if folder:
        capacity = sum(1 for _ in bucket.objects.filter(Prefix= folder + '/')) # counts number of objects in a specified folder
    else:
        capacity = sum(1 for _ in bucket.objects.filter(Delimiter='/')) # counts number of objects in root of bucket
    print(capacity)
    capacity = 100000
    recommended_length = 8
    # C^R(n,r) = (n+r-1)!/r!(n-1)!  , where there are n=26 letters + 10 integers and r = length
    max_capacities = [666, 8426, 82251, 658008]
    for index, max_capacity in enumerate(max_capacities):
        if capacity < max_capacity//2: #keep bucket under half of maximum capacity
            recommended_length = index + 2
            break

    return recommended_length

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
    print(get_id_length())
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