Option Strict Off
Imports System
Imports System.Drawing
Imports NXOpen
Imports System.Collections.Generic
Imports System.ComponentModel
Imports System.Data
Imports System.Text
Imports NXOpen.UF
Imports Snap
Imports System.Windows.Forms
Imports SharedModule.Public_Variable
Imports SharedModule.Capture_Assembly

Module Source

    Public Sub Main(ByVal args As String())

        Try
            Console.WriteLine("## NX image creation")
            Sub_Reading_Arguments(args)
            Dim Status_Start As New UFPart.LoadStatus
            Dim Tag_Start As New Tag '= Nothing
            Dim File = Part_Folder_Path + Part_Name_org + Part_Format
            theUFSession.Part.Open(File, Tag_Start, Status_Start)
            Part_act = Utilities.NXObjectManager.Get(Tag_Start)
            Dim PartLoadStatus1 As PartLoadStatus = Nothing
            Console.WriteLine("FILE NAME" + File)
            '# Defines Workpart without representing it individually
            'theSession.Parts.SetWork(Part_act)
            '# Defines Workpart and displays it individually
            theSession.Parts.SetDisplay(Part_act, False, False, PartLoadStatus1)
            PartLoadStatus1.Dispose()

            Dim Work_Part As Part = theSession.Parts.Work
            Dim strPartJpg As String = ""

            '# Selected views
            Dim Selected_views(3) As NXOpen.View.Canned
            Selected_views(0) = NXOpen.View.Canned.Top
            Selected_views(1) = NXOpen.View.Canned.Trimetric
            Selected_views(2) = NXOpen.View.Canned.Left
            Selected_views(3) = NXOpen.View.Canned.Right

            Dim options As New UFDisp.ShadeOptions

            options.disable_raytracing = True
            options.distribute_excess_light = True
            options.facet_quality = 1
            options.resolution = 300
            options.plot_quality = UFDisp.ShadePlot.PlotMedium

            options.generate_shadows = False
            options.transparent_shadows = False
            options.fixed_camera_viewing = False
            options.super_sample = 3
            options.raytrace_memory = 128
            options.subdivision_depth = 6
            options.radiosity_quality = 15
            options.distribute_excess_light = False
            options.use_midpoint_sampling = True
            options.format = UFDisp.ShadeFormat.FormatRaster
            options.display = UFDisp.ShadeDisplay.DisplayNearestRgb

            Dim objects1 As NXOpen.IFitTo() = Nothing
            Dim body_lists As New List(Of NXOpen.Body)
            For Each body In Work_Part.Bodies
                body_lists.Add(body)
            Next
            objects1 = body_lists.ToArray

            Dim x_gr = CInt(Resolution.Split(",")(0))
            Dim y_gr = CInt(Resolution.Split(",")(1))

            For Each Single_View In Selected_views
                Work_Part.Views.WorkView.Orient(Single_View, NXOpen.View.ScaleAdjustment.Fit)
                Work_Part.ModelingViews.WorkView.FitToObjects(objects1)
                strPartJpg = Part_Folder_Path & Part_Name_org & "_" & Single_View.ToString() & ".jpg"
                theUFSession.Disp.BatchShadeOptions(strPartJpg, x_gr, y_gr, UFDisp.ShadeMethod.Preview, options)
                'theUFSession.Disp.CreateFramedImage(strPartJpg,
                '                                    UFDisp.ImageFormat.Png, UFDisp.BackgroundColor.White,
                '                                    {0, 0}, x_gr, y_gr)
            Next

        Catch ex As Exception
            Console.WriteLine(ex.ToString)
            Dim Path_Exe_Act = Environment.CurrentDirectory()
            Dim timeOfDay As String = String.Format("{0}{1}", Now.TimeOfDay.Hours, Now.TimeOfDay.Minutes)
            Dim Error_File_Name As String = Date_now + "_Error_ImageGeneration" + Part_Name_org + "_" + timeOfDay + ".txt"
            Dim Error_File As IO.StreamWriter
            Error_File = My.Computer.FileSystem.OpenTextFileWriter(Path_Exe_Act + System.IO.Path.DirectorySeparatorChar.ToString + Error_File_Name, False)
            Error_File.WriteLine(ex.ToString)
            Error_File.WriteLine(Part_Folder_Path + Part_Name_org + Part_Format)
            Error_File.Close()
        End Try

    End Sub
End Module


