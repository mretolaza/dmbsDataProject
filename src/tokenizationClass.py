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

    # INSERT
    def enterInsert_stmt(self, ctx: sqlParser.Insert_stmtContext):

        tableName = self.getTokenValue(ctx.table_name())
        tableData = eval(dbFile.readTableFS(tableName, "data"))

        # table structure
        tableStructure = eval(dbFile.readTableFS(tableName, "structure"))
        # input col structure
        targetCols = [self.getTokenValue(col) for col in ctx.column_name()]

        newData = []

        values = [self.getTokenValue(value) for value in ctx.expr()]
        colNames = [col[0] for col in tableStructure]
        colTypes = [col[1] for col in tableStructure]

        if len(values) > len(tableStructure):
            raise ValueError("LA PETICIÓN DE INSERTAR TIENE MÁS VALORES QUE LA LONGITUD DE LA MESA")

        # specific insert stmt

        if len(targetCols):
            newData = [""] * len(tableStructure)
            for targetCol in targetCols:
                if targetCol in colNames:
                    colIndex = targetCols.index(targetCol)
                    valueIndex = colNames.index(targetCol)
                    if (not len(values) > valueIndex):
                        newData[colIndex] = 'NULL'
                    else:
                        newData[colIndex] = dataCM.matchData(colTypes[colIndex], values[valueIndex])
                else:
                    raise ValueError("LA COLUMNA " + targetCol + " NO EXISTE EN LA TABLA " + tableName)

        # regular insert stmt

        else:
            index = 0
            for value in ctx.expr():
                newData.append(dataCM.matchData(tableStructure[index][1], self.getTokenValue(value)))
                index = index + 1

        if len(newData):
            if None in newData:
                raise ValueError("AL MOMENTO DE INSERTAR LA CONSULTA TIENE TIPOS INCONSISTENTES")
            tableData.append(tuple(newData))
            dbFile.insertTableFS(tableName, str(tableData))
            print("INSERT A " + tableName + " EXITOSO")
        else:
            dataCM.raiseError(False, "NO SE PUEDE INSERTAR EN UNA TUPLA VACÍA")

    # !INSERT

    # SELECT SECTION
    def enterSelect_core(self, ctx: sqlParser.Select_coreContext):

        tableName = self.getTokenValue(ctx.table_or_subquery()[0].table_name())

        tableStructure = eval(dbFile.readTableFS(tableName, "structure"))
        tableData = eval(dbFile.readTableFS(tableName, "data"))
        colNames = [col[0] for col in tableStructure]

        # check if table exists in database
        if tableName not in dbFile.showTablesFS():
            raise ValueError("LA TABLA" + tableName + " NO EXISTE EN " + dbFile.currentDatabase)

        dataCM.setSavedStructure(tableStructure)

        # insert target columns
        targets = [self.getTokenValue(target) for target in ctx.result_column()]

        if "*" in targets:
            dataCM.setSavedData(tableData)
        else:

            if all(value in colNames for value in targets):
                targetsIndex = [colNames.index(elem) for elem in targets]
                filteredData = []
                for tup in tableData:
                    filteredValue = []
                    for col in targetsIndex:
                        filteredValue.append(tup[col])
                    filteredData.append(tuple(filteredValue))
                dataCM.setSavedData(filteredData)

            else:
                raise ValueError("AL MENOS UNA DE LAS TABLAS OBJETIVO NO EXISTE EN" + tableName)

        # Exit a parse tree produced by sqlParser#select_core.

    def exitSelect_core(self, ctx: sqlParser.Select_coreContext):
        dbPrint.print_table(dataCM.isSavedData, [col[0] for col in dataCM.structureSaved])
        print(dataCM.isSavedData)

    # !SELECT SECTION

    # SELECT REDUCE (WHERE)
    def enterExprComparisonSecond(self, ctx: sqlParser.ExprComparisonSecondContext):
        if dataCM.multiples:
            pass
        else:
            builtCondition = dataCM.queryWhereStringCLBuilder(
                [col[0] for col in dataCM.structureSaved].index(self.getTokenValue(ctx.expr()[0])),
                self.getTokenValue(ctx.expr()[1]),
                self.getTokenValue(ctx.children[1])
            )
            dataCM.setSavedData(dataCM.handleNullValue(dataCM.isSavedData, builtCondition))

    # !SELECT REDUCE (WHERE)

    # SELECT AND
    def enterExprAnd(self, ctx: sqlParser.ExprAndContext):
        dataCM.multiples = True
        conditions = ctx.expr()
        reducedData = []

        for condition in conditions:
            builtCondition = dataCM.queryWhereStringCLBuilder(
                [col[0] for col in dataCM.structureSaved].index(self.getTokenValue(condition.expr()[0])),
                self.getTokenValue(condition.expr()[1]),
                self.getTokenValue(condition.children[1])
            )
            reducedData.append(dataCM.handleNullValue(dataCM.isSavedData, builtCondition))

        dataCM.setSavedData(dataCM.handleAndStmt(reducedData))

    # !SELECT AND 

    # SELECT OR
    def enterExprOr(self, ctx: sqlParser.ExprOrContext):
        dataCM.multiples = True
        conditions = ctx.expr()
        reducedData = []

        for condition in conditions:
            builtCondition = dataCM.queryWhereStringCLBuilder(
                [col[0] for col in dataCM.structureSaved].index(self.getTokenValue(condition.expr()[0])),
                self.getTokenValue(condition.expr()[1]),
                self.getTokenValue(condition.children[1])
            )
            reducedData.append(dataCM.handleNullValue(dataCM.isSavedData, builtCondition))

        dataCM.setSavedData(dataCM.handleOrStmt(reducedData))
    # !SELECT OR