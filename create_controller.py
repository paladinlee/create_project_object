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


def CreateController():

    path = os.path.join("./", _project_name, "Controllers", "Business")

    if not os.path.exists(path):
        os.makedirs(path)

    file_name = _schema.table_name + "Controller.cs"
    file_path = os.path.join(path, file_name)
    f = open(file_path, "w", encoding="UTF-8")

    text = """
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

using {project_name}.Models.Business;
using Shared.Utilities;
using Dapper;

namespace {project_name}.Controllers.Business
{{
    public class {table_name}Controller : Controller
    {{
        private readonly DbConnectionFactory _dbConnectionFactory;
        
        public {table_name}Controller(DbConnectionFactory dbConnectionFactory)
        {{
            _dbConnectionFactory = dbConnectionFactory;
        }}

        // GET: {table_name}Controller
        public ActionResult Index(int pageIndex, int pageSize, string sortExpression,string sortDirection)
        {{
            TempData["PageIndex"] = pageIndex;
            TempData["PageSize"] = pageSize;
            TempData["SortExpression"] = sortExpression;
            TempData["SortDirection"] = sortDirection;
            if (TempData["SortDirection"] + "" == "DESC")
                TempData["SortDirection"] = "";
            else
                TempData["SortDirection"] = "DESC";
                
            {table_name} model = new {table_name}();
            DynamicParameters @params = model.SqlParameters();
            @params.Add("@PageIndex", pageIndex);
            @params.Add("@PageSize", pageSize);

            var reader = _dbConnectionFactory.GetDefault()
                .QueryMultiple2(model.SqlList(TempData["SortExpression"]+"", TempData["SortDirection"]+ ""), @params, "取得 設定值 發生錯誤，錯誤訊息：{{0}}");

            var mains = reader.Read<{table_name}>().ToArray();

            return View("~/Views/Business/{table_name}/Index.cshtml", mains);
        }}

        // GET: {table_name}Controller/Details/5
        public ActionResult Details({param_key})
        {{
            {table_name} model = new {table_name}();
            {model_key}
            DynamicParameters @params = model.SqlParameters();
            var reader = _dbConnectionFactory.GetDefault()
                .QueryMultiple2(model.SqlSelect(), @params, "取得 設定值 發生錯誤，錯誤訊息：{{0}}");

            var mains = reader.Read<{table_name}>().ToArray();

            if (mains.Count() > 0)
                model = mains.First();

            return View("~/Views/Business/{table_name}/Details.cshtml", model);
        }}

        // GET: {table_name}Controller/Create
        public ActionResult Create()
        {{
            {table_name} model = new {table_name}();
            return View("~/Views/Business/{table_name}/Create.cshtml", model);
        }}

        // POST: {table_name}Controller/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Create([FromForm] {table_name} model)
        {{
            try
            {{
                DynamicParameters @params = model.SqlParameters();
                _dbConnectionFactory.GetDefault()
                    .Execute2(model.SqlInsert(), @params, "取得 設定值 發生錯誤，錯誤訊息：{{0}}");

                TempData["AlertMessage"] = "存檔成功";
                return RedirectToAction("Index");
            }}
            catch (Exception ex)
            {{
                TempData["AlertMessage"] = ex.Message;
                return View("~/Views/Business/{table_name}/Create.cshtml", model);
            }}
        }}

        // GET: {table_name}Controller/Edit/5
        public ActionResult Edit({param_key})
        {{            
            {table_name} model = new {table_name}();
            {model_key}
            DynamicParameters @params = model.SqlParameters();
            var reader = _dbConnectionFactory.GetDefault()
                .QueryMultiple2(model.SqlSelect(), @params, "取得 設定值 發生錯誤，錯誤訊息：{{0}}");

            var mains = reader.Read<{table_name}>().ToArray();

            if (mains.Count() > 0)
                model = mains.First();
            return View("~/Views/Business/{table_name}/Edit.cshtml", model);
        }}

        // POST: {table_name}Controller/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Edit({param_key}, [FromForm] {table_name} model)
        {{
            try
            {{
            
                DynamicParameters @params = model.SqlParameters();
                _dbConnectionFactory.GetDefault()
                    .Execute2(model.SqlUpdate(), @params, "取得 設定值 發生錯誤，錯誤訊息：{{0}}");

                TempData["AlertMessage"] = "存檔成功";
                return RedirectToAction("Index");
            }}
            catch (Exception ex)
            {{
                TempData["AlertMessage"] = ex.Message;
                return View("~/Views/Business/{table_name}/Edit.cshtml", model);
            }}
        }}

        // GET: {table_name}Controller/Delete/5
        public ActionResult Delete({param_key})
        {{
            {table_name} model = new {table_name}();
            {model_key}
            DynamicParameters @params = model.SqlParameters();
            _dbConnectionFactory.GetDefault()
                .Execute2(model.SqlDelete(), @params, "取得 設定值 發生錯誤，錯誤訊息：{{0}}");

            TempData["AlertMessage"] = "刪除成功";
            return RedirectToAction("Index");
        }}

        // POST: {table_name}Controller/Delete/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Delete({param_key}, [FromForm] {table_name} model)
        {{
            try
            {{
                DynamicParameters @params = model.SqlParameters();
                _dbConnectionFactory.GetDefault()
                    .Execute2(model.SqlDelete(), @params, "取得 設定值 發生錯誤，錯誤訊息：{{0}}");

                TempData["AlertMessage"] = "刪除成功";
                return RedirectToAction("Index");
            }}
            catch (Exception ex)
            {{
                TempData["AlertMessage"] = ex.Message;
                return View("~/Views/Business/{table_name}/Edit.cshtml", model);
            }}
        }}
    }}
}}


"""
    model_key = ""
    param_key = ""
    if len(_schema.identity_column) > 0:
        model_key = " model.%s = %s;" % (
            _schema.identity_column,
            _schema.identity_column,
        )
        for dr in _schema.table_columns:
            if dr["COLUMN_NAME"] == _schema.identity_column:
                # print(dr["DATA_TYPE"])
                param_key = "%s %s" % (
                    _schema.System_DataType(dr["DATA_TYPE"]),
                    _schema.identity_column,
                )
    else:
        model_key = "\n".join(
            [" model.%s = %s;" % (p, p) for p in _schema.primary_column]
        )

        columns = [
            x
            for x in _schema.table_columns
            if x["COLUMN_NAME"] in _schema.primary_column
        ]
        param_key = ", ".join(
            [
                "{DATA_TYPE} {COLUMN_NAME}".format(
                    DATA_TYPE=_schema.System_DataType(dr["DATA_TYPE"]),
                    COLUMN_NAME=dr["COLUMN_NAME"],
                )
                for dr in columns
            ]
        )

    f.write(
        text.format(
            project_name=_project_name,
            table_name=_schema.table_name,
            model_key=model_key,
            param_key=param_key,
        )
    )

    f.close()


def is_even(x):
    c = ""
    c = x["COLUMN_NAME"]
    print("TestHourCounts" in _schema.primary_column)
    # if _schema.primary_column.index(c) >= 0:
    #     return True
    # else:
    return False


def Create(project_name, table_name):

    ProjectName(project_name)

    if table_name == "--All--":
        dt = schema_info.GetTableList()
    else:
        dt = [{'TABLE_NAME': table_name}]
    
    global _schema
    for dr in dt:
        _schema = schema_info.SchemaInfo(dr["TABLE_NAME"])
        CreateController()


# Create("ITRI_ARTC,","evf_monthlydatalist_d")
