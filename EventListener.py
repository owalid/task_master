class EventListener:
    def __init__(self, activated=False, subscriptions="PROCESS_STATE", options='' ):
        self.activated = activated
        self.subscriptions = subscriptions
        options = options 