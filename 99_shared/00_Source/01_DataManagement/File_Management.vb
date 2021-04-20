Imports NXOpen
Imports NXOpen.UF
Imports Snap

Public Module File_Management

    Public Sub Sub_Delete_Existing_Files(ByVal File As String)
        If My.Computer.FileSystem.FileExists(File) = True Then
            My.Computer.FileSystem.DeleteFile(File)
        End If
    End Sub

End Module
