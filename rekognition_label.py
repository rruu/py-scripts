import boto3
import sys
import json


if len(sys.argv) < 2 or len(sys.argv) > 2:
    print("Usage: %s [bucket_name]" % (str(sys.argv[0])))
    sys.exit(1)

BUCKET = sys.argv[1]

def detect_labels(bucket, key, max_labels=10, min_confidence=90):
    rekognition = boto3.client("rekognition")
    response = rekognition.detect_labels(
        Image={
        "S3Object": {
        "Bucket": BUCKET,
        "Name": KEY,
    }
        },
        MaxLabels=max_labels,
        MinConfidence=min_confidence,
    )
    print(response['Labels'])


client = boto3.client('s3')
response = client.list_objects_v2(Bucket=BUCKET)

for object in response['Contents']:
    KEY = (object['Key'])
    hs = (object['ETag'][1:-1])
    print("{} {}".format(KEY,hs))
    detect_labels(BUCKET, KEY)


