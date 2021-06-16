from helper_functions import lift, combine, lower
from FlatFAT import FlatFAT


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

