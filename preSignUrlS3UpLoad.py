import requests

with open("", "rb") as f:
    r = requests.put(
        "preSignedUrlHere",
        data=f,
        headers={"Content-Type": "video/mp4"},
    )

print(r.status_code)
print(r.text)
