import boto3

s3 = boto3.client("s3")

url = s3.generate_presigned_url(
    "put_object",
    Params={
        "Bucket": "",
        "Key": "",
        "ContentType": "video/mp4",
    },
    ExpiresIn=600,  # seconds
)

print("Pre-signed URL:", url)
