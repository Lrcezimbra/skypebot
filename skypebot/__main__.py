import importlib

from decouple import config
from skpy import SkypeEventLoop, SkypeNewMessageEvent

import skypebot


ACCEPTED_SELF_MESSAGES = skypebot.KEYWORDS['allegro']


class SkypePing(SkypeEventLoop):
    def __init__(self, username, password):
        super(SkypePing, self).__init__(username, password)

    def onEvent(self, event):
        try:
            if not isinstance(event, SkypeNewMessageEvent):
                return

            msg = event.msg.content.lower()
            is_accepted_self_message = msg in ACCEPTED_SELF_MESSAGES
            if event.msg.userId == self.userId and not is_accepted_self_message:
                return

            print(msg)

            importlib.reload(skypebot)
            skypebot.handle(event)

        except Exception as e:
            print(e)
            print('PAREM DE TENTAR ME MATAR!!!11!!ONZE!!')


if __name__ == '__main__':
    SKYPE_LOGIN = config('SKYPE_LOGIN')
    SKYPE_PASSWORD = config('SKYPE_PASSWORD')

    sk = SkypePing(SKYPE_LOGIN, SKYPE_PASSWORD)
    sk.setPresence()
    sk.loop()
