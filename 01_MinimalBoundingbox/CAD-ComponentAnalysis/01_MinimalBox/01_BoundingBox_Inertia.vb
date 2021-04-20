Imports NXOpen
Imports System
Imports NXOpen.UF
Imports NXOpen.UI
Imports NXOpen.Utilities
Imports Math_Net = MathNet.Numerics
Imports SharedModule.Public_Variable
Imports SharedModule.Typ_Transformations
Imports SharedModule.Mod_Boundingbox_General_Func
Module Mod_Boundingbox_HTAS
    Public Function Func_Zink_Randbox_HTAS(ByRef Min_Box() As Vector3d, ByRef COG As Point3d) As Double()
        '# Zink: Minimal edge box based on main axes of inertia
        Dim Edge_1(2) As Double
        Dim Edge_2(2) As Double
        Dim Dirs(2, 2) As Double
        Dim Delta(2) As Double
        Dim Actual_Coordinatesystem_Tag As Tag = NXOpen.Tag.Null

        Dim Unitsystem As Integer
        Dim Body_Tag(0) As NXOpen.Tag
        Body_Tag(0) = Body_act.Tag
        Dim Body_Typ As Integer = 0
        Dim Use_accuracy As Integer = 1
        Dim accuracy(10) As Double
        accuracy(0) = 0.99
        '# Issues of MassProbs:
        Dim Density As Double
        Dim Mass_properties(46) As Double
        Dim Calculated_error(12) As Double

        '# Unitsystem: 1= Inches, 4= Meter
        Unitsystem = 4
        Body_Tag(0) = Body_act.Tag

        '# Control Solid or Sheet
        '# !!!!Error message for body_type = 0 is still missing !!!!
        If Body_act.IsSheetBody = True Then
            Body_Typ = 2
            Density = 0.2
        End If
        If Body_act.IsSolidBody = True Then
            Body_Typ = 1
        End If

        '# Carrying out the body analysis
        theUFSession.Modl.AskMassProps3d(Body_Tag, 1, Body_Typ, Unitsystem, Density, Use_accuracy, accuracy, Mass_properties, Calculated_error)

        '# Read out Workpart Coordinate System (WCS)
        Dim WCS_xaxis As Vector3d
        Dim WCS_yaxis As Vector3d
        Part_act.WCS.CoordinateSystem.GetDirections(WCS_xaxis, WCS_yaxis)
        Dim Origin_WCS As Point3d = Part_act.WCS.Origin()

        Dim WCS_(,) As Double = {{WCS_xaxis.X, WCS_xaxis.Y, WCS_xaxis.Z}, {WCS_yaxis.X, WCS_yaxis.Y, WCS_yaxis.Z}}

        '# Storage of the component volume in mm³
        Output_CSV("Volume_Part") = Mass_properties(1) * (1000 ^ 3)

        '# Transformation of Principal Tracking Axes (HTAS) into Absolute Coordinate System (ACS)
        Dim HTAS_COG_WCS() As Double = {Mass_properties(3), Mass_properties(4), Mass_properties(5)}
        Output_CSV("COG_Body_x") = HTAS_COG_WCS(0) * 1000
        Output_CSV("COG_Body_y") = HTAS_COG_WCS(1) * 1000
        Output_CSV("COG_Body_z") = HTAS_COG_WCS(2) * 1000
        Dim HTAS_xaxis_WCS() As Double = {Mass_properties(22), Mass_properties(23), Mass_properties(24)}
        Dim HTAS_yaxis_WCS() As Double = {Mass_properties(25), Mass_properties(26), Mass_properties(27)}

        Func_Vectortrans_using_ACS(Origin_WCS, WCS_, HTAS_COG_WCS)
        Func_Vectortrans_using_ACS(Origin_WCS, WCS_, HTAS_xaxis_WCS)
        Func_Vectortrans_using_ACS(Origin_WCS, WCS_, HTAS_yaxis_WCS)

        '# Transfer of HTAS body in ACS for coordinate system
        Dim HTAS_COG_ACS As New Point3d(HTAS_COG_WCS(0), HTAS_COG_WCS(1), HTAS_COG_WCS(2))
        COG = HTAS_COG_ACS
        Dim HTAS_xaxis_ACS As New Vector3d(HTAS_xaxis_WCS(0), HTAS_xaxis_WCS(1), HTAS_xaxis_WCS(2))
        Dim HTAS_yaxis_ACS As New Vector3d(HTAS_yaxis_WCS(0), HTAS_yaxis_WCS(1), HTAS_yaxis_WCS(2))
        Dim HTAS_Coordsys_ACS As NXOpen.CartesianCoordinateSystem
        HTAS_Coordsys_ACS = Part_act.CoordinateSystems.CreateCoordinateSystem(HTAS_COG_ACS, HTAS_xaxis_ACS, HTAS_yaxis_ACS)

        '# CrossProduct x/y=z
        Dim HTAS_zaxis_ACS_double(2) As Double
        theUFSession.Vec3.Cross(Func_Vector3d_to_Double(HTAS_xaxis_ACS), Func_Vector3d_to_Double(HTAS_yaxis_ACS), HTAS_zaxis_ACS_double)
        Dim HTAS_zaxis_ACS As Vector3d = Func_Double_to_Vector3d(HTAS_zaxis_ACS_double)
        Min_Box = {HTAS_xaxis_ACS, HTAS_yaxis_ACS, HTAS_zaxis_ACS}

        '# Creation of the smallest possible edge box based on the HTAS in ACS
        theUFSession.Modl.AskBoundingBoxExact(Body_Tag(0), HTAS_Coordsys_ACS.Tag, Edge_1, Dirs, Delta)

        '# Calculation and transfer of the box volume
        Func_Zink_Randbox_HTAS = {Func_Calculate_Box_Volume(Delta), Mass_properties(1) * 10 ^ 9}
    End Function
End Module