from ParsingEnum import SUBSCRIPTIONS_CAT

class EventListener:
    def __init__(self, activated=False, subscriptions=SUBSCRIPTIONS_CAT.PROCESS_STATES.value, options='' ):
        self.activated = activated
        self.subscriptions = subscriptions
        options = options 