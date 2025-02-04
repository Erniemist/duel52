import json
import uuid


class Action:
    def __init__(self, name, data):
        self.action_id = str(uuid.uuid4().int)
        self.name = name
        self.data = data
        self.sent = False
        self.resolved = False

    def json(self):
        return {'action': self.name, 'data': self.data, 'action_id': self.action_id}
