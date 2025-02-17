import uuid


class Action:
    name = None

    def __init__(self):
        self.action_id = str(uuid.uuid4().int)
        self.sent = False
        self.resolved = False

    def json(self):
        return {'action': self.name, 'data': self.data(), 'action_id': self.action_id}

    def data(self):
        raise NotImplemented()
