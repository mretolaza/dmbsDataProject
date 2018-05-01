# https://docs.python.org/2/library/pdb.html
# Se agrega importación del SQL LISTENER para obtener
# Las funciones básicas de SQL
# Manegador de los datos que se van a ejectutar
from cliManager import cliManager
# Se agrega fileManager este es el archivo que se encargará del manejo de la db (Sus archivos)
from fileManager import fileManager
# Estructura de como se imprimen los archivos los datos a utilizar y visualizacion de los mismos
from printerClass import printerClass

from sqlListener import sqlListener

if __name__ is not None and "." in __name__:
    from .sqlParser import sqlParser
else:
    from sqlParser import sqlParser

# Se inicializan las clases a utilizar 
dbFile = fileManager()
dataCM = cliManager()
dbPrint = printerClass()


class tokenizationClass(sqlListener):
    def __init__(self):
        pass

    # Se ejecutan las clases de SQL LISTENER SQL PARSER
    def exitR(self, ctx):
        print("Bienvenido, el ingreso de cualquier valor SQL ha sido validado")

    def getTokenValue(self, name):
        return name.getText()

        # Los comentarios se colocan con el nombre
        # que deben de ser ejecutados

    # CREATE DATABASE
    def enterCreate_database_stmt(self, ctx: sqlParser.Create_database_stmtContext):
        database_name = self.getTokenValue(ctx.database_name())
        dbFile.createDatabaseFS(database_name)

    def exitCreate_database_stmt(self, ctx: sqlParser.Create_database_stmtContext):
        print("LA BASE DE DATOS SE HA CREADO SATISFACTORIAMENTE")
        pass

    # !CREATE DATABASE

    # SHOW DATABASE
    def enterShow_databases_stmt(self, ctx: sqlParser.Show_databases_stmtContext):
        print("BASES DE DATOS DEL SISTEMA:")
        print(dbFile.showDatabasesFS())
        pass

    # !SHOW DATABASE

    # USE DATABASE
    def enterUse_database_stmt(self, ctx: sqlParser.Use_database_stmtContext):
        datbase_name = self.getTokenValue(ctx.database_name())
        dbFile.useDatabaseFS(datbase_name)
        print("BASE DE DATOS ACTUAL CAMBIO A: " + datbase_name)

    # !USE DATABASE

    # DROP DATABASE
    def enterDrop_database_stmt(self, ctx: sqlParser.Drop_database_stmtContext):
        database_name = self.getTokenValue(ctx.database_name())
        dbFile.removeDatabaseFS(database_name)
        pass

    # !DROP DATABASE

    # CREATE TABLE
    def enterCreate_table_stmt(self, ctx: sqlParser.Create_table_stmtContext):
        table_name = self.getTokenValue(ctx.table_name())
        cols = []
        for column in ctx.column_def():
            type = dataCM.validateCreateTableTypes(self.getTokenValue(column.type_name().name()[0]))
            key = self.getTokenValue(column.column_name())
            cols.append((key, type))
        if dbFile.createTableFS(table_name, cols):
            print("SE HA CREADO LA TABLA " + table_name + " EXITOSAMENTE")
        pass

    # !CREATE TABLE

    # SHOW TABLES
    def enterShow_tables_stmt(self, ctx: sqlParser.Show_tables_stmtContext):
        print("TABLAS EN: " + dbFile.getDatabaseFS())
        print(dbFile.showTablesFS())
        pass

    # !SHOW TABLES

    # ALTER TABLE
    def enterAlter_table_stmt(self, ctx: sqlParser.Alter_table_stmtContext):
        # se llama al show tables
        table_name_old = self.getTokenValue(ctx.table_name())
        table_name_new = self.getTokenValue(ctx.new_table_name())
        r = (dbFile.showTablesFS())
        check = False
        for tables in r:
            if (tables == table_name_old):
                check = True
        if (check):
            (dbFile.renameFS(table_name_old, table_name_new))
    # !ALTER TABLE
