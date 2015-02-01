import xmlReader
import Key
import itertools
from FunctionalDependency import FunctionalDependency
from Key import Key
from Attribute import Attribute
from ForeignKey import ForeignKey
import copy

class Relation(object):

    def __init__(self,name=''):
        self.Name = name
        self.FDs = []
        self.Attributes = []
        self.Keys=[]
        self.NormalForm = '1NF'   # default normal form is 1NF
        self.FdsViolateNF = []    # list of FDs that violate the next normal form
        self.FdsToDrop = []
        self.canonical_cover = []
        self.foreign_keys = []
        self.decomposed_relations = []  # new decomposed (children) relations
        # hard-coded keys (to be implemented later)

    def __repr__(self):
        return self.Name

    # default comparison function
    def __eq__(self, other):
        if set(self.Name) == set(other.Name):
            return True
        else:
            return False

    # sequentially compute the normal form of the relation
    def computeNormalForm(self):
        if len(self.Keys) == 0:
            self.compute_candidate_keys()

        if len(self.canonical_cover) == 0:
            self.compute_canonical_cover()

        if self.is2NF():
            if self.is3NF():
                self.isBCNF()

    # test if relation in Second normal form (2NF)
    def is2NF(self):
        if self.checkFullFDs():
            self.NormalForm = '2NF'
            return True
        else:
            return False

    # test if relation in third normal form (3NF)
    def is3NF(self):
        if not(self.checkTransitiveFDs()):
            self.NormalForm = '3NF'
            return True
        else:
            return False

    # test if relation in Boyce-Codd normal form (BCNF)
    def isBCNF(self):
        test=[]
        if self.checkNonTrivialFDs():
            self.NormalForm = 'BCNF'
            return True
        else:
            return False

    # full FD from keys to non-prime attributes
    def checkFullFDs(self):
        nonPrimeAttributes = self.getNonPrimeAttributes()
        #fdList = self.fromKeysToNonPrimeAttributes(nonPrimeAttributes)
        self.FdsViolateNF = self.getFDsViolate2NF(nonPrimeAttributes)

        if len(self.FdsViolateNF)>0:
             return False
        else:
             return True


    # non-transitive FD from keys to non-prime attributes
    def checkTransitiveFDs(self):
        nonPrimeAttributes = self.getNonPrimeAttributes()
        for fd in self.canonical_cover:
             if set(fd.leftHandSide).issubset(set(nonPrimeAttributes)) and fd.isNonPrimeAttribute(nonPrimeAttributes):
                 self.FdsViolateNF.append(fd)

        if len(self.FdsViolateNF)>0:
            return True
        else:
            return False

    # check that every non-trivial FD is on a superkey
    def checkNonTrivialFDs(self):
        nonTrivialFdList = []
        nonSuperKeyList = []

        # get all non-trivial FDs
        for fd in self.canonical_cover:
            if fd.isNonTrivial():
                nonTrivialFdList.append(fd)

        # check non-trivial FDs is on a superkey
        for fd in nonTrivialFdList:
            if not(fd.isSuperKey(self.Keys)):
                nonSuperKeyList.append(fd)

        if len(nonSuperKeyList) > 0:
            self.FdsViolateNF = nonSuperKeyList
            return False
        else:
            return True

     # get non-prime attributes by computing difference between relation's attributes and primeAttribute sets
    def getNonPrimeAttributes(self):
         primeAttributes = self.getPrimeAttributes()
         nonPrimeAttributes=list(set(self.Attributes)-set(primeAttributes))

         #print (nonPrimeAttributes)
         return nonPrimeAttributes

     # get the 'unique' prime attributes from the relation's keys
    def getPrimeAttributes(self):
         primeAttributes=[]

         for key in self.Keys:
             for attribute in key.Attributes:
                 if attribute not in primeAttributes:
                     primeAttributes.append(attribute)

         #print (primeAttributes)
         return primeAttributes

    # (THIS FUNCTION NOT USED NOW) get all FDs where Keys in the lhs and NonPrimeAttributes in rhs
    def fromKeysToNonPrimeAttributes(self, nonPrimeAttributes):
        fdList=[]

        for key in self.Keys:
            for nonPrimeAttribue in nonPrimeAttributes:
                fdObj = FunctionalDependency()
                fdObj.leftHandSide = key.Attributes
                fdObj.rightHandSide = nonPrimeAttribue
                fdList.append(fdObj)

        #print(fdList)
        return fdList

    # get a list of all (decomposed) FDs that violate 2NF
    def getFDsViolate2NF(self, nonPrimeAttributes):
        fdsViolate2NF = []

        for fd in self.canonical_cover:
            # 1. check if the fd's rhs is nonPrimeAttribute
            if fd.isNonPrimeAttribute(nonPrimeAttributes):
                isFull = True
                for key in self.Keys:
                    # 2. check if a key is not minimal compared to the lhs of fd (lhs -> nonPrimeAttribute)
                    if not(key.isMinimal(fd.leftHandSide)):
                        isFull = False
                        break

                if not(isFull):
                    fdsViolate2NF.append(fd)

        return fdsViolate2NF

    # print the current normal form
    def print_normal_form(self):

        print(self.Name + ' is in '+self.NormalForm)

        if len(self.FdsViolateNF) > 0:
            next_normal_form = self.get_next_norml_form()
            print("FDs violate "+next_normal_form+":")
            print(self.FdsViolateNF)

    #  get next normal form of the current norml form
    def get_next_norml_form(self):
        NormalForms = ['1NF', '2NF', '3NF', 'BCNF']
        currentNFindex = NormalForms.index(self.NormalForm)
        return NormalForms[currentNFindex+1]

    def compute_attribute_closure(self, f, attribute):
        # step 1: closure is equal to the attribute
        closure = attribute[:]

        # step 2: iterate through all FDs to compare lhs with the closure
        for fd in f:
            if set(fd.leftHandSide).issubset(set(closure)):
                for att in fd.rightHandSide:
                    # only add rhs attribute which is not exist before in closure
                    if att not in closure:
                        closure.append(att)
                        # recursively re-compute closure after adding new attribute
                        closure = self.compute_attribute_closure(f, closure)

        return closure

    # Compute canonical cover (F_min)
    def compute_canonical_cover(self):
        new_f = []

        # step 1: Decompose any FD from F up to rhs as singleton
        for fd in self.FDs:
            for decomposed_fd in fd.decompose():
                # step 2: Check for attribute redundancy in lhs of any FD
                is_redundant = False
                for lhs in decomposed_fd.leftHandSide:
                    if decomposed_fd.rightHandSide[0] in self.compute_attribute_closure(self.FDs, [lhs]):
                        fd_obj = FunctionalDependency()
                        fd_obj.leftHandSide = [lhs]
                        fd_obj.rightHandSide = [decomposed_fd.rightHandSide[0]]
                        new_f.append(fd_obj)
                        is_redundant = True
                        break
                if not is_redundant:
                    new_f.append(decomposed_fd)

        self.canonical_cover = new_f[:]
        # Step 3: Check for redundancy of any FD
        for fd in new_f:
            # Is X −> A redundant ? Check for A in X+ of g , where g = newF − {X −> A}
            g = self.canonical_cover[:]
            g.remove(fd)
            lhs_closure_of_g = self.compute_attribute_closure(g, fd.leftHandSide)
            if fd.rightHandSide[0] in lhs_closure_of_g:
                self.canonical_cover.remove(fd)

    # decompose relation to achieve higher normal form
    def decompose(self):
        if len(self.FdsViolateNF) > 0:
            nasty_fd = self.FdsViolateNF[0]

            lhs_closure = self.compute_attribute_closure(self.FDs, nasty_fd.leftHandSide)
            r1 = Relation()
            r1.Name = self.Name + "1"
            r1.Attributes = lhs_closure
            r1.compute_fds_from_original(self.canonical_cover)
            key = Key()
            key.Attributes = nasty_fd.leftHandSide
            r1.Keys.append(key)
            #r1.compute_candidate_keys()
            r1.computeNormalForm()
            r1.inherit_parent_foreign_keys(self.foreign_keys)
            self.decomposed_relations.append(r1)

            #if not (r1.NormalForm == '3NF' or r1.NormalForm == 'BCNF'):
            if r1.NormalForm != 'BCNF':
                r1.decompose()

            r2 = Relation()
            r2.Name = self.Name + "2"
            r2.Attributes = list(set(self.Attributes).difference(set(lhs_closure).difference(set(nasty_fd.leftHandSide))))
            r2.compute_fds_from_original(self.canonical_cover)
            r2.compute_candidate_keys()
            r2.computeNormalForm()
            r2.inherit_parent_foreign_keys(self.foreign_keys)
            r2.foreign_keys.append(ForeignKey(nasty_fd.leftHandSide, r1))

            self.decomposed_relations.append(r2)

            if r2.NormalForm != 'BCNF':
                r2.decompose()

            # here: ZT relation to preserve Z −> T
            remaining_fds = list((set(self.canonical_cover)-set(r1.FDs))-set(r2.FDs))
            if len(remaining_fds) > 0:
                index = 3
                for fd in remaining_fds:
                    if set(fd.leftHandSide + fd.rightHandSide) == set(self.Attributes):
                        self.FdsToDrop.append(fd)
                    else:
                        r = Relation()
                        r.Name = self.Name + str(index)
                        r.Attributes = fd.leftHandSide + fd.rightHandSide
                        r.FDs.append(fd)
                        r.compute_candidate_keys()
                        r.computeNormalForm()
                        self.decomposed_relations.append(r)

                        r.inherit_parent_foreign_keys(self.foreign_keys)

                        # Foreign Key computation:
                        for key in r1.Keys:
                            if key.Attributes == r.Attributes:
                                r.foreign_keys.append(ForeignKey(key.Attributes, r1))

                        for key in r2.Keys:
                            if key.Attributes == r.Attributes:
                                r.foreign_keys.append(ForeignKey(key.Attributes, r2))

                        if r.NormalForm != 'BCNF':
                            r.decompose()

                        index += 1

    def compute_fds_from_original(self, originalFDs):
        for fd in originalFDs:
            if set(fd.leftHandSide).issubset(self.Attributes) and set(fd.rightHandSide).issubset(self.Attributes):
                 self.FDs.append(fd)

    def compute_candidate_keys(self):
        temp_keys = []
        left = []           # contains attributes appear 'only' on the left hand sides of FDs
                            # 'left' attributes must be part of every key
        middle = []         # contains attributes appear on both left and right hand sides of FDs
                            # 'middle' attributes may or may not part of a key
        right = []          # contains attributes appear 'only' on the right hand sides of FDs
                            # 'right' attributes are not part of any key

        for fd in self.FDs:
            left += fd.leftHandSide
            right += fd.rightHandSide

        middle = list(set(left).intersection(set(right)))
        left = list(set(left)-set(middle))
        right = list(set(right)-set(middle))

        if len(left) > 0:
            # check keys in left list
            self.check_attribute_list(left, temp_keys)

            # if keys still not found, check keys in left list with middle list combinations
            if len(temp_keys) == 0:
                r1 = 1
                while r1 != (len(left)+1):
                    for left_combination in itertools.combinations(left, r1):
                        r2 = 1
                        while r2 != (len(middle)+1):
                            for middle_combination in itertools.combinations(middle, r2):
                                self.check_key(list(left_combination) + list(middle_combination), temp_keys)
                            #if len(temp_keys) > 0:
                            #    break
                            r2 += 1
                    #if len(temp_keys) > 0:
                    #        break
                    r1 += 1
        else:
            # check keys in middle list
            self.check_attribute_list(middle, temp_keys)

        if len(temp_keys) == 0:
            key = Key()
            # Basic Key U->U:
            key.Attributes = self.Attributes
            temp_keys.append(key)

        self.Keys = temp_keys[:]


    # check keys in attribute list (e.g., Left or Middle lists)
    def check_attribute_list(self, attribute_list, temp_keys):
        r = 1
        while r != (len(attribute_list)+1):
            for combination in itertools.combinations(attribute_list, r):
                self.check_key(list(combination), temp_keys)
            # as we are searching minimal set of attributes, we have to stop after a success combination of r
            #if len(self.Keys) > 0:
            #        break
            r += 1

    def check_key(self, attribute, temp_keys):
        is_super_key = False
        for key in temp_keys:
            if set(set(key.Attributes)).issubset(attribute):
                is_super_key = True
                break

        if not is_super_key:
            if set(self.compute_attribute_closure(self.FDs, attribute)) == set(self.Attributes):
                key = Key()
                key.Attributes = attribute[:]
                temp_keys.append(key)

    #inherit the foreign keys of the parent relation
    def inherit_parent_foreign_keys (self, parent_foreign_keys):
        for parent_fk in parent_foreign_keys:
            if set(parent_fk.Attributes).issubset(self.Attributes):
                # check if the reference is decomposed in order to refer to its decomposed children
                if len(parent_fk.Reference.decomposed_relations) > 0:
                    new_fk = copy.copy(parent_fk)
                    new_fk.update_reference()
                    self.foreign_keys.append(new_fk)
                else:
                    self.foreign_keys.append(parent_fk)

    def print_proposal(self):
        for decomposed_relation in self.decomposed_relations:
            print(decomposed_relation.Name)
            print(decomposed_relation.Attributes)
            print(decomposed_relation.FDs)
            for key in decomposed_relation.Keys:
                print(key.Attributes)
            decomposed_relation.print_normal_form()
            if len(decomposed_relation.foreign_keys) > 0:
                print("foreign key:")
                for fk in decomposed_relation.foreign_keys:
                    print(fk.Attributes)
                    print(fk.Reference)
            if len(decomposed_relation.FdsToDrop) > 0:
                print ("In order to achieve higher NF in "+decomposed_relation.Name+", It is required to drop the following FDs:")
                print(decomposed_relation.FdsToDrop)
                print("\n")
            print()

            decomposed_relation.print_proposal()

    def print_report(self, TAB = ''):
        str_report = ''
        NEW_LINE = '\n'

        str_report += TAB + self.Name + NEW_LINE
        str_report += TAB + "Attributes:" +str(self.Attributes) + NEW_LINE
        str_report += TAB + "FDs:" + str(self.FDs) + NEW_LINE

        str_report += TAB + "Keys("+str(len(self.Keys))+"): "
        if self.Keys:
            for key in self.Keys:
                str_report += str(key.Attributes) +  ", "
            str_report = str_report[:-2] + NEW_LINE
        else:
            str_report += "-"  + NEW_LINE

        if self.foreign_keys:
            str_report += TAB + "Foreign keys("+str(len(self.foreign_keys)) +"):"
            for fk in self.foreign_keys:
                str_report += str(fk.Attributes) + "(" + fk.Reference.Name + "), "
            str_report = str_report[:-2] + NEW_LINE

        str_report += TAB + "Normal Form: " + self.NormalForm + NEW_LINE
        if len(self.FdsViolateNF) > 0:
            next_normal_form = self.get_next_norml_form()
            str_report += TAB + "FDs violate "+next_normal_form+": "+str(self.FdsViolateNF)
        str_report += NEW_LINE

        if len(self.decomposed_relations) > 0:
            str_report += TAB + "Decomposed relations based on " + str(self.FdsViolateNF[0]) + ":" + NEW_LINE

            if len(self.FdsToDrop) > 0:
                str_report += TAB + "(It is required to drop the following FDs: " + str(self.FdsToDrop)  + ")" + NEW_LINE

            str_report += NEW_LINE
            for decomposed_relation in self.decomposed_relations:
                str_report += decomposed_relation.print_report(TAB + '\t')

        return str_report

    def buildCreateTableClause(self):
        fk_holder=''
        pk_holder=''
        clause="CREATE TABLE "+self.Name+"("
        for field in self.Attributes:
            if field.Autoincrement==True:
                clause += " "+field.Name+" SERIAL "
            else:
                clause += " "+field.Name+" "+str(field.Type)

            if field.Nullable==False:
                clause +=" NOT NULL \n,"
            else:
                clause += " \n,"
        clause = clause[:-3]
        if len(self.Keys) > 0:
            clause=clause+"\n, PRIMARY KEY("
            for att in self.Keys[0].Attributes:
                clause += att.Name + ", "
            clause = clause[:-2] + ")"
        if len(self.foreign_keys) > 0:
            for fk in self.foreign_keys:
                clause  += "\n, FOREIGN KEY("
                for att in fk.Attributes:
                    clause += att.Name + ", "
                clause = clause[:-2] + ")"
                clause += " REFERENCES "+fk.Reference.Name+"("
                if len(fk.Reference.Keys) > 0:
                    for att in fk.Reference.Keys[0].Attributes:
                        clause += att.Name + ", "
                    clause = clause[:-2] + ")"
        clause=clause.rstrip(',')
        clause=clause+");\n"
        return clause

    def buildCreateTableScript(self):
        script = ''
        if len(self.decomposed_relations) > 0:
            for relation in self.decomposed_relations:
                script += relation.buildCreateTableScript()
        else:
            script = self.buildCreateTableClause() + "\n"
        return script

    def buildDmlClause(self, parent):
        clause = 'INSERT INTO ' + self.Name + ' ('
        for att in self.Attributes:
            clause += att.Name + ', '
        clause = clause[:-2] + ')\n'
        clause += 'SELECT '
        for att in self.Attributes:
            clause += '"' + att.Name + '", '
        clause = clause[:-2] + ' FROM "' + parent.Name + '";\n'
        return clause

    def buildDmlScript(self, parent = None):
        script = ''
        if len(self.decomposed_relations) > 0:
            if not parent:
                parent = self
            for relation in self.decomposed_relations:
                script += relation.buildDmlScript(parent)
        else:
            # parent is not the same as the default value
            if parent:
                script = self.buildDmlClause(parent) + "\n"
        return script

    def buildDropTableClause(self):
        clause="DROP TABLE "+self.Name
        return clause