import json


class Event:
    def __init__(self, event_id, name, data):
        self.event_id = event_id
        self.name = name
        self.data = data
        self.sent = False
        self.resolved = False

    def json(self):
        return json.dumps({'event': self.name, 'data': self.data, 'event_id': self.event_id})
