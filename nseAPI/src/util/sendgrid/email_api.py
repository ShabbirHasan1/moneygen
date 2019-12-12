import requests
from config import Config
import json


class EmailAPI:
    def __init__(self, api_key=Config.SENDGRID_API_KEY):
        self.api_key = api_key
        self.headers = {
            'Authorization': 'Bearer ' + self.api_key,
            'Content-Type': 'application/json'
        }
        self.url = Config.SENDGRID_API_ENDPOINT

    def send(
        self,
        subject: str,
        body: str, msg_type='text/html', 
        from_email='logs@moneygen.com', 
        to_email=Config.SENDGRID_TO_EMAIL):

        data = {
                "personalizations": [
                    {
                    "to": [
                        {
                        "email": to_email
                        }
                    ],
                    "subject": subject
                    }
                ],
                "from": {
                    "email": from_email
                },
                "content": [
                    {
                    "type": msg_type,
                    "value": body
                    }
                ]
                }
        payload = json.dumps(data)
        res = requests.post(self.url, data=payload, headers=self.headers)
        return res