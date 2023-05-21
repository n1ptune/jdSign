import requests
from urllib.parse import urlencode

from jdSign import getSignWithstv
base_url = "https://api.m.jd.com/client.action?"

QueryString = {
    "functionId" : "device",
    "lmt" : "0",
    "clientVersion" : "12.0.1",
    "build" : "98778",
    "client" : "android",
    "partner" : "oppo",
    "sdkVersion" : "28",
    "lang" : "zh_CN",
    "harmonyOs" : "0",
    "networkType" :"wifi",
    "uemps" : "2-2-2",
    "ext" : '{"prstate":"0","pvcStu":"1","cfgExt":"{\"privacyOffline\":\"0\"}"}',
    "avifSupport" : "1",
    "eid" : "",
    "ef" : "1",
    "ep" : ''
}

uuid = "ac9cdd4119f45c4e"
body = {
    "brand":"OnePlus",
    "clientVersion":"12.0.1",
    "model":"ONEPLUS A6000",
    "nettype":"WIFI",
    "osVersion":"9",
    "partner":"oppo",
    "platform":"100",
    "screen":"2075*1080",
    "uuid": uuid 
}
post_data = {
    "lmt" : "0",
    "body" : str(body)
}
def parse_url(inData : dict):
    return base_url + urlencode(inData) + "&" +  getSignWithstv(inData["functionId"], post_data["body"], body["uuid"], inData["client"], inData["clientVersion"])

url = parse_url(QueryString)
r = requests.post(url, data = post_data)
print(r.text)


