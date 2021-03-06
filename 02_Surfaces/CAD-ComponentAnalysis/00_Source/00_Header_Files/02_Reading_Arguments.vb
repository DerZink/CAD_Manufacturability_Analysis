Option Strict Off
Imports System
Imports NXOpen
Imports NXOpen.UF
Imports Snap
Imports SharedModule.Public_Variable
Imports SharedModule.Public_Switch

Module Argument

    Public Sub Sub_Reading_Arguments(ByVal args As String())

        Console.WriteLine("## NX SurfaceAnalysis: The following environment variables are passed:")
        Console.WriteLine("Args.Length = " & args.Length.ToString())
        If args.Length = 0 Or args.Length = 1 Then
            Console.WriteLine("## NX SurfaceAnalysis: No commands were given!")
            Part_Folder_Path = "D:\00_Datenbank-Fertigbarkeitsanalyse\test\01_PhysicalData\05015e16-39e5-456c-8ff8-9c453ae2d6ff\"
            Part_Name_org = "00000"
            Part_Format = ".prt"
            Data_Name = "_Surfaces"
            Draft_Mode = True
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
            End If
        Next

    End Sub
End Module


