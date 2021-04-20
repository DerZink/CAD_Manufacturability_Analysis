Option Strict Off
Imports System
Imports NXOpen
Imports NXOpen.UF
Imports Snap
Imports SharedModule.Public_Variable
Imports SharedModule.Text_File_Management

Module Source

    Public Sub Main(ByVal args As String())

        Try

            Sub_Reading_Arguments(args)

            Dim Status_Start As New UFPart.LoadStatus
            Dim Tag_Start As New Tag '= Nothing
            Dim File = Part_Folder_Path + Part_Name_org + Part_Format
            theUFSession.Part.Open(File, Tag_Start, Status_Start)
            Part_act = Utilities.NXObjectManager.Get(Tag_Start)
            Dim PartLoadStatus1 As PartLoadStatus = Nothing

            '# Defines Workpart without representing it individually
            'theSession.Parts.SetWork(Part_act)
            '# Defines Workpart and displays it individually
            theSession.Parts.SetDisplay(Part_act, False, False, PartLoadStatus1)
            PartLoadStatus1.Dispose()
            '# Open the bodies in Part and add them to the list, Public Variables
            Body_List = Part_act.Bodies.ToArray()
            '# Only one body should exist after AssemblyDecomposition
            Body_act = Body_List(0)
            '# SurfaceAnalysis
            Sub_Part_Surface_Data()

        Catch ex As Exception
            Console.WriteLine(ex.ToString)
            Dim Path_Exe_Act = Environment.CurrentDirectory()
            Dim UhrTime As String = String.Format("{0}{1}", Now.TimeOfDay.Hours, Now.TimeOfDay.Minutes)
            Dim ErrorFileName As String = Date_now + "_Error_SurfaceAnalysis_" + Part_Name_org + "_" + UhrTime + ".txt"
            Dim Error_File = Func_Text_file_Open(Path_Exe_Act + System.IO.Path.DirectorySeparatorChar.ToString + ErrorFileName)
            Error_File.WriteLine(ex.ToString)
            Sub_Text_File_Close(Error_File)
        End Try

    End Sub

End Module


