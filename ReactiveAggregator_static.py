from helper_functions import lift, combine, lower
from FlatFAT_static_size import FlatFATs as FlatFAT


# FlatFAT.update(list(Event), type) where type is one of "trigger", "insert", "evict"

class ReactiveAggregatorStatic:
    """Reactive Aggregator for IStream and ArgMax"""

    def __init__(self, size=128):
        self.flatFAT = FlatFAT(size)

    def insert(self, events):
        if len(events) == 0:
            return
        updated = False
        while not updated:
            try:
                self.flatFAT.update(events, "insert")
                updated = True
            except ValueError as e:
                raise ValueError("Would resize bigger")
                # print('resizing bigger', end='\b'*15)
                # locations = self.flatFAT.getLocations()
                # self.flatFAT = FlatFAT(self.flatFAT.getSize()*2)
                # self.flatFAT.new(locations)
        ffSize = self.flatFAT.getSize()
        if ffSize - self.flatFAT.getLocations().count(None) < ffSize/4 and ffSize > 1:
            print('resizing smaller', end='\b'*16)
            locations = self.flatFAT.getLocations()
            self.flatFAT = FlatFAT(ffSize//2)
            self.flatFAT.new(locations)

    def evict(self, events):
        if len(events) == 0:
            return
        self.flatFAT.update(events, "evict")


    def trigger(self, events):
        if len(events) == 0:
            return
        self.flatFAT.update(events, "trigger")

    def submit(self):
        return self.flatFAT.aggregate()
