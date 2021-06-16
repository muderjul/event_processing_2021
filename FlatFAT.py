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
        pass

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
        if self.leftChild != None:
            size += self.leftChild.getSize()
        if self.rightChild != None:
            size += self.rightChild.getSize()
        return size

    def __repr__(self):
        return "FlatFAT()"

    def __str__(self):
        return "FlatFAT(tuple:%s, \nleft:%s, \nright:%s)" % (self.tuple, self.leftChild, self.rightChild)
