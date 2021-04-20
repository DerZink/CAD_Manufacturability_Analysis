Option Strict Off
Imports System
Imports System.Drawing
Imports NXOpen
Imports System.Collections.Generic
Imports System.ComponentModel
Imports System.Data
Imports System.Text
Imports NXOpen.UF
Imports NXOpen.TDP
Imports System.Windows.Forms
Imports SharedModule.Public_Variable
Imports SharedModule.Capture_Assembly

Module Source

    Public Sub Main(ByVal args As String())

        Try
            Console.WriteLine("## NX 3D creation")
            Dim Path_Exe_Act = Environment.CurrentDirectory()
            Console.WriteLine(Path_Exe_Act)
            Sub_Reading_Arguments(args)
            Dim Status_Start As New UFPart.LoadStatus
            Dim Tag_Start As New Tag '= Nothing
            Dim File = Part_Folder_Path + Part_Name_org + Part_Format
            theUFSession.Part.Open(File, Tag_Start, Status_Start)
            Part_act = Utilities.NXObjectManager.Get(Tag_Start)
            'Dim PartLoadStatus1 As PartLoadStatus = Nothing
            '# Defines Workpart without representing it individually
            theSession.Parts.SetWork(Part_act)
            '# Defines Workpart and displays it individually
            'theSession.Parts.SetDisplay(Part_act, False, False, PartLoadStatus1)
            'PartLoadStatus1.Dispose()

            Dim Work_Part As Part = theSession.Parts.Work

            Dim theTDPManager As NXOpen.TDP.Manager = NXOpen.TDP.Manager.GetManager(theSession)
            Dim publisherBuilder As NXOpen.TDP.PublisherBuilder = Nothing
            publisherBuilder = theTDPManager.CreateTdpPublisherBuilder(Work_Part)

            publisherBuilder.ViewSelection = NXOpen.TDP.PublisherBuilder.ViewSelectionType.AllViews

            Dim PartPDF As String = Part_Folder_Path & Part_Name_org & "_" & "3D" & ".pdf"
            publisherBuilder.OutputFilename = PartPDF

            publisherBuilder.Compression = True
            publisherBuilder.ModelAccuracy = PublisherBuilder.ModelAccuracyType.Maximum

            publisherBuilder.OverrideColors = True
            publisherBuilder.BackgroundColor = Work_Part.Colors.Find("White")
            publisherBuilder.PmiColor = Work_Part.Colors.Find("Black")


            publisherBuilder.SetWorkTemplateFile(TDP_Path)

            Console.WriteLine("## IN")
            Dim result As PublisherBuilder.PublishResult = Nothing
            result = publisherBuilder.Publish()
            Console.WriteLine(result.ToString())
            Console.WriteLine("## OUT")

            Dim outPutObject As NXOpen.NXObject = Nothing
            outPutObject = publisherBuilder.Commit()


            Console.WriteLine("## IN2")
            publisherBuilder.Destroy()
            Console.WriteLine("## OUT2")



        Catch ex As Exception
            Console.WriteLine(ex.ToString)
            Dim Path_Exe_Act = Environment.CurrentDirectory()
            Dim timeOfDay As String = String.Format("{0}{1}", Now.TimeOfDay.Hours, Now.TimeOfDay.Minutes)
            Dim Error_File_Name As String = Date_now + "_Error_3DGeneration" + Part_Name_org + "_" + timeOfDay + ".txt"
            Dim Error_File As IO.StreamWriter
            Error_File = My.Computer.FileSystem.OpenTextFileWriter(Path_Exe_Act + System.IO.Path.DirectorySeparatorChar.ToString + Error_File_Name, False)
            Error_File.WriteLine(ex.ToString)
            Error_File.WriteLine(Part_Folder_Path + Part_Name_org + Part_Format)
            Error_File.Close()
        End Try

        '# bad but only way to stop code 'System.Environment.Exit(0) not working
        'Dim CurrentProcess = Process.GetCurrentProcess()
        'CurrentProcess.Kill()
        Console.WriteLine("## Still IN 2")
    End Sub

End Module
