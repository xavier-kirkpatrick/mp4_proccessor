import subprocess
import boto3
import os

s3 = boto3.client("s3")
sns = boto3.client("sns")


# This function was version/attempt 1 and is no longer valid.
# The current and functional code is in main.py inside the "lambdaZipBluePrint" folder


def main(event, context):
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]

    if not object_key.endswith(".mp4"):
        return {"statusCode": 200, "body": "Not an mp4 file."}

    input_path = "/tmp/input.mp4"
    output_path = "/tmp/thumb.jpg"

    filename_without_ext = os.path.splitext(os.path.basename(object_key))[0]
    thumbnail_key = f"thumbnails/{filename_without_ext}.jpg"

    s3.download_file(bucket_name, object_key, input_path)

    ffmpeg_cmd = [
        "/opt/ffmpeg/ffmpeg",
        "-i",
        input_path,
        "-vf",
        "fps=1/60",
        output_path,
    ]

    subprocess.run(ffmpeg_cmd, check=True)

    s3.upload_file(output_path, bucket_name, thumbnail_key)

    sns_message = f"The uploaded file '{object_key}' was proccessed into thumb nails"

    topic_arn = os.environ["SNS_TOPIC_ARN"]

    sns.publish(TopicArn=topic_arn, Message=sns_message)

    return {"statusCode": 200, "body": "Word count processed successfully."}
