class Event:
    def __init__(self, timestamp, key, value):
        self.timestamp = timestamp
        self.key = key
        self.value = value

    def getKey(self):
        return self.key

    def __repr__(self):
        return f"Event(timestamp={self.timestamp}, key={self.key}, value={self.value})"

    def to_dict(self):
        pass
