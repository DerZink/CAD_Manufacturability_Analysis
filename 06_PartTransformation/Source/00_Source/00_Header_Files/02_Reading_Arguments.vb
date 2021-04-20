Option Strict Off
Imports System
Imports NXOpen
Imports NXOpen.UF
Imports Snap
Imports SharedModule.Typ_Transformations
Module Arguments

    Public Sub Sub_Reading_Arguments(ByVal args As String())

        Console.WriteLine("## NX Area Analysis: The following environment variables are passed:")
        Console.WriteLine("Args.Length = " & args.Length.ToString())
        If args.Length = 0 Or args.Length = 1 Then
            Console.WriteLine("## NX image creation: No commands were given!")
            Dim Path_Database = "D:\00_Datenbank-Fertigbarkeitsanalyse\01_PhysicalData\"
            Part_ID_a = "40d0d1ae-cf08-403f-97c3-c1355f2d13a9_00000"
            Part_ID_b = "5804e17e-1e5a-4ddd-a07a-f8032c994e60_00019"
            Path_Output = Path_Database + "00_PartTransformations\"

            Part_Ending = "_PointCloud.prt"

            Translation_a = New Vector3d(-246.4, 58.2, 12.7)
            Translation_b = New Vector3d(-2.8, 13.7, 11.9)

            Sub_Vector_Common_to_Matrix3x3({0.0, 0.0, 1.0}, {1.0, 0.0, 0.0}, {0.0, 1.0, 0.0}, Rotation_a)
            Sub_Vector_Common_to_Matrix3x3({-0.037, 0.999, 0.016}, {-0.511, -0.033, 0.859}, {0.859, 0.024, 0.511}, Rotation_b)

        End If

        For ii As Integer = 0 To args.Length - 1
            If args(ii).ToLower().Contains("--path_output=") Then
                Path_Output = args(ii).Split("=")(1) + "\"
                Console.WriteLine(String.Format("{0}Path Output = {1}", ControlChars.Tab, Path_Output.ToString))

            ElseIf args(ii).ToLower().Contains("--part_id_a=") Then
                Part_ID_a = args(ii).Split("=")(1)
                Console.WriteLine(String.Format("{0}Part ID a = {1}", ControlChars.Tab, Part_ID_a.ToString))
            ElseIf args(ii).ToLower().Contains("--part_id_b=") Then
                Part_ID_b = args(ii).Split("=")(1)
                Console.WriteLine(String.Format("{0}Part ID b = {1}", ControlChars.Tab, Part_ID_b.ToString))

            ElseIf args(ii).ToLower().Contains("--part_ending=") Then
                Part_Ending = args(ii).Split("=")(1)
                Console.WriteLine(String.Format("{0}Part ID b = {1}", ControlChars.Tab, Part_Ending.ToString))

            ElseIf args(ii).ToLower().Contains("--translation_a=") Then
                Dim Translation_aStr As String = args(ii).Split("=")(1)
                Translation_a = Func_StringToVector3d(Translation_aStr)
                Console.WriteLine(String.Format("{0}Translation a = {1}", ControlChars.Tab, Translation_a.ToString))
            ElseIf args(ii).ToLower().Contains("--translation_b=") Then
                Dim Translation_bStr As String = args(ii).Split("=")(1)
                Translation_b = Func_StringToVector3d(Translation_bStr)
                Console.WriteLine(String.Format("{0}Translation b = {1}", ControlChars.Tab, Translation_b.ToString))

            ElseIf args(ii).ToLower().Contains("--rotation_a=") Then
                Dim Rotation_aStr As String = args(ii).Split("=")(1)
                Rotation_a = Func_StringToMatrix3x3(Rotation_aStr)
                Console.WriteLine(String.Format("{0}Rotation a = {1}", ControlChars.Tab, Rotation_a.ToString))
            ElseIf args(ii).ToLower().Contains("--rotation_b=") Then
                Dim Rotation_bStr As String = args(ii).Split("=")(1)
                Rotation_b = Func_StringToMatrix3x3(Rotation_bStr)
                Console.WriteLine(String.Format("{0}Rotation b = {1}", ControlChars.Tab, Rotation_b.ToString))
            End If
        Next

    End Sub

    Private Function Func_StringToVector3d(ByVal VecString As String) As Vector3d
        Dim valueList As New List(Of Double)
        For Each strValue As String In VecString.Split(",")
            Dim value As Double = Nothing
            Double.TryParse(
                    strValue, Globalization.NumberStyles.Any, New Globalization.CultureInfo("en-US"), value)
            valueList.Add(value)
        Next
        Func_StringToVector3d = Func_Double_to_Vector3d(valueList.ToArray())
    End Function

    Private Function Func_StringToMatrix3x3(ByVal MatrixString As String) As Matrix3x3
        Dim vectorsList As New List(Of Double())
        Dim vectorList As New List(Of Double)
        For Each strValue As String In MatrixString.Split(",")
            Dim value As Double = Nothing
            Double.TryParse(
                    strValue, Globalization.NumberStyles.Any, New Globalization.CultureInfo("en-US"), value)
            vectorList.Add(value)
            If vectorList.Count = 3 Then
                vectorsList.Add(vectorList.ToArray())
                vectorList.Clear()
            End If
        Next
        Sub_Vector_Common_to_Matrix3x3(vectorsList(0), vectorsList(1), vectorsList(2), Func_StringToMatrix3x3)
    End Function

End Module


