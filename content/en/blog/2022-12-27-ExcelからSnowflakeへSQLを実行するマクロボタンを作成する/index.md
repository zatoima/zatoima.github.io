---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Creating a Macro Button to Execute SQL from Excel to Snowflake"
subtitle: ""
summary: " "
tags: ["Snowflake"]
categories: ["Snowflake"]
url: snowflake-excel-sql-execute-macro-button
date: 2022-12-27
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---

### Overview

Creating a macro button in Excel to execute SQL against Snowflake via ODBC connection.

The implementation uses the `QueryTable` object in VBA to retrieve data from Snowflake.

### VBA Code

```vb
Sub ExecuteSnowflakeQuery()
    Dim conn As String
    Dim sql As String
    Dim ws As Worksheet
    Dim qt As QueryTable

    ' ODBC connection string
    conn = "ODBC;DSN=snowflake_dsn;uid=YOUR_USERNAME;pwd=YOUR_PASSWORD"

    ' SQL to execute
    sql = "SELECT * FROM YOUR_TABLE LIMIT 100"

    ' Target sheet
    Set ws = ThisWorkbook.Sheets("Sheet1")

    ' Clear existing query tables
    Dim qt2 As QueryTable
    For Each qt2 In ws.QueryTables
        qt2.Delete
    Next qt2

    ' Clear existing data
    ws.Cells.Clear

    ' Create QueryTable
    Set qt = ws.QueryTables.Add( _
        Connection:="ODBC;" & "DSN=snowflake_dsn;uid=YOUR_USERNAME;pwd=YOUR_PASSWORD", _
        Destination:=ws.Range("A1"), _
        Sql:=sql)

    ' Execute query
    With qt
        .FieldNames = True
        .RowNumbers = False
        .FillAdjacentFormulas = False
        .PreserveFormatting = True
        .RefreshOnFileOpen = False
        .BackgroundQuery = True
        .RefreshStyle = xlInsertDeleteCells
        .SavePassword = False
        .SaveData = True
        .AdjustColumnWidth = True
        .RefreshPeriod = 0
        .PreserveColumnInfo = True
        .Refresh BackgroundQuery:=False
    End With

    MsgBox "Query executed successfully!"
End Sub
```

### Performance Results

Query execution times measured with this approach:

| Rows Returned | Execution Time |
|--------------|----------------|
| 100 rows     | ~2 seconds     |
| 1,000 rows   | ~5 seconds     |
| 10,000 rows  | ~30 seconds    |

### Notes

- The `QueryTable` approach works well for moderate data volumes
- For large datasets, consider using Snowflake's native export features
- The ODBC connection must be pre-configured (see the M1 Mac ODBC setup article)
- Password is embedded in the connection string in this example; consider more secure approaches for production use
