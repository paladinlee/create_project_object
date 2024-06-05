"""
Connects to a SQL database using pymssql
"""

import xlwt, datetime
import schema_info


def CreateSheet(book, tableName):

    sheet = book.add_sheet(tableName[0:31])

    dt = _schema.table_columns

    field_names = list(dt[0].keys())

    num_fields = len(field_names)

    i = 0
    while i < num_fields:

        sheet.write(0, i, field_names[i])
        i = i + 1

    r = 1
    for dr in dt:
        c = 0
        while c < num_fields:
            name = field_names[c]
            sheet.write(r, c, dr[name])
            c = c + 1

        r = r + 1


def Export(table_name):

    book = xlwt.Workbook(encoding="utf-8")

    if table_name == "--All--":
        dt = schema_info.GetTableList()
    else:
        dt = [{"TABLE_NAME": table_name}]

    global _schema
    for dr in dt:
        _schema = schema_info.SchemaInfo(dr["TABLE_NAME"])
        CreateSheet(book, dr["TABLE_NAME"])

    fileName = datetime.datetime.now().strftime("%Y%m%d%H%M") + ".xls"

    book.save(fileName)

    return fileName


# Export()
