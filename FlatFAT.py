from helper_functions import lift, combine, lower
from math import log, ceil

class FlatFAT(object):

    def __init__(self, tuple=None, leftChild=None, rightChild=None):
        self.tuple = tuple
        self.leftChild = leftChild
        self.rightChild = rightChild

    def new(self, locations):
        if len(locations) == 1:
            self.tuple = lift(locations[0])
        elif len(locations) > 1:
            depth = ceil(log(len(locations), 2))
            self.leftChild = FlatFAT()
            self.leftChild.new(locations[:2**(depth-1)])
            self.rightChild = FlatFAT()
            self.rightChild.new(locations[2**(depth-1):])
            self.tuple = combine(leftChild.getTuple(), rightChild.getTuple())
        else:
            return

    def update(self, locations):
        for location in locations:
            if location["type"] == "insert":
                if self.leftChild != None:
                    if self.rightChild != None: # both set
                        lcSize = self.leftChild.getSize()
                        rcSize = self.rightChild.getSize()
                        if log(lcSize, 2) != ceil(log(lcSize, 2)): # left space
                            self.leftChild.update([location])
                        elif log(rcSize, 2) != ceil(log(rcSize, 2)): # right space
                            self.rightChild.update([location])
                        elif rcSize < lcSize: # both need a new depth layer, but right is smaller than left
                            self.rightChild.update([location])
                        else: # both need a new depth layer but left is LEQ than right
                            self.leftChild.update([location])
                        self.tuple = combine(self.leftChild.getTuple(), self.rightChild.getTuple())
                    else: # left set only
                        self.rightChild = FlatFAT()
                        location.pop("type")
                        self.rightChild.new([location])
                        self.tuple = combine(self.tuple, location)
                else: # left not set
                    if self.rightChild != None: # right set only
                        self.leftChild = FlatFAT()
                        location.pop("type")
                        self.leftChild.new([location])
                        self.tuple = combine(self.tuple, location)
                    else: # both not set
                        self.leftChild = FlatFAT()
                        self.leftChild.new([self.tuple])
                        self.rightChild = FlatFAT
                        location.pop("type")
                        self.rightChild.new([location])
                        self.tuple = combine(self.tuple, location)

            elif location["type"] == "evict":
                if self.leftChild != None:
                    if self.rightChild != None: # both childs not empty
                        if self.leftChild.update([location]) == 0: # left child update returns non-empty tree
                            if self.rightChild.update([location]) == 0: # right child update returns non-empty tree
                                self.tuple = combine(self.leftChild.getTuple(), self.rightChild.getTuple())
                                return 0
                            else: # right child update returned empty tree
                                # todo compact left tree?
                                self.tuple = self.leftChild.getTuple()
                                self.rightChild = None
                                return 0
                        else: # left side update returned empty tree
                            self.leftChild = None
                            if self.rightChild.update([location]) == 0: # right child update returns non-empty tree
                                # todo compact right tree?
                                self.tuple = self.rightChild.getTuple()
                                return 0
                            else: # both tree sides empty, return compacting upwards
                                return -1
                    else: # right child empty, left child not empty
                        if self.leftChild.update([location]) == 0: # left child not empty after update
                            self.tuple = self.leftChild.getTuple()
                            return 0
                        else: # both children empty after update
                            return -1
                else:
                    if self.rightChild != None: # left child empty, right child not empty
                        if self.rightChild.update([location]) == 0: # right child not empty after update
                            self.tuple = self.rightChild.getTuple()
                            return 0
                        else: # both children empty after update
                            return -1
                    else: # we are root and only node
                        if self.tuple["arg"] == location["arg"]:
                            self.tuple = None
                            return -1
                        else:
                            return 0

            elif location["type"] == "trigger":
                if self.leftChild != None:
                    self.leftChild.update([location])
                    if self.rightChild != None: # left and right not empty
                        self.rightChild.update([location])
                        self.tuple = combine(self.leftChild.getTuple(), self.rightChild.getTuple())
                    else: # right side empty, one sided update
                        self.tuple = self.leftChild.getTuple()
                else:
                    if self.rightChild != None: # left empty and right not empty
                        self.rightChild.update([location])
                        self.tuple = self.rightChild.getTuple()
                    else: # we are leaf
                        if self.tuple["arg"] == location["arg"]: # check if we should update
                            self.tuple["max"] = location["max"]
                        else: # arg does not match, noop
                            continue
            else:
                pass # cannot happen

    def aggregate(self):
        return self.tuple

    def prefix(i):
        if self.leftChild != None:
            lcSize = self.leftChild.size()
            if lcSize == i:
                return self.leftChild.aggregate()
            elif lcSize < i:
                return self.leftChild.prefix(i)
            else:
                i -= lcSize
                if self.rightChild != None:
                    rcSize = self.rightChild.size()
                    if rcSize >= i:
                        return combine(self.leftChild.aggregate(), self.rightChild.aggregate())
                    else:
                        return combine(self.leftChild.aggregate(), self.rightChild.prefix(i))

    def suffix(i):
        if self.rightChild != None:
            rcSize = self.rightChild.size()
            if rcSize == i:
                return self.rightChild.aggregate()
            elif rcSize < i:
                return self.rightChild.suffix(i)
            else:
                i -= rcSize
                if self.leftChild != None:
                    lcSize = self.leftChild.size()
                    if lcSize >= i:
                        return combine(self.rightChild.aggregate(), self.leftChild.aggregate())
                    else:
                        return combine(self.rightChild.aggregate(), self.leftChild.suffix(i))

    def getSize(self):
        size = 0
        if self.leftChild == None and self.rightChild == None:
            return 1
        if self.leftChild != None:
            size += self.leftChild.getSize()
        if self.rightChild != None:
            size += self.rightChild.getSize()
        return size

    def __repr__(self):
        return "FlatFAT()"

    def __str__(self):
        return "FlatFAT(tuple:%s, \nleft:%s, \nright:%s)" % (self.tuple, self.leftChild, self.rightChild)
