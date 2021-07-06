from helper_functions import lift, combine, lower
from math import log, ceil, floor

from event import Event

class FlatFATs(object):

    def __init__(self, size):
        # save at which depth in a binary tree the leafs begin, size is implicitly increased up to next power of 2
        self.leafsDepth = ceil(log(size, 2))
        # more than just the size because we need to save intermediate nodes as well
        self.locations = [None for i in range(2**(self.leafsDepth) -1 + size)]

    def new(self, locations):
        # should only be called on empty trees, does not check if any locations would be overwritten
        if len(locations) > 2**self.leafsDepth:
            raise ValueError("Locations is too much for this tree")
        for i in range(len(locations)):
            if isinstance(locations[i], Event):
                self.locations[2**self.leafsDepth - 1 + i] = lift(locations[i])
            else:
                self.locations[2**self.leafsDepth - 1 + i] = locations[i]
        # update all intermediate results
        self.combine({x for x in range(len(self.locations[2**(self.leafsDepth)-1:]))})


    def update(self, locations, type):
        # fail if any fail (i.e. Catch and raise value error in case trigger or evict have no target)
        try:
            changes = set()
            for location in locations:
                # insert -> find first free slot. evict, trigger -> find first occurence of 'arg'
                if type == "insert":
                    insertInto = self.locations.index(None, 2**self.leafsDepth - 1)
                else:
                    # comparison to location is intended to abuse internal __eq__ method
                    insertInto = self.locations.index(location, 2**self.leafsDepth - 1)
                changes.add(insertInto - 2**self.leafsDepth + 1)
                # evict -> set to None. insert, trigger -> set to given location
                if type == "evict":
                    self.locations[insertInto] = None
                else:
                    self.locations[insertInto] = lift(location)
            # update all intermediate results
            ## TODO maybe make smart location wise updates with indices?
            self.combine(changes)
        except ValueError as e:
            if type == "insert":
                raise ValueError("Not enough space to insert")
            elif type == "trigger":
                raise ValueError("location for trigger could not be found")
            elif type == "evict":
                raise ValueError("location for evict could not be found")
            else:
                raise e

    def prefix(self, i, depth=-1):
        # no depth given, start at bottom by default
        if depth == -1:
            depth = self.leafsDepth
        # 0 -> might be called improperly
        if i == 0:
            return None
        # 1 -> special case because of 2**0
        elif i == 1:
            return self.locations[2**depth - 1]
        # save how many locations still have a full intermediate result one depth above
        toplevel = 2**floor(log(i, 2))
        if toplevel != i:
            # differs by exactly one -> combine stray result with prefix of tree with depth-1
            return combine(self.locations[2**depth - 1 + i - 1], self.prefix(toplevel//2, depth-1))
        else:
            # == i but cannot be 0 -> i is power of 2
            return self.prefix(toplevel//2, depth-1)


    def suffix(self, i, depth=-1):
        if depth == -1:
            depth = self.leafsDepth
        if i == 0:
            return None
        elif i == 1:
            return self.locations[2**(depth+1) - 2]
        toplevel = 2**floor(log(i, 2))
        if toplevel != i:
            if toplevel == 0:
                return self.locations[2**(depth+1) - 2 - i + 1]
            else:
                return combine(self.locations[2**(depth+1) - 2 - i + 1], self.suffix(toplevel//2, depth-1))
        else:
            return self.suffix(toplevel//2, depth-1)

    def combine(self, indices=set()):
        # update all intermediate results, go from leafs to root (range index running to 0)
        for depth in range(self.leafsDepth, -1, -1):
            if len(indices) == 0:
                return
            if depth == self.leafsDepth:
                indices = {nodeIndex//2 for nodeIndex in indices}
                continue
            # run trough depths descending first and through nodes per level ascending second
            indicesInLevel = indices
            indices = set()
            while len(indicesInLevel) > 0:
                nodeIndex = indicesInLevel.pop()
                # check if any of the children are not set and ignore/unset values if necessary
                if self.locations[2**(depth+1) - 1 + 2*nodeIndex] is None:
                    if 2**(depth+1) - 1 + 2*nodeIndex + 1 >= len(self.locations) or self.locations[2**(depth+1) - 1 + 2*nodeIndex + 1] is None:
                        newValue = None
                    else:
                        newValue = self.locations[2**(depth+1) - 1 + 2*nodeIndex + 1]
                else:
                    if 2**(depth+1) - 1 + 2*nodeIndex + 1 >= len(self.locations) or self.locations[2**(depth+1) - 1 + 2*nodeIndex + 1] is None:
                        newValue = self.locations[2**(depth+1) - 1 + 2*nodeIndex]
                    else:
                        newValue = combine(self.locations[2**(depth+1) - 1 + 2*nodeIndex], self.locations[2**(depth+1) - 1 + 2*nodeIndex + 1])
                if self.locations[2**depth - 1 + nodeIndex] != newValue:
                    if depth > 0:
                        indices.add(nodeIndex//2)
                self.locations[2**depth - 1 + nodeIndex] = newValue

    def getLocations(self):
        return self.locations[2**self.leafsDepth - 1:]

    def getSize(self):
        return 2**self.leafsDepth

    def aggregate(self):
        # return root result, may be None if no locations are available
        return self.locations[0]

    def __repr__(self):
        return "FlatFAT()"

    def __str__(self):
        return "FlatFAT(size: %s, maxArg: %s)" % (2**self.leafsDepth, self.aggregate())


if "__name__" == "__main__":
    # some basic functionality testing
    # expected results:

    # 8
    # [{'max': 8, 'arg': '8'}, {'max': 4, 'arg': '4'}, {'max': 8, 'arg': '8'}, {'max': 2, 'arg': '2'}, {'max': 4, 'arg': '4'}, {'max': 6, 'arg': '6'}, {'max': 8, 'arg': '8'}, {'max': 1, 'arg': '1'}, {'max': 2, 'arg': '2'}, {'max': 3, 'arg': '3'}, {'max': 4, 'arg': '4'}, {'max': 5, 'arg': '5'}, {'max': 6, 'arg': '6'}, {'max': 7, 'arg': '7'}, {'max': 8, 'arg': '8'}]
    # [{'max': 8, 'arg': '8'}, {'max': 4, 'arg': '4'}, {'max': 8, 'arg': '8'}, {'max': 2, 'arg': '2'}, {'max': 4, 'arg': '4'}, {'max': 6, 'arg': '6'}, {'max': 8, 'arg': '8'}, {'max': 0, 'arg': '1'}, {'max': 2, 'arg': '2'}, {'max': 3, 'arg': '3'}, {'max': 4, 'arg': '4'}, {'max': 5, 'arg': '5'}, {'max': 6, 'arg': '6'}, {'max': 7, 'arg': '7'}, {'max': 8, 'arg': '8'}]
    # [{'max': 7, 'arg': '7'}, {'max': 4, 'arg': '4'}, {'max': 7, 'arg': '7'}, {'max': 2, 'arg': '2'}, {'max': 4, 'arg': '4'}, {'max': 6, 'arg': '6'}, {'max': 7, 'arg': '7'}, {'max': 0, 'arg': '1'}, {'max': 2, 'arg': '2'}, {'max': 3, 'arg': '3'}, {'max': 4, 'arg': '4'}, {'max': 5, 'arg': '5'}, {'max': 6, 'arg': '6'}, {'max': 7, 'arg': '7'}, None]
    # [{'max': 9, 'arg': '9'}, {'max': 4, 'arg': '4'}, {'max': 9, 'arg': '9'}, {'max': 2, 'arg': '2'}, {'max': 4, 'arg': '4'}, {'max': 6, 'arg': '6'}, {'max': 9, 'arg': '9'}, {'max': 0, 'arg': '1'}, {'max': 2, 'arg': '2'}, {'max': 3, 'arg': '3'}, {'max': 4, 'arg': '4'}, {'max': 5, 'arg': '5'}, {'max': 6, 'arg': '6'}, {'max': 7, 'arg': '7'}, {'max': 9, 'arg': '9'}]
    # [{'max': 0, 'arg': '1'}, {'max': 2, 'arg': '2'}, {'max': 3, 'arg': '3'}, {'max': 4, 'arg': '4'}, {'max': 5, 'arg': '5'}, {'max': 6, 'arg': '6'}, {'max': 7, 'arg': '7'}, {'max': 9, 'arg': '9'}]
    # 0 None
    # 1 {'max': 0, 'arg': '1'}
    # 2 {'max': 2, 'arg': '2'}
    # 3 {'max': 3, 'arg': '3'}
    # 4 {'max': 4, 'arg': '4'}
    # 5 {'max': 5, 'arg': '5'}
    # 6 {'max': 6, 'arg': '6'}
    # 7 {'max': 7, 'arg': '7'}
    # 8 {'max': 9, 'arg': '9'}
    # 0 None
    # 1 {'max': 1, 'arg': '1'}
    # 2 {'max': 2, 'arg': '2'}
    # 3 {'max': 3, 'arg': '3'}
    # 4 {'max': 4, 'arg': '4'}
    pass

    f = FlatFATs(8)
    print(f.getSize())
    f.new([Event(0, "1", 1), Event(0, "2", 2), Event(0, "3", 3), Event(0, "4", 4), Event(0, "5", 5), Event(0, "6", 6), Event(0, "7", 7), Event(0, "8", 8)])
    print(f.locations)
    f.update([Event(0, "1", 0)], "trigger")
    print(f.locations)
    f.update([Event(0, "8", 8)], "evict")
    print(f.locations)
    f.update([Event(0, "9", 9)], "insert")
    print(f.locations)
    print(f.getLocations())
    for i in range(9):
        print(i, f.prefix(i))

    f = FlatFATs(4)
    f.new([Event(0, "4", 4), Event(0, "3", 3), Event(0, "2", 2), Event(0, "1", 1)])
    for i in range(5):
        print(i, f.suffix(i))
