class Event:
    def __init__(self, timestamp, key, value):
        self.timestamp = timestamp
        self.key = key
        self.value = value

    def getKey(self):
        return self.key

    # allow comparison to other Event-Instances as well as our internal Dict structure
    def __eq__(self, other):
        if other is None:
            return False
        elif isinstance(other, Event):
            return self.key == other.key
        else:
            try:
                return self.key == other["arg"]
            except KeyError:
                return False

        return False

    def __hash__(self):
        return self.key.__hash__()

    def __repr__(self):
        return f"Event(timestamp={self.timestamp}, key={self.key}, value={self.value})"

    def to_dict(self):
        pass
