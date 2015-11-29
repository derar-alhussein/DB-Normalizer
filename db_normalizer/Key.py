
class Key(object):

    def __init__(self):
        self.Attributes=[]

    # check if the key is minimal
    def isMinimal(self, fdLHS):
        # Key is Not minimal if it 'strictly' contains the lhs of fd
        if fdLHS != self.Attributes and set(fdLHS).issubset(self.Attributes):
            return False
        else:
            return True