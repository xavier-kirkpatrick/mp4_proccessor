import boto3
import os

s3 = boto3.client("s3")

my_bucket_name = "mp4-zip-store"

file_path = "mp4_files/Kill_Bill.mp4"


def upload_file_s3(file_to_upload, bucket_name):
    if not os.path.exists(file_to_upload):
        print("Unable to locate file to upload")
        return {"statusCode": 404, "body": "File to upload not found"}
    try:
        print("Uploading file to S3...")
        with open(file_to_upload, "rb") as f:
            s3.put_object(
                Bucket=bucket_name, Key=os.path.basename(file_to_upload), Body=f
            )
        print("Upload complete")
        return {"statusCode": 200, "body": "File uploaded successfully"}

    except Exception as error:
        print("Upload to S3 failed: ", error)
        return {"statusCode": 500, "body": "Upload to S3 failed"}


upload_file_s3(
    file_path,
    my_bucket_name,
)

#  permanently delete
