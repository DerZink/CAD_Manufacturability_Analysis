Imports NXOpen
Imports System
Imports NXOpen.UF
Imports NXOpen.UI
Imports NXOpen.Utilities
Imports Math_Net = MathNet.Numerics
Imports SharedModule.Public_Variable
Imports SharedModule.Typ_Transformations
Imports SharedModule.Declaration_Tables
Imports SharedModule.Mod_Boundingbox_General_Func

Module Mod_Create_Minimum_Boundingbox

    Public Sub Sub_Create_Minimum_Boundingbox()

        '# Use public variable Body_act and
        Dim Min_Box(2) As Vector3d '# rotation axes of the minimum box
        Dim Vol_Box_min As Double   '# Volume of the minimum box
        Dim Part_MainFocus As Point3d = Nothing
        Dim Volume_HTAS(1) As Double
        Dim Duration_HTAS As Double
        Dim Difference_Volume_HTAS_Part As Double
        Dim Volume_Gen As Double = 0.0
        Dim Duration_Gen As Double = 0.0
        Dim Box_HTAS(2) As Vector3d

        '# Determination of the minimum box along the main axis of gravity
        Dim Dauer_1 As Double = Timer()
        Volume_HTAS = Func_Zink_Randbox_HTAS(Min_Box, Part_MainFocus)
        Duration_HTAS = Timer() - Dauer_1
        Difference_Volume_HTAS_Part = Volume_HTAS(0) - Volume_HTAS(1)
        Vol_Box_min = Volume_HTAS(0)
        Box_HTAS = Min_Box

        '# Determine the minimum box with genetic algorithm if main axis box is not good enough.
        If Not Math.Abs(Difference_Volume_HTAS_Part) <= 1.0 Then
            Dim Duration_2 As Double = Timer()
            Volume_Gen = Func_Zink_Boundingbox_genetic(Min_Box)
            Duration_Gen = Timer() - Duration_2
        End If
        If Volume_Gen < Vol_Box_min And Volume_Gen <> 0.0 And Math.Abs(Volume_Gen - Vol_Box_min) >= 1.0 Then
            Vol_Box_min = Volume_Gen
        Else
            Min_Box = Box_HTAS
        End If

        Console.WriteLine(String.Format("## Minimum_Boundingbox: Duration Create the border box HTAS = {0} s, Genetic = {1} s", Duration_HTAS, Duration_Gen))
        Output_CSV("Volume_Box") = Vol_Box_min
        '# Create the minimal box

        Sub_Box_Boundingpoints_Create(Min_Box(0), Min_Box(1), True)

        '# Align the part coordinate system to the minimum box coordinate system
        Dim WCS_Min_Box_Matrix As Matrix3x3
        Sub_Vector_Common_to_Matrix3x3(Min_Box(0), Min_Box(1), Min_Box(2), WCS_Min_Box_Matrix)
        Part_act.WCS.SetOriginAndMatrix(Part_MainFocus, WCS_Min_Box_Matrix)

        '# CSV-Output:
        Dim CSV_Output As New CSV_Output_BoundingBox
        CSV_Output.Entries_definition()
        CSV_Output.Filling(Output_CSV("Dim_1"), Output_CSV("Dim_2"), Output_CSV("Dim_3"), Output_CSV("Volume_Part"),
                             Output_CSV("Volume_Box"), Output_CSV("Coordinate_P1_x"), Output_CSV("Coordinate_P1_y"),
                             Output_CSV("Coordinate_P1_z"), Output_CSV("Coordinate_P2_x"), Output_CSV("Coordinate_P2_y"),
                             Output_CSV("Coordinate_P2_z"), Output_CSV("Orientation_1_x"), Output_CSV("Orientation_1_y"),
                             Output_CSV("Orientation_1_z"), Output_CSV("Orientation_2_x"), Output_CSV("Orientation_2_y"),
                             Output_CSV("Orientation_2_z"), Output_CSV("Orientation_3_x"), Output_CSV("Orientation_3_y"),
                             Output_CSV("Orientation_3_z"), Output_CSV("COG_Body_x"),
                             Output_CSV("COG_Body_y"), Output_CSV("COG_Body_z"), Date_now)
        CSV_Output.Output()


    End Sub

End Module