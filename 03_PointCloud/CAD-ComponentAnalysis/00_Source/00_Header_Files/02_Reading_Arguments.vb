Option Strict Off
Imports System
Imports NXOpen
Imports NXOpen.UF
Imports SharedModule.Public_Variable

Module Argument

    Public Sub Sub_Reading_Arguments(ByVal args As String())

        Console.WriteLine("## Corruption data: The following environment variables are transferred:")
        Console.WriteLine("Args.Length = " & args.Length.ToString())
        If args.Length = 0 Or args.Length = 1 Then
            Console.WriteLine("## NX Curvature data: No commands were given!")
            Part_Folder_Path = "D:\04_Arbeitsordner_lokal_sync\00_Diss\03_Python\timeComplexity\Results\BenchAquisition\01_PhysicalData\0001\00000\"
            Part_Name_org = "00000"
            Part_Format = ".prt"
            Data_Name = "_PointCloud_test"
            Draft_Mode = True
            BoxDir_1 = New Vector3d(0.845835, 0.533445, 0)
            BoxDir_2 = New Vector3d(-0.533445, 0.845835, 0)
            NumberOfPoints = 100000
            DiscretizationStep = 2
        End If

        For ii As Integer = 0 To args.Length - 1
            'Console.WriteLine("args(" & ii.ToString & ") = " & args(ii))
            If args(ii).ToLower().Contains("--part_path=") Then
                Part_Folder_Path = args(ii).Split("=")(1) + "/"
                Console.WriteLine(String.Format("{0}Part path = {1}", ControlChars.Tab, Part_Folder_Path.ToString))
            ElseIf args(ii).ToLower().Contains("--part_name=") Then
                Part_Name_org = args(ii).Split("=")(1)
                Console.WriteLine(String.Format("{0}Part Name = {1}", ControlChars.Tab, Part_Name_org.ToString))
            ElseIf args(ii).ToLower().Contains("--part_format=") Then
                Part_Format = args(ii).Split("=")(1)
                Console.WriteLine(String.Format("{0}Part Format = {1}", ControlChars.Tab, Part_Format.ToString))
            ElseIf args(ii).ToLower().Contains("--data_name=") Then
                Data_Name = args(ii).Split("=")(1)
                Console.WriteLine(String.Format("{0}Data Name = {1}", ControlChars.Tab, Data_Name.ToString))
            ElseIf args(ii).ToLower().Contains("--draft_mode=") Then
                Dim Draft_Mode_str As String = args(ii).Split("=")(1)
                If (Draft_Mode_str = "True") Then
                    Draft_Mode = True
                Else
                    Draft_Mode = False
                End If
                Console.WriteLine(String.Format("{0}Draft Mode = {1}", ControlChars.Tab, Draft_Mode.ToString))
            ElseIf args(ii).ToLower().Contains("--discretization=") Then
                Dim Discretization_distance_str As String = args(ii).Split("=")(1)
                Double.TryParse(
                    Discretization_distance_str, Globalization.NumberStyles.Any, New Globalization.CultureInfo("en-US"), DiscretizationStep)
                Console.WriteLine(String.Format("{0}Data Name = {1}", ControlChars.Tab, DiscretizationStep.ToString))
            ElseIf args(ii).ToLower().Contains("--number_of_points=") Then
                Dim NumberOfPoints_str As String = args(ii).Split("=")(1)
                Double.TryParse(
                    NumberOfPoints_str, Globalization.NumberStyles.Any, New Globalization.CultureInfo("en-US"), NumberOfPoints)
                Console.WriteLine(String.Format("{0}Data Name = {1}", ControlChars.Tab, NumberOfPoints.ToString))
            End If
        Next

        If args.Length >= 1 Then
            Sub_readIn_Boxdirs()
        End If

    End Sub

    Private Sub Sub_readIn_Boxdirs()
        Dim File_Path_Name As String = Part_Folder_Path + Part_Name_org + "_MinimalBoundingBox.csv"
        Dim CSV_File As IO.StreamReader
        CSV_File = My.Computer.FileSystem.OpenTextFileReader(File_Path_Name)

        Dim Pos_dir1 As Integer = 0
        Dim Name_dir1 As String = "orientation_1_x"
        Dim lineCount As Integer = 0

        While (CSV_File.Peek() >= 0)
            Dim line As String = CSV_File.ReadLine()
            Dim line_array As String() = line.Split(";")
            If (lineCount = 0) Then
                Dim pos_line As Integer = 0
                For Each column In line_array
                    If column.Equals(Name_dir1) Then
                        Pos_dir1 = pos_line
                        Exit For
                    End If
                    pos_line += 1
                Next
            Else
                Dim dirs_1 As New List(Of Double)
                Dim dirs_2 As New List(Of Double)
                For pos_1 As Integer = Pos_dir1 To Pos_dir1 + 2 Step 1
                    Dim dir_str1 As String = line_array(pos_1)
                    Dim dir_dbl1 As Double = Nothing
                    Double.TryParse(dir_str1, Globalization.NumberStyles.Any, New Globalization.CultureInfo("en-US"), dir_dbl1)
                    dirs_1.Add(dir_dbl1)
                    Dim dir_str2 As String = line_array(pos_1 + 3)
                    Dim dir_dbl2 As Double = Nothing
                    Double.TryParse(dir_str2, Globalization.NumberStyles.Any, New Globalization.CultureInfo("en-US"), dir_dbl2)
                    dirs_2.Add(dir_dbl2)
                Next
                BoxDir_1 = New Vector3d(dirs_1(0), dirs_1(1), dirs_1(2))
                BoxDir_2 = New Vector3d(dirs_2(0), dirs_2(1), dirs_2(2))
                Exit While
            End If

            lineCount += 1
        End While

    End Sub
End Module


