import subprocess
import boto3
import os
import glob

s3 = boto3.client("s3")
sns = boto3.client("sns")


# I was insidcated while reading some infomation about the /tmp storage that it doesn't empty out after usage.
# I added this clean_out code to empty /tmp before and after our "main" function runs it's proccesses.
def clean_out_tmp():
    for file in glob.glob("/tmp/*.jpg"):
        try:
            os.remove(file)
        except Exception as error:
            print(f"Failed to remove {file} from /tmp: {error}")

    for file in glob.glob("/tmp/*.mp4"):
        try:
            os.remove(file)
        except Exception as error:
            print(f"Failed to remove {file} from /tmp: {error}")


def main(event, context):
    # clean the tmp storage first
    clean_out_tmp()

    # Read the S3 event and obtain the bucket name and object key
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]

    # Make sure the S3 object key suffix is .mp4 as this is what file type our code expects.
    # This also prevents against an uncontrolled loop between S3 and Lambda when using the same bucket for DL and UL.
    # Dispite this, different buckets should be used as best practice

    # It's also bad practice as our function will still be called via the S3 event object.
    # If you"re paying $$, that counts as an invocation.

    if not object_key.endswith(".mp4"):
        return {"statusCode": 200, "body": "Not an mp4 file."}

    input_path = "/tmp/input.mp4"
    output_path_pattern = "/tmp/thumb_%03d.jpg"

    # Handling the object DL from S3
    try:
        s3.download_file(bucket_name, object_key, input_path)
    except Exception as error:
        print(f"Download from S3 failed: {error}")
        return {"statusCode": 404, "body": "Download from S3 failed"}

    ffmpeg_path = "./bin/ffmpeg"

    ffmpeg_cmd = [
        ffmpeg_path,
        "-i",
        input_path,
        "-vf",
        "fps=1/60",
        output_path_pattern,
    ]

    # Handles the mp4 to thumb nail proccess
    # The "try" segemnt has two prints for logging stages as ffmpeg runs
    try:
        print("Proccessing MP4...")
        subprocess.run(ffmpeg_cmd, check=True)
        print("Proccess Complete")
    except subprocess.CalledProcessError as error:
        print(f"MP4 subprocces has failed: {error.returncode}")
        print(error.stderr)
        print(error.stdout)
        return {"statusCode": 500, "body": "ffmpeg failed to process the file."}

    # Error handling for uploading the thumb nails back to S3
    for each_file in glob.glob("/tmp/*.jpg"):
        try:
            filename = os.path.basename(each_file)
            s3.upload_file(each_file, bucket_name, f"thumbnails/{filename}")
        except Exception as error:
            print(f"Upload to S3 failed: {error}")
            return {"statusCode": 500, "body": "Upload to S3 failed"}

    sns_message = f"The uploaded file '{object_key}' was proccessed into thumb nails"

    topic_arn = os.environ.get("SNS_TOPIC_ARN")

    # Checks if eviron var value exists under the key: "SNS_TOPIC_ARN"
    if not topic_arn:
        return {"Status code": 404, "Body": "Failed to locate SNS Environ Var"}

    # Handles error if puslish to SNS action fails.
    try:
        sns.publish(TopicArn=topic_arn, Message=sns_message)
    except Exception as error:
        print(f"Failed to publish message to SNS: {error}")
        return {"statusCode": 500, "body": "Failed to publish message to SNS"}

    # Finally, clean the tmp storage
    clean_out_tmp()

    return {"statusCode": 200, "body": "MP4 processed to thumb nails successfully."}
