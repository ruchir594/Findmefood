import os
import web
import json
import requests
import dotenv
import logging

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

print(os.environ.get("PAGE_ACCESS_TOKEN"))

urls = (
    "/hookmeup", "index",
)

def push(id, message):
    response = requests.post("https://graph.facebook.com/v2.6/me/messages", 
        data=json.dumps({
            "recipient": {
                "id": id
            },
            "message": {
                "text": message
            }
        }),
        params={
            "access_token": os.environ.get("PAGE_ACCESS_TOKEN")
        },
        headers={
            "content-type": "application/json"
        }
    )
    return json.loads(response.text)

class index(object):
    def __init__(self):
        self.requests = []

    def GET(self):
        web.header("Content-Type", "text/plain")
        query = web.input()
        return query['hub.challenge']

    def POST(self):
        # let's get some server events here..
        raw = web.data()
        if raw:
            payload = json.loads(raw)
        if "messaging" in payload["entry"][0]:
            for message in payload["entry"][0]["messaging"]:
                text = ""
                if "postback" in message:
                    text = json.dumps(message["postback"])
                elif "message" in message:
                    text = message["message"]["text"]
                return push(message["sender"]["id"], text)

        return push(message["sender"]["id"], "So something went wong there.. IYKWIM")

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()