
class ForeignKey(object):
    def __init__(self, attributes, reference):
        self.Attributes = attributes
        self.Reference = reference

    # update reference from parent to decomposed child
    def update_reference(self):
        for relation in self.Reference.decomposed_relations:
            if len(relation.decomposed_relations) > 0:
                self.update_reference()
            else:
                for key in relation.Keys:
                    if self.Attributes == key.Attributes:
                        self.Reference = relation
