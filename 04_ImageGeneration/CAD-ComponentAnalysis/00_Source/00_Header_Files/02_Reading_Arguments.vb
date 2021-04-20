Option Strict Off
Imports System
Imports NXOpen
Imports NXOpen.UF
Imports Snap
Imports SharedModule.Public_Variable
Module Arguments

    Public Sub Sub_Reading_Arguments(ByVal args As String())

        Console.WriteLine("## NX Area Analysis: The following environment variables are passed:")
        Console.WriteLine("Args.Length = " & args.Length.ToString())
        If args.Length = 0 Or args.Length = 1 Then
            Console.WriteLine("## NX image creation: No commands were given!")
            Part_Folder_Path = "D:\00_Datenbank-Fertigbarkeitsanalyse\01_PhysicalData\9a8d12dc-02b0-4208-86d3-9bf1d2e7fbb6\00000\"
            Part_Name_org = "00000"
            Part_Format = ".prt"
            Resolution = "1500,1500"
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
            ElseIf args(ii).ToLower().Contains("--resolution=") Then
                Resolution = args(ii).Split("=")(1)
                Console.WriteLine(String.Format("{0}Resolution = {1}", ControlChars.Tab, Resolution.ToString))
            End If
        Next

    End Sub
End Module


