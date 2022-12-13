import requests, io
from mastodon import Mastodon

#create a mastodon object
m = Mastodon(access_token="freebooksbot_usercred.secret")

#Image source - first Packt, then Gutenburg
#metadata = m.media_post("https://static.packt-cdn.com/products/9781788992879/cover/smaller", mime_type="image/jpg")
#print(metadata)

#upload file with requests
with open("freebooksbot_usercred.secret") as f: authorization_token = f.readline()[:-1]
headers = {"Authorization": "Bearer " + authorization_token, "User-Agent":"freebooksbot"}
img = requests.get("https://static.packt-cdn.com/products/9781788992879/cover/smaller")
#print(img.content)
body = {"file":io.BytesIO(img.content)}
data = {'upload': ''}
metadata = requests.post("https://botsin.space/api/v2/media", data=data, headers=headers, files=body)
#print(metadata.json()["id"])


#Post
m.status_post("This post contains an image from Packt Publishing!", media_ids=metadata.json()["id"])


