import pdb
from datetime import date
import re
from collections import OrderedDict

class cliManager():
    #Tipos de datos permitidos en el programa
    isAllowedDataType = ['INT', 'FLOAT', 'DATE', 'CHAR']
    isSavedData = []
    cacheLogData = []
    structureSaved = []
    multilines = False
    reductor = ""

    def __init__(self):
        pass

    def validateCreateTableTypes(self, input):
        if input not in self.isAllowedDataType:
            raise ValueError("ERROR" + input + " NO ES UN TIPO DE DATO VÁLIDO")
        else:
            return input

    def queryWhereStringCLBuilder(self, index, reducer, condition):

        index = str(index)
        if condition == '<':
            return str("item[" + index + "] < " + reducer)
        if condition == '<=':
            return str("item[" + index + "] <= " + reducer)
        if condition == '>':
            return str("item[" + index + "] > " + reducer)
        if condition == '>=':
            return str("item[" + index + "] >= " + reducer)
        if condition == '<>':
            return str("item[" + index + "] != " + reducer)
        if condition == '=':
            return str("item[" + index + "] == " + reducer)

    def queryWhereAgregatorBuilder(self, array, operator, comparator):
        if operator == 'AND':
            return (tup for tup in array if operator)

    def matchData(self, type, value):
        if type == "INT":
            try:
                return int(value)
            except Exception:
                print("ERROR" + value + " NO ES UN TIPO DE DATO INTEGER")
        if type == "FLOAT":
            try:
                return float(value)
            except Exception:
                print("ERROR" + value + " NO ES UN TIPO DE DATO FLOAT")
        if type == "CHAR":
            try:
                return str(value)
            except Exception:
                print("ERROR" + value + " NO ES UN TIPO DE DATO CHAR")
        if type == "VARCHAR":
            try:
                return str(value)
            except Exception:
                print("ERROR" + value + " NO ES UN TIPO DE DATO VARCHAR")
         if type == "DATE":
            try:
                return str(value)
            except Exception:
                print("ERROR" + value + " NO ES UN TIPO DE DATO DATE")
        
    def generateSpecificColOrder(self, cols, structure):
        return [any(e[0] == col for e in structure) for col in cols]

    def raiseError(self, condition, message):
        if condition:
            pass
        else:
            raise ValueError(message)

    def setSavedData(self, data):
        self.isSavedData = data

    def setSavedStructure(self, structure):
        self.structureSaved = structure

    def setCachedData(self, data):
        self.cacheLogData = data

    def addToCache(self, data):
        self.cacheLogData.append(data)

    def handleNullValue(self, data, bc):
        returnData = []
        for item in data:
            try:
                if eval(bc):
                    returnData.append(item)
            except TypeError:
                pass
        return returnData

    def handleAndStmt(self,listas):
        return [element for element in listas[0] if element in listas[1]]

    def handleOrStmt(self,listas):
        return listas[1] + [x for x in listas[0] if x not in listas[1]]