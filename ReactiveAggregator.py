from helper_functions import lift, combine, lower
from FlatFAT import FlatFAT


# FlatFAT.update(list(dict("type", "arg", "max"))) where type is one of "trigger", "insert", "evict"

class ReactiveAggregator:
    """Reactive Aggregator for IStream and ArgMax"""

    def __construct__(self):
        self.flatFAT = FlatFAT()

    def insert(self, events):
        self.flatFAT.evaluate(events)

    def evict(self, events):
        self.flatFAT.evaluate(events)

    def trigger(self, events):
        self.flatFAT.evaluate(events)
