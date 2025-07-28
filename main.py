import subprocess

# vid_file = sys.argv

vid = "Kill_Bill.mp4"


def main(mp4):
    ffmpeg_cmd = [
        "ffmpeg",
        "-i",
        mp4,
        "-vf",
        "fps=1/60",
        "-s 320x240",
        "-f",
        "image2",
        "thumb_nails/tn-%03d.jpeg",
    ]

    subprocess.run(ffmpeg_cmd)

    return {"statusCode": 200, "body": "Hello, Lambda!"}


main(vid)
