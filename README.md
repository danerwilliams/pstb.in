# pstb.in
> Pastebin and url shortener made in serverless AWS

![screenshot](./screenshot.jpg)

## Permissions
S3 buckets permissions have given me many issues, here are my settings:
  

Bucket Policy:
```
{
    "Version": "2012-10-17",
    "Id": "Policyxxxxxxxxxxx",
    "Statement": [
        {
            "Sid": "Stmtxxxxxxxxxxx",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::bucketName/*"
        },
        {
            "Sid": "Stmtxxxxxxxxxxxxx",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::xxxxxxxxxxxx:role/roleName"
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:PutObjectTagging"
            ],
            "Resource": "arn:aws:s3:::bucketName/*"
        },
        {
            "Sid": "Stmtxxxxxxxxxxxxxx",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::xxxxxxxxxxxx:role/roleName"
            },
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::bucketName"
        }
    ]
}
```
  
  
CORS Configuration:
```
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "PUT"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]
```

## Troubleshooting
* Chalice may cause permissions issues with the generated lambda functions, see [this issue](https://github.com/aws/chalice/issues/1606)
