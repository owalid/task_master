from ParsingEnum import SUBSCRIPTIONS_CAT

class EventListenerOptions:
    def __init__(self, activated=False, mail='' ):
        self.activated = activated
        self.mail = mail