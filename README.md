https://github.com/BtbN/FFmpeg-Builds/releases

ffmpeg-n6.1-latest-linux64-gpl-6.1.tar.xz 

sha256:7b9b71754e90b557b79c2d8aad3a6f5ac7d3662ad0de954d62bc5fafe785d18f

- Before editing anymore code please do so in a newly made branch.

Main Lambda code file can be found in "lambdaZipBluePrint/main.py"

The raw binary for ffmpeg is not at "lambdaZipBluePrint/bin/ffmpeg" as it's too large for GH.
It can though, be found inside compressed inside lambda-ffmpeg.zip. 

The file lambda-ffmpeg.zip is also ready be run in a lambda.

It will probably need to be applyed via an S3 bucket due to size.