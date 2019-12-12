import requests
from config import Config


class EmailAPI:
    def __init__(self, api_key=Config.SENDGRID_API_KEY):
        self.api_key = api_key
        self.headers = {
            'Authorization': 'Bearer ' + self.api_key
        }
        self.url = Config.SENDGRID_API_ENDPOINT

    def send(
        self,
        subject: str,
        body: str, msg_type='text/html', 
        from_email='logs.moneygen.com', 
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
        res = requests.post(self.url, data=data, headers=self.headers)
        return res