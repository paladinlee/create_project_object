import pymssql


class SchemaInfo(object):

    def __init__(self, table_name):

        self.table_name = table_name
        self.table_columns = SetSCHEMA_COLUMNS(table_name)
        self.column_names = []
        for dr in self.table_columns:
            self.column_names.append(dr["COLUMN_NAME"])

        self.identity_column = SetSCHEMA_IDENTITY()
        self.primary_column = SetSCHEMA_PRIMARY_KEY()
        # print(self.table_columns)

    def System_DataType(self, data_type):
        data_type = data_type.lower()

        match data_type:
            case "bigint":
                return "long"

            case "varbinary" | "binary" | "timestamp" | "tinyint":
                return "byte[]"

            case "bit":
                return "bool"

            case "char" | "nchar" | "ntext" | "nvarchar" | "real" | "text" | "varchar":
                return "string"

            case "date" | "datetime" | "datetime2":
                return "DateTime"

            case "datetimeoffset":
                return "DateTimeOffset"

            case "decimal" | "money" | "smallmoney":
                return "decimal"

            case "float":
                return "double"

            case "int":
                return "int"

            case "smallint":
                return "short"

            case "Time":
                return "TimeSpan"

            case "uniqueidentifier":
                return "Guid"

            case "xml":
                return "Xml"

        return data_type

def GetTableList():
    SQL_QUERY = """
SELECT TOP 5 TABLE_NAME
  FROM INFORMATION_SCHEMA.TABLES
 WHERE TABLE_TYPE = 'BASE TABLE'
   --AND TABLE_NAME LIKE 'HeavyDutyAppendixB%'
   --AND TABLE_NAME = 'ForgetPwdLog'
   --AND TABLE_NAME = 'artcAppendixInfo'
"""
    cursor = SetConn().cursor()
    cursor.execute(SQL_QUERY)

    return cursor.fetchall()

# 全域變數
def SetConn():
    global _conn
    _conn = pymssql.connect(
        server="localhost\\SQLEXPRESS02",
        user="sa",
        password="1qaz@WSX",
        database="ITRI_ARTC",
        as_dict=True,
    )
    return _conn


def SetSCHEMA_COLUMNS(table_name):
    global _dtSCHEMA_COLUMNS
    global _column_names
    global _table_name

    SQL_QUERY = """
SELECT *
  FROM INFORMATION_SCHEMA.COLUMNS
 WHERE TABLE_NAME = %s
"""
    cursor = SetConn().cursor()
    cursor.execute(SQL_QUERY, table_name)

    _dtSCHEMA_COLUMNS = cursor.fetchall()
    _column_names = []
    for dr in _dtSCHEMA_COLUMNS:
        _column_names.append(dr["COLUMN_NAME"])

    _table_name = table_name

    return _dtSCHEMA_COLUMNS


def SetSCHEMA_IDENTITY():
    global _identity_column
    _identity_column = ""

    SQL_QUERY = """
select COLUMN_NAME, TABLE_NAME
from INFORMATION_SCHEMA.COLUMNS
where TABLE_NAME = %s
AND  COLUMNPROPERTY(object_id(TABLE_SCHEMA+'.'+TABLE_NAME), COLUMN_NAME, 'IsIdentity') = 1
"""
    cursor = SetConn().cursor()
    cursor.execute(SQL_QUERY, _table_name)

    dt = cursor.fetchall()

    if len(dt) > 0:
        _identity_column = dt[0]["COLUMN_NAME"]

    return _identity_column


def SetSCHEMA_PRIMARY_KEY():
    global _primary_column
    _primary_column = ""

    SQL_QUERY = """
SELECT 
     KU.TABLE_NAME
    ,KU.COLUMN_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS TC 
INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KU
    ON TC.CONSTRAINT_TYPE = 'PRIMARY KEY' 
    AND TC.CONSTRAINT_NAME = KU.CONSTRAINT_NAME 
    AND KU.TABLE_NAME=%s
ORDER BY 
     KU.TABLE_NAME
    ,KU.ORDINAL_POSITION
"""
    cursor = SetConn().cursor()
    cursor.execute(SQL_QUERY, _table_name)

    dt = cursor.fetchall()

    _primary_column = []
    for dr in dt:
        _primary_column.append(dr["COLUMN_NAME"])

    return _primary_column
