Option Strict Off
Imports System
Imports NXOpen
Imports NXOpen.UF
Imports Snap
Imports SharedModule.Public_Variable

Module Argumente

    Public Sub Sub_Reading_Arguments(ByVal args As String())

        Console.WriteLine("## NX Area Analysis: The following environment variables are passed:")
        Console.WriteLine(ControlChars.Tab & "Args.Length = " & args.Length.ToString())
        If args.Length = 0 Or args.Length = 1 Then
            Console.WriteLine("## NX Area Analysis: No commands were given!")
            Part_Folder_Path = "D:\04_Arbeitsordner_lokal_sync\00_Diss\03_Python\timeComplexity\Results\BenchAquisition\PartsRaw\"
            Part_Name_org = "0000"
            Part_Format = ".prt"
            Part_ID = "11111"
            Output_Path_Part = "D:\04_Arbeitsordner_lokal_sync\00_Diss\03_Python\timeComplexity\Results\BenchAquisition\PartsRaw\"
        End If

        For ii As Integer = 0 To args.Length - 1
            'Console.WriteLine("args(" & ii.ToString & ") = " & args(ii))
            If args(ii).ToLower().Contains("--part_path=") Then
                Part_Folder_Path = args(ii).Split("=")(1) + "\"
                Console.WriteLine(String.Format("{0}Part Path = {1}", ControlChars.Tab, Part_Folder_Path.ToString))
            ElseIf args(ii).ToLower().Contains("--part_name=") Then
                Part_Name_org = args(ii).Split("=")(1)
                Console.WriteLine(String.Format("{0}Part Name = {1}", ControlChars.Tab, Part_Name_org.ToString))
            ElseIf args(ii).ToLower().Contains("--part_format=") Then
                Part_Format = args(ii).Split("=")(1)
                Console.WriteLine(String.Format("{0}Part Format = {1}", ControlChars.Tab, Part_Format.ToString))
            ElseIf args(ii).ToLower().Contains("--part_id=") Then
                Part_ID = args(ii).Split("=")(1)
                Console.WriteLine(String.Format("{0}Part ID = {1}", ControlChars.Tab, Part_ID.ToString))
            ElseIf args(ii).ToLower().Contains("--output_path_part=") Then
                Output_Path_Part = args(ii).Split("=")(1)
                Console.WriteLine(String.Format("{0}Output Part Path = {1}", ControlChars.Tab, Output_Path_Part.ToString))
            End If
        Next

        If Not My.Computer.FileSystem.DirectoryExists(Output_Path_Part) Then
            My.Computer.FileSystem.CreateDirectory(Output_Path_Part)
        End If


    End Sub
End Module


