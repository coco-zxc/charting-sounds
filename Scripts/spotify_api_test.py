import base64
from json import loads
import requests

client_id = ''
client_secret = ''

def get_token() :
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode ('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers ={
        "Authorization": "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
        }
    data = {"grant_type": "client_credentials"}
    response = loads(requests.post(url, headers=headers, data=data).content)
    token = response["access_token"]
    return token






