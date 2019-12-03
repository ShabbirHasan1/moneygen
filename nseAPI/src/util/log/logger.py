from util.slack import SlackWebhook

# TODO: Properly implement different levels of logging
class Logger:
    def __init__():
        pass

    @staticmethod
    def info(message: str, push_to_slack=False):
        if push_to_slack:
            Logger.info('Pushing message to slack: '+str(SlackWebhook().send(message)))
        print(message)

    @staticmethod
    def err(message: str, push_to_slack=False):
        if push_to_slack:
            Logger.info('Pushing message to slack: '+str(SlackWebhook().send(message)))
        print(message)

    @staticmethod
    def warn(message: str, push_to_slack=False):
        if push_to_slack:
            Logger.info('Pushing message to slack: '+str(SlackWebhook().send(message)))
        print(message)

