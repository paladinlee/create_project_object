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


def CreateViewIndex():

    path = os.path.join("./", _project_name, "Views", "Business", _schema.table_name)

    if not os.path.exists(path):
        os.makedirs(path)

    file_name = "Index.cshtml"
    file_path = os.path.join(path, file_name)
    f = open(file_path, "w", encoding="UTF-8")

    text = """
@model IEnumerable<{project_name}.Models.Business.{table_name}>
<p>
    <a asp-action="Create">Create New</a>
</p>
<table class="table">
    <thead>
        <tr>
{th_list}
            <th></th>
        </tr>
    </thead>
    <tbody>
        @foreach (var item in Model)
        {{
            <tr>
{td_list}
                <td>
                    @Html.ActionLink("Edit", "Edit", new {{ {model_key} }}) |
                    @Html.ActionLink("Details", "Details", new {{ {model_key} }}) |
                    @Html.ActionLink("Delete", "Delete", new {{ {model_key} }})
                </td>
            </tr>
        }}
    </tbody>
</table>
@if (TempData.ContainsKey("AlertMessage"))
{{
    <script type="text/javascript">
        alert("@TempData["AlertMessage"]");
    </script>
}}
"""
    th_list = "".join(
        [
            """
            <th>
                @Html.ActionLink("{column_name}", "Index", new {{ sortExpression = "{column_name}", sortDirection = TempData["SortDirection"] }})
            </th>
             """.format(
                column_name=p
            )
            for p in _schema.column_names
        ]
    )

    td_list = "".join(
        [
            """
                <td>
                    @Html.DisplayFor(modelItem => item.{column_name})
                </td>
             """.format(
                column_name=p
            )
            for p in _schema.column_names
        ]
    )

    model_key = ""
    if len(_schema.identity_column) > 0:
        model_key = " %s = item.%s" % (
            _schema.identity_column,
            _schema.identity_column,
        )
    else:
        model_key = ",".join(
            [" %s = item.%s" % (p, p) for p in _schema.primary_column]
        )

    f.write(
        text.format(
            project_name=_project_name,
            table_name=_schema.table_name,
            th_list=th_list,
            td_list=td_list,
            model_key=model_key,
        )
    )

    f.close()

def CreateViewDetails():

    path = os.path.join("./", _project_name, "Views", "Business", _schema.table_name)

    if not os.path.exists(path):
        os.makedirs(path)

    file_name = "Details.cshtml"
    file_path = os.path.join(path, file_name)
    f = open(file_path, "w", encoding="UTF-8")

    text = """
@model {project_name}.Models.Business.{table_name}

<div>
    <h4>{table_name}</h4>
    <hr />
    <dl class="row">
{d_list}       
    </dl>
</div>
<div>
    @Html.ActionLink("Edit", "Edit", new {{ {model_key} }}) |
    <a asp-action="Index">Back to List</a>
</div>
"""
  
    d_list = "".join(
        [
            """
        <dt class = "col-sm-2">
            @Html.DisplayNameFor(model => model.{column_name})
        </dt>
        <dd class = "col-sm-10">
            @Html.DisplayFor(model => model.{column_name})
        </dd>
             """.format(
                column_name=p
            )
            for p in _schema.column_names
        ]
    )

    model_key = ""
    if len(_schema.identity_column) > 0:
        model_key = " %s = Model.%s" % (
            _schema.identity_column,
            _schema.identity_column,
        )
    else:
        model_key = ",".join(
            [" %s = Model.%s" % (p, p) for p in _schema.primary_column]
        )

    f.write(
        text.format(
            project_name=_project_name,
            table_name=_schema.table_name,
            d_list=d_list,
            model_key=model_key,
        )
    )

    f.close()

def CreateViewCreate():

    path = os.path.join("./", _project_name, "Views", "Business", _schema.table_name)

    if not os.path.exists(path):
        os.makedirs(path)

    file_name = "Create.cshtml"
    file_path = os.path.join(path, file_name)
    f = open(file_path, "w", encoding="UTF-8")

    text = """
@model {project_name}.Models.Business.{table_name}

<h4>{table_name}</h4>
<hr />
<div class="row">
    <div class="col-md-4">
        <form asp-action="Create">
            <div asp-validation-summary="ModelOnly" class="text-danger"></div>
{div_list}
            <div class="form-group">
                <input type="submit" value="Create" class="btn btn-primary" />
            </div>
        </form>
    </div>
</div>

<div>
    <a asp-action="Index">Back to List</a>
</div>

@section Scripts {{
    @{{await Html.RenderPartialAsync("_ValidationScriptsPartial");}}
}}
@if (TempData.ContainsKey("AlertMessage"))
{{
    <script type="text/javascript">
        alert("@TempData["AlertMessage"]");
    </script>
}}
"""
  
    div_list = "".join(
        [
            """
            <div class="form-group">
                <label asp-for="{column_name}" class="control-label"></label>
                <input asp-for="{column_name}" class="form-control" />
                <span asp-validation-for="{column_name}" class="text-danger"></span>
            </div>
             """.format(
                column_name=p
            )
            for p in _schema.column_names
        ]
    )

    f.write(
        text.format(
            project_name=_project_name,
            table_name=_schema.table_name,
            div_list=div_list,
        )
    )

    f.close()

def CreateViewEdit():

    path = os.path.join("./", _project_name, "Views", "Business", _schema.table_name)

    if not os.path.exists(path):
        os.makedirs(path)

    file_name = "Edit.cshtml"
    file_path = os.path.join(path, file_name)
    f = open(file_path, "w", encoding="UTF-8")

    text = """
@model {project_name}.Models.Business.{table_name}

<h4>{table_name}</h4>
<hr />
<div class="row">
    <div class="col-md-4">
        <form asp-action="Edit">
            <div asp-validation-summary="ModelOnly" class="text-danger"></div>
{div_list}
            <div class="form-group">
                <input type="submit" value="Save" class="btn btn-primary" />
            </div>
        </form>
    </div>
</div>

<div>
    <a asp-action="Index">Back to List</a>
</div>

@section Scripts {{
    @{{
        await Html.RenderPartialAsync("_ValidationScriptsPartial");
    }}
}}
@if (TempData.ContainsKey("AlertMessage"))
{{
    <script type="text/javascript">
        alert("@TempData["AlertMessage"]");
    </script>
}}
"""
  
    div_list = "".join(
        [
            """
            <div class="form-group">
                <label asp-for="{column_name}" class="control-label"></label>
                <input asp-for="{column_name}" class="form-control" />
                <span asp-validation-for="{column_name}" class="text-danger"></span>
            </div>
             """.format(
                column_name=p
            )
            for p in _schema.column_names
        ]
    )

    f.write(
        text.format(
            project_name=_project_name,
            table_name=_schema.table_name,
            div_list=div_list,
        )
    )

    f.close()


def Create(project_name, table_name):

    ProjectName(project_name)

    if table_name == "--All--":
        dt = schema_info.GetTableList()
    else:
        dt = [{'TABLE_NAME': table_name}]

    global _schema
    for dr in dt:
        _schema = schema_info.SchemaInfo(dr["TABLE_NAME"])
        CreateViewIndex()
        CreateViewDetails()
        CreateViewCreate()
        CreateViewEdit()


# Create("CreateObjectByPython")
