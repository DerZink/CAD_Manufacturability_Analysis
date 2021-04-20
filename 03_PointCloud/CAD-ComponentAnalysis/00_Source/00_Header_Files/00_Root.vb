Option Strict Off
Imports System
Imports NXOpen
Imports NXOpen.UF
Imports SharedModule.Public_Variable
Imports SharedModule.Capture_Assembly
Imports SharedModule.File_Management

Module Source

    Public Sub Main(ByVal args As String())

        'Dim Args() As String = {"0"}
        Try
            Console.WriteLine("## NX CurvatureData")
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

            SharedModule._00_Min_Box._start(BoxDir_1, BoxDir_2)
            SharedModule._01_PointsCloud._start()
            SharedModule._02_Analyse._start()

            Dim PartSavedStatus As PartSaveStatus = Nothing
            Dim Output_Part As Part = theSession.Parts.Display
            Dim Output_Part_Export As String = Part_Folder_Path + Part_Name_org + Data_Name + ".prt"
            Sub_Delete_Existing_Files(Output_Part_Export)
            PartSavedStatus = Output_Part.SaveAs(Output_Part_Export)

        Catch ex As Exception
            Console.WriteLine(ex.ToString)
            Console.WriteLine(ex.ToString)
            Dim Path_Exe_Act = Environment.CurrentDirectory()
            Dim Uhrzeit As String = String.Format("{0}{1}", Now.TimeOfDay.Hours, Now.TimeOfDay.Minutes)
            Dim Error_File_Name As String = Date_now + "_Error_PointCloudAnalysis_" + Part_Name_org + "_" + Uhrzeit + ".txt"
            Dim Error_File As IO.StreamWriter
            Error_File = My.Computer.FileSystem.OpenTextFileWriter(Path_Exe_Act + System.IO.Path.DirectorySeparatorChar.ToString + Error_File_Name, False)
            Error_File.WriteLine(ex.ToString)
            Error_File.Close()
        End Try

    End Sub

End Module


