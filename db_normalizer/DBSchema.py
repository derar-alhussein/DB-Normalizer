from sqlalchemy import  *
import sqlalchemy
from sqlalchemy.engine import reflection
from Relation import Relation
from Attribute import Attribute
from Key import Key

class Dbschema(object):

    def __init__(self,username, password, host, port ,db_name):
        if password:
            self.engine=create_engine('postgresql://'+username+':'+password+'@'+host+':'+port+'/'+db_name)
        else:
            self.engine=create_engine('postgresql://'+username+'@'+host+':'+port+'/'+db_name)
        self.metadata=MetaData()
        self.con=self.engine.connect()
        self.insp = reflection.Inspector.from_engine(self.engine)
        self.tableNames=self.insp.get_table_names()
        #self.tableColumns=[]
        #self.tableSchema=[]

    def getSchema(self):
        tableColumns=[]
        for table in self.tableNames:
            print("Table name :"+table)

            for columns in self.insp.get_columns(table):
                tableColumns.append(columns['name'])
            print(tableColumns)
            print("Primary Key :"+str(self.getPrimaryKey(table)))
            print("Foreign Key :"+str(self.getForeignKey(table)))
            tableColumns=[]


    def getPrimaryKey(self,table):
        primList=[]
        primList=self.insp.get_primary_keys(table)
        return primList

    def getForeignKey(self,table):
        FKList=[]
        flist=[]
        flist=self.insp.get_foreign_keys(table)
        FKList=flist
        return FKList

    #other lists like constraints list can be found too
    def dbProcessSchemes(self):
        relationList = []
        for table in self.tableNames:
            relObj=Relation()
            relObj.Name = table
            for columns in self.insp.get_columns(table):
                attribute_object = Attribute(columns['name'])
                attribute_object.Type = columns['type']
                attribute_object.Autoincrement = columns['autoincrement']
                attribute_object.Nullable = columns['nullable']
                relObj.Attributes.append(attribute_object)

            #attribute_object = Attribute()
            #attribute_object.Name = columns['name']

            key = Key()
            for att in self.insp.get_primary_keys(table):
                attribute_object = Attribute(att)
                key.Attributes.append(attribute_object)
            relObj.Keys.append(key)

            #relObj.FDs = self.getFunctionalDependencies(relation)
            relationList.append(relObj)
        return relationList

    def execute_script(self, script):
        trans = self.con.begin()
        try:
            self.con.execute(script)
            trans.commit()
        except:
            trans.rollback()
            raise

    def execute_select_query(self, script):
        try:
            result = self.con.execute(script)
            return result
        except:
            raise

