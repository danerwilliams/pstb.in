# pstb.in
> Paste bin and url shortener


## Configurations

### S3
##### Bucket Policy
```
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::pstbin/*"
        }
    ]
}
```
##### CORS Policy
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
