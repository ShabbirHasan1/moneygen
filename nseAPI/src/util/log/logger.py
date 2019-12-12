from util.slack import SlackWebhook
from util.sendgrid import EmailAPI

# TODO: Properly implement different levels of logging
# TODO: Add process id support
# @body: Use python logging module

# TODO: Add TCPserver support
# @body: Use python logging module

# TODO: Add sendgrid support

class Logger:
    def __init__():
        pass

    @staticmethod
    def info(message: str, push_to_slack=False, push_to_sendgrid=False, sendgrid_subject=None):
        if push_to_slack:
            Logger.info('Pushing message to slack: '+str(SlackWebhook().send(message)))
        if push_to_sendgrid:
            Logger.info('Pushing to sendgrid:' + str(EmailAPI().send(subject='INFO: ' + sendgrid_subject, body=message)))
        print(message)

    @staticmethod
    def err(message: str, push_to_slack=False, push_to_sendgrid=False, sendgrid_subject=None):
        if push_to_slack:
            Logger.info('Pushing message to slack: '+str(SlackWebhook().send(message)))
        if push_to_sendgrid:
            Logger.info('Pushing to sendgrid:' + str(EmailAPI().send(subject='ERROR: '+sendgrid_subject, body=message)))
        print(message)

    @staticmethod
    def warn(message: str, push_to_slack=False, push_to_sendgrid=False, sendgrid_subject=None):
        if push_to_slack:
            Logger.info('Pushing message to slack: '+str(SlackWebhook().send(message)))
        if push_to_sendgrid:
            Logger.info('Pushing to sendgrid:' + str(EmailAPI().send(subject='WARNING: ' + sendgrid_subject, body=message)))
        print(message)

