import requests

def get():
    req = requests.get("https://api.ipify.org/?format=text")
    res = req.text

    return res