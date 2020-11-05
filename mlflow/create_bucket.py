
from minio import Minio
from minio.error import ResponseError
import json
import os

minioClient = Minio("http://localhost:9000".split('//')[1],
                  access_key="ACCESSKEY",
                  secret_key="SECRETKEY",
                  secure=False)

minioClient.list_buckets()

try:
    minioClient.make_bucket('mlflow')
except ResponseError as err:
    print(err)

buckets = minioClient.list_buckets()
for bucket in buckets:
    print(bucket.name, bucket.creation_date)

policy = {"Version":"2012-10-17",
        "Statement":[
            {
            "Sid":"",
            "Effect":"Allow",
            "Principal":{"AWS":"*"},
            "Action":"s3:GetBucketLocation",
            "Resource":"arn:aws:s3:::mlflow"
            },
            {
            "Sid":"",
            "Effect":"Allow",
            "Principal":{"AWS":"*"},
            "Action":"s3:ListBucket",
            "Resource":"arn:aws:s3:::mlflow"
            },
            {
            "Sid":"",
            "Effect":"Allow",
            "Principal":{"AWS":"*"},
            "Action":"s3:GetObject",
            "Resource":"arn:aws:s3:::mlflow/*"
            },
            {
            "Sid":"",
            "Effect":"Allow",
            "Principal":{"AWS":"*"},
            "Action":"s3:PutObject",
            "Resource":"arn:aws:s3:::mlflow/*"
            }

        ]}

minioClient.set_bucket_policy('mlflow', json.dumps(policy))

# List all object paths in bucket that begin with my-prefixname.
objects = minioClient.list_objects('mlflow', prefix='my',
                              recursive=True)
for obj in objects:
    print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
          obj.etag, obj.size, obj.content_type)
