Imports NXOpen
Imports NXOpen.UF

Public Module Mod_Output
    '# Data sorting and ID assigned
    '###########################################################################
    Public Sub Sub_Table_sorting(ByVal sortVariable As String, ByRef DataTable As DataTable)

        Dim CurrView As System.Data.DataView

        CurrView = New System.Data.DataView(DataTable)
        CurrView.Sort = sortVariable & " DESC"

        DataTable = CurrView.ToTable()

        For l = 0 To DataTable.Rows.Count - 1

            '# ID Assignment
            DataTable.Rows(l).Item("ID") = l + 1

        Next

    End Sub

    '# Data Export
    '###########################################################################
    Public Sub Sub_Table_exporting(ByVal File_Name As String, ByVal D_Table As DataTable)
        Dim Row As String = Nothing
        Dim D_Row As DataRow
        Dim D_Column As DataColumn
        Dim str As New Text.StringBuilder
        Dim Table_exporting As String = Nothing

        Dim Output_CSV_Path = Part_Folder_Path
        Dim File_Path_Name = Output_CSV_Path + File_Name
        Sub_Delete_Existing_Files(File_Path_Name)
        Dim CSV_File As IO.StreamWriter = Func_Text_File_open(File_Path_Name)

        '#  --- Columns superscriptions
        For Each D_Column In D_Table.Columns
            Row += IIf(Row <> "", ";", "").ToString
            Row += D_Column.ColumnName
        Next
        Table_exporting += Row & Chr(13)

        '#  --- Output of all lines
        For Each D_Row In D_Table.Rows

            Row = Nothing
            '#  Loop over all columns
            For Each D_Column In D_Table.Columns
                Row += IIf(Row <> "", ";", "").ToString
                Dim intermediate_value = D_Row.Item(D_Column.ColumnName)
                If intermediate_value.GetType() = GetType(Double) Then
                    Dim Entry As Double = intermediate_value
                    Row += Entry.ToString("r", System.Globalization.CultureInfo.CreateSpecificCulture("en-US"))
                Else
                    Dim Entry = intermediate_value
                    Row += Entry.ToString
                End If
            Next
            Table_exporting += Row & Chr(13)

        Next
        '# Close csv file
        CSV_File.WriteLine(Table_exporting)
        Sub_Text_File_Close(CSV_File)

    End Sub

    '# Create new DataSet and DataTable (table)
    '###########################################################################
    Public Function Func_Create_Table(ByVal Columns_List As List(Of List(Of String))) As DataSet

        Dim Data_Set As New DataSet   '# new DataSet
        Dim Table = New DataTable() '# New Datatable

        Dim ListLength As Integer
        ListLength = Columns_List.Count

        For i = 0 To ListLength - 1
            Table.Columns.Add(New DataColumn(Columns_List(i)(0), Type.GetType(Columns_List(i)(1))))
        Next

        '# Add new table to DataSet
        Data_Set.Tables.Add(Table)

        '# Return the new DataTable
        Func_Create_Table = Data_Set

    End Function
    Public Function Funk_Create_Table_2(ByVal Columns_List As List(Of List(Of String))) As DataTable

        Dim Table = New DataTable() '# New Datatable

        Dim Length_List As Integer
        Length_List = Columns_List.Count

        For i = 0 To Length_List - 1
            Table.Columns.Add(New DataColumn(Columns_List(i)(0), Type.GetType(Columns_List(i)(1))))
        Next

        '# Return the new DataTable
        Funk_Create_Table_2 = Table

    End Function
End Module
