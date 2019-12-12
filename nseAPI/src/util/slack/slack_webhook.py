import requests
from config import Config
import json


class SlackWebhook:
    def __init__(self, webhook=Config.SLACK_WEBHOOK):
        self.webhook_url = webhook

    def send(self, data):
        '''Data can be dict, str, int, list'''
        data = json.dumps({'text': data})
        res = requests.post(self.webhook_url, data)
        return res