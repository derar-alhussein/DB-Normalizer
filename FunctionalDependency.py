class FunctionalDependency(object):

    def __init__(self):
        self.leftHandSide = []
        self.rightHandSide = []

    # default printing function as LHS -> RHS
    def __repr__(self):
        return self.lhs_pretty_print() + "->" + self.rhs_pretty_print()

    def lhs_pretty_print(self):
        lhs = ''
        for att in self.leftHandSide:
            lhs += att.Name + '.'
        return lhs[:-1]

    def rhs_pretty_print(self):
        rhs = ''
        for att in self.rightHandSide:
            rhs += att.Name + '.'
        return rhs[:-1]

    #def __str__(self):
    #    return self.lhs_pretty_print() + "->" + self.rhs_pretty_print()

    # default comparison function between this fd and other one
    def __eq__(self, other):
        if set(self.leftHandSide) == set(other.leftHandSide) and set(self.rightHandSide) == set(other.rightHandSide):
            return True
        else:
            return False

    def __hash__(self):
        return hash((frozenset(self.leftHandSide),frozenset(self.rightHandSide)))

    # Decompose Functional Dependency X->YZ will be two: X->Y and X->Z
    def decompose(self):
        FdList = []
        for rhs in self.rightHandSide:
            fdObj=FunctionalDependency()
            fdObj.leftHandSide=self.leftHandSide
            fdObj.rightHandSide.append(rhs)
            FdList.append(fdObj)
        return FdList

    # check if the rhs is nonPrimeAttribute
    def isNonPrimeAttribute(self,nonPrimeAttributes):
        if  self.rightHandSide[0] in nonPrimeAttributes:
            return True
        else:
            return False

    def isNonTrivial(self):
        if set(self.rightHandSide) != set(self.leftHandSide):
            return True

    # check if the lhs is superkey
    def isSuperKey(self, Keys):
        for key in Keys:
            if set(key.Attributes).issubset(set(self.leftHandSide)):
                return True

        return False

    def is_valid(self, relationObject , schema):
        is_valid_fd = False
        # Trivial FD is always valid
        if self.leftHandSide == self.rightHandSide:
            is_valid_fd = True
        else:
            try:
                script = 'SELECT '
                lhs_attributes = ''
                for attribute in self.leftHandSide:
                    lhs_attributes += '"'+attribute.Name+'", '
                lhs_attributes = lhs_attributes[:-2]
                script += lhs_attributes +'\n'
                script += ' FROM( SELECT '
                sub_query_columns = lhs_attributes + ', '
                for attribute in self.rightHandSide:
                    if attribute not in self.leftHandSide:
                        sub_query_columns += '"'+attribute.Name+'", '
                sub_query_columns = sub_query_columns[:-2]
                script += sub_query_columns +'\n'
                script += ' FROM "'+ relationObject.Name+'"\n'
                script += ' group by ' + sub_query_columns  +'\n'
                script +=') temp \n'
                script += ' group by ' + lhs_attributes +'\n'
                script += 'HAVING count(*) > 1 \n'

                result = schema.execute_select_query(script)
                if  result.rowcount == 0: # empty result means valid FDs
                    is_valid_fd = True
            except:
                raise

        return is_valid_fd





