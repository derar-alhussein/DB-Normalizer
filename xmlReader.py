import xml.etree.cElementTree as eTree
import FunctionalDependency
import Relation
from Attribute import Attribute
import xml.etree.cElementTree as Etree
import xml.dom.minidom
from Key import Key

class XmlReader(object):

    #Constructor takes in document and assigns xml root element to root
    def __init__(self,xmldocument):
        self.xml=eTree.parse(xmldocument)
        self.root=self.xml.getroot()

    # read xml node that relation name
    def getRelationName(self, relation):
            for name in relation:
                return name.text

# read xml nodes that represents relation's columns (attributes)
    def getColumns(self, relation):
        column_names=[]
        for attributes in relation.iter('attributes'):
            for columns in attributes:
                column_names.append(columns.text)
        return column_names

    # read xml nodes that represents Dependencies (Functional Dependencies)
    def getFunctionalDependencies(self, relation):
        FDs=[]
        for dependencies in relation.iter('dependencies'):
            for fd in dependencies:
                fdObj=FunctionalDependency.FunctionalDependency()

                for lhs in fd.iter('lhs'):
                    for attribute in lhs:
                        attribute_object = Attribute(attribute.text)
                        fdObj.leftHandSide.append(attribute_object)

                for rhs in fd.iter('rhs'):
                    for attribute in rhs:
                        attribute_object = Attribute(attribute.text)
                        fdObj.rightHandSide.append(attribute_object)

                FDs.append(fdObj)
        return FDs

    def getKyes(self, relation):
        Keys=[]
        for keys in relation.iter('keys'):
            for key in keys:
                key_obj=Key()

                for attribute in key.iter('attribute'):
                    attribute_object = Attribute(attribute.text)
                    key_obj.Attributes.append(attribute_object)
                Keys.append(key_obj)
        return Keys

    # fill and return a Relation object
    def xmlProcessSchemes(self):
        relationList = []
        for relation in self.root:
            relObj=Relation.Relation()
            relObj.Name = self.getRelationName(relation)

            for columns in self.getColumns(relation):
                attribute_object = Attribute(columns)
                relObj.Attributes.append(attribute_object)

            relObj.Keys = self.getKyes(relation)
            relObj.FDs = self.getFunctionalDependencies(relation)

            #attribute_object = Attribute()
            #attribute_object.Name = columns['name']

            relationList.append(relObj)
        return relationList

    def xmlCompleteStructure(self,relObj, file):

        root=Etree.Element("schema")
        for table in relObj:
            relation=Etree.SubElement(root,"relation")

            name=Etree.SubElement(relation,"name").text=table.Name
            attributes=Etree.SubElement(relation,"attributes")
            for i in table.Attributes:
                column=Etree.SubElement(attributes,"column").text=str(i)
            dependencies=Etree.SubElement(relation,"dependencies")

            for d in table.FDs:
                fds=Etree.SubElement(dependencies,"fd")
                lhs=Etree.SubElement(fds,"lhs")
                for att in d.leftHandSide:
                    Etree.SubElement(lhs,"attribute").text=str(att)

                rhs=Etree.SubElement(fds,"rhs")
                for att in d.rightHandSide:
                    Etree.SubElement(rhs,"attribute").text=str(att)


            nf=Etree.SubElement(relation,"normalFormlevel").text=table.NormalForm

            voilatedFD=Etree.SubElement(relation,"FdsViolateNF")
            for j in table.FdsViolateNF:
                vfds=Etree.SubElement(voilatedFD,"VoilatedFd")
                lhs=Etree.SubElement(vfds,"lhs")
                for att in d.leftHandSide:
                    Etree.SubElement(lhs,"attribute").text=str(att)

                rhs=Etree.SubElement(vfds,"rhs")
                for att in d.rightHandSide:
                    Etree.SubElement(rhs,"attribute").text=str(att)

            keys=Etree.SubElement(relation,"keys")
            for key in table.Keys:
                k=Etree.SubElement(keys,"key")
                for att in key.Attributes:
                    Etree.SubElement(k,"attribute").text=str(att)
        self.indent(root)
        tree=Etree.ElementTree(root)
        tree.write(file, xml_declaration=True, encoding='utf-8', method="xml")

    def indent(self, elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i



















