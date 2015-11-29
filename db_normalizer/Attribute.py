class Attribute(object):

    def __init__(self, Name):
        self.Name = Name
        self.Type = ''
        self.Length = ''
        self.Autoincrement = False
        self.Nullable = True
        #self.Closure = []

    # default printing function
    def __repr__(self):
        return self.Name

    def __eq__(self, other):
        if self.Name == other.Name:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.Name)

    #def __str__(self):
    #    return self.Name

    #def computeClosure(self, FDs):
