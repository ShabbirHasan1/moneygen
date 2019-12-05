import requests
from config import Config
import json


class SlackWebhook:
    def __init__(self, webhook=Config.SLACK_WEBHOOK):
        self.webhook_url = webhook

    def send(self, data):
        # Importing it here to avoid error due to circular dependency
        from util.log import Logger
        '''Data can be dict, str, int, list'''
        Logger.info('Sending slack message to: ' + self.webhook_url)
        data = json.dumps({'text': data})
        res = requests.post(self.webhook_url, data)
        return res