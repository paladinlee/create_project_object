"""
Connects to a SQL database using pymssql
"""

import pymssql, os, codecs
import schema_info


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


def ProjectName(project_name):
    global _project_name
    _project_name = project_name

    path = os.path.join("./", project_name)
    if not os.path.exists(path):
        os.makedirs(path)

    return _project_name


def CreateClass():

    path = os.path.join("./", _project_name, "Models", "Business")

    if not os.path.exists(path):
        os.makedirs(path)

    file_name = _schema.table_name + ".cs"
    file_path = os.path.join(path, file_name)
    f = open(file_path, "w", encoding="UTF-8")

    text = """
using Dapper;

namespace {project_name}.Models.Business;
public class {table_name}
{{
 {class_params}

  public string SqlList(string sortExpression,string sortDirection)
  {{
    
 {func_list}

  }}

  public string SqlSelect()
  {{
    
return @"
 {sql_select}
";
  }}

  public string SqlInsert()
  {{
    
return @"
 {sql_insert}
";
  }}

  public string SqlUpdate()
  {{
    
return @"
 {sql_update}
";
  }}

  public string SqlDelete()
  {{
    
return @"
 {sql_delete}
";
  }}

  public DynamicParameters SqlParameters()
  {{
{sql_parameters}
  }}

}}
"""

    f.write(
        text.format(
            project_name=_project_name,
            table_name=_schema.table_name,
            class_params=CreateParams(),
            func_list=CreateFuncList(),
            sql_select=CreateSqlSelect(),
            sql_insert=CreateSqlInsert(),
            sql_update=CreateSqlUpdate(),
            sql_delete=CreateSqlDelete(),
            sql_parameters=CreateSqlParameters(),
        )
    )

    f.close()


def CreateParams():

    text = ""

    for dr in _schema.table_columns:
        is_nullable = ""
        if dr["IS_NULLABLE"] == "YES":
            is_nullable = "?"

        text = (
            text
            + " public {DataType}{IsNull} {ParamName}".format(
                DataType=_schema.System_DataType(dr["DATA_TYPE"]),
                IsNull=is_nullable,
                ParamName=dr["COLUMN_NAME"],
            )
            + " { get; set; }\n "
        )

    return text


def CreateFuncList():

    text = """
        string orderSort = "{primary_column}";
        if (string.IsNullOrEmpty(sortExpression) == false)
            orderSort = sortExpression + " " + sortDirection;

        return @" 
IF(@PageIndex='' or @PageIndex = 0)
BEGIN
	SET @PageIndex=1
END

IF(@PageSize='' or @PageSize = 0)
BEGIN
	SET @PageSize=25
END

SELECT A.* FROM 
    (SELECT * FROM {table_name}) AS A
ORDER BY " + orderSort + @"
OFFSET (@PageIndex - 1) * @PageSize ROWS
FETCH NEXT @PageSize ROWS ONLY;
";
"""

    # region 生成 where column

    primary_column = ""
    if len(_schema.identity_column) > 0:
        primary_column = _schema.identity_column
    else:
        primary_column = ",".join(_schema.primary_column)

    # endregion

    return text.format(table_name=_schema.table_name, primary_column=primary_column)


def CreateSqlSelect():
    text = """
SELECT * FROM %s
 %s
"""

    # region 生成 where column

    strWhere = ""
    if len(_schema.identity_column) > 0:
        strWhere = "WHERE %s = @%s " % (
            _schema.identity_column,
            _schema.identity_column,
        )
    else:
        strWhere = "WHERE " + "\n   AND ".join(
            ["%s = @%s " % (p, p) for p in _schema.primary_column]
        )

    # endregion

    return text % (_schema.table_name, strWhere)


def CreateSqlInsert():
    text = """
INSERT INTO %s
           (%s)
     VALUES
           (%s)
"""
    # 複製 _column_names
    columns = [i for i in _schema.column_names]

    # identity 會自動編號，不需放入 params
    if _schema.identity_column in columns:
        columns.remove(_schema.identity_column)

    strColumn = ", ".join(columns)
    strParam = "@" + ", @".join(columns)
    return text % (_schema.table_name, strColumn, strParam)


def CreateSqlUpdate():
    text = """
UPDATE %s
 %s
 %s
"""
    # region 生成 set column

    # 複製 _column_names
    columns = [i for i in _schema.column_names]

    # identity 無法編輯，不需放入 params
    if _schema.identity_column in columns:
        columns.remove(_schema.identity_column)

    strParam = "  SET " + "\n     , ".join(["%s = @%s " % (c, c) for c in columns])
    # endregion

    # region 生成 where column

    strWhere = ""
    if len(_schema.identity_column) > 0:
        strWhere = "WHERE %s = @%s " % (
            _schema.identity_column,
            _schema.identity_column,
        )
    else:
        strWhere = "WHERE " + "\n   AND ".join(
            ["%s = @%s " % (p, p) for p in _schema.primary_column]
        )

    # endregion

    return text % (_schema.table_name, strParam, strWhere)


def CreateSqlDelete():
    text = """
DELETE FROM %s
 %s
"""

    # region 生成 where column

    strWhere = ""
    if len(_schema.identity_column) > 0:
        strWhere = "WHERE %s = @%s " % (
            _schema.identity_column,
            _schema.identity_column,
        )
    else:
        strWhere = "WHERE " + "\n   AND ".join(
            ["%s = @%s " % (p, p) for p in _schema.primary_column]
        )

    # endregion

    return text % (_schema.table_name, strWhere)


def CreateSqlParameters():
    text = """
    var sqlParameters = new DynamicParameters();

%s

    return sqlParameters;
"""

    strParam = "\n".join(
        ['    sqlParameters.Add("@%s", %s);' % (c, c) for c in _schema.column_names]
    )

    return text % (strParam)


def Create(project_name, table_name):

    ProjectName(project_name)

    if table_name == "--All--":
        dt = schema_info.GetTableList()
    else:
        dt = [{'TABLE_NAME': table_name}]
    
    global _schema
    for dr in dt:
        _schema = schema_info.SchemaInfo(dr["TABLE_NAME"])
        CreateClass()


# Create("ITRI_ARTC")