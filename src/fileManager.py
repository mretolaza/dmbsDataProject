# Se llama a archivo que crea los files de la base de
# datos, este es una carpeta existente dentro de la carpeta file
# https://docs.python.org/3.3/library/collections.html
# Se importa JSON LIB
import json

from createFile import createFile


class fileManager():
    currentDatabase = None
    dbSchemaTerm = '.schem'
    dbInfoTerm = '.dat'
    createFile = None

    def __init__(self):
        self.createFile = createFile()

    def createDatabaseFS(self, database):
        self.createFile.create_folder(database)

    def showDatabasesFS(self):
        return self.createFile.list_files()

    def showTablesFS(self):
        if self.currentDatabase is not None:
            return self.createFile.list_files(self.currentDatabase)
        else:
            raise TypeError("ERROR, NO HA SELECCIONADO NINGUNA BASE DE DATOS PARA TRABAJAR")

    def removeDatabaseFS(self, database):
        self.createFile.remove_folder(database)

    def createTableFS(self, table_name, table_structure):
        if (self.currentDatabase):
            self.createFile.create_folder(
                self.currentDatabase + "/" + table_name)  # Crea carpeta a la cual pertenece la tabla
            self.createFile.createWrite_file(
                self.currentDatabase + "/" + table_name + "/" + table_name + self.dbSchemaTerm,
                json.dumps(table_structure))  # Crea la "shema" con la base y estrucurta de la tabla

            self.createFile.createWrite_file(
                self.currentDatabase + "/" + table_name + "/" + table_name + self.dbInfoTerm,
                "[]")  # Despliega un array vacio para tablas
            return True
        else:
            raise ValueError('ERROR, NO HA SELECCIONADO NINGUNA BASE DE DATOS')

    def useDatabaseFS(self, database):
        if database not in self.showDatabasesFS():
            raise ValueError("ERROR" + database + " LA BASE DE DATOS NO EXISTE")
        self.currentDatabase = database

    def getDatabaseFS(self):
        return self.currentDatabase

    # Se crea estrucutura JSON con la cual se guardarán los datos en la db
    def insertTableFS(self, table, data):
        self.createFile.createWrite_file(self.currentDatabase + "/" + table + "/" + table + self.dbInfoTerm, data)

    # Se aplican  los mismos parámetros para la lectura de la db
    def readTableFS(self, table, fileType):
        return self.createFile.read_file(self.currentDatabase + "/" + table + "/" + table + (
            self.dbInfoTerm if fileType == "data" else self.dbSchemaTerm))

    # Se aplican los mismos parámetros para "re-nombramiento"
    def renameFS(self, table_name_old, table_name_new):
        return self.createFile.rename_files(self.currentDatabase + "/",
                                            self.currentDatabase + "/" + table_name_old + "/", table_name_old,
                                            table_name_new)
