from helper_functions import lift, combine, lower
from FlatFAT import FlatFAT


# FlatFAT.update(list(dict("type", "arg", "max"))) where type is one of "trigger", "insert", "evict"

class ReactiveAggregator:
    """Reactive Aggregator for IStream and ArgMax"""

    def __init__(self):
        self.flatFAT = FlatFAT()

    def insert(self, events):
        self.flatFAT.update(events, "insert")

    def evict(self, events):
        self.flatFAT.update(events, "evict")

    def trigger(self, events):
        self.flatFAT.update(events, "trigger")

    def submit(self):
        return self.flatFAT.aggregate()
