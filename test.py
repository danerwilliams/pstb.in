#!/usr/bin/env python3
import boto3
s3 = boto3.client('s3')
with open('/tmp/totally_arbitrary_file', 'w') as _:
    s3.upload_file('/tmp/totally_arbitrary_file', 'www.pstb.in', "test", ExtraArgs = {'WebsiteRedirectLocation': 'http://google.com', 'Tagging': 'url'})

bucket = boto3.resource('s3').Bucket('www.pstb.in')
capacity = sum(1 for _ in bucket.objects.filter(Delimiter= '/')) # counts number of objects in a specified folder
print(capacity)

