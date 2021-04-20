Public Module Text_File_Management

    Function Func_Text_File_open(ByRef File_Path_Name As String) As IO.StreamWriter
        Dim File As IO.StreamWriter
        File = My.Computer.FileSystem.OpenTextFileWriter(File_Path_Name, False)
        Return File
    End Function

    Sub Sub_Text_File_Close(ByRef File As IO.StreamWriter)
        File.Close()
    End Sub

End Module
