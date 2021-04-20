Imports NXOpen
Imports NXOpen.UF
Imports System.Math
Imports System.Data
Imports Snap
Imports SharedModule.Public_Variable
Imports SharedModule.NX_Functions

Module Modul_NXSurfacesfunctions

    Public Sub Sub_Surface_Analysis(ByVal Flaechen_tag As Tag)
        '# AskFaceData Dims:
        Dim Radius, Rad_Data, Norm_Dir, Point(0 To 2), dir(0 To 2), box(0 To 5) As Double
        Dim SurfaceTyp As Integer = Nothing
        '# AskFaceEdge Dims:
        Dim Edgelist() As Tag = Nothing
        '# AskFaceProbs Dims:
        Dim P_Point(0 To 2), u1(0 To 2), u2(0 To 2), v1(0 To 2), v2(0 To 2), P_Norm(0 To 2), radii(0 To 1), uv(1), uv_Open_SurfacesPoint(2) As Double

        theUFSession.Modl.AskFaceData(Flaechen_tag, SurfaceTyp, Point, dir, box, Radius, Rad_Data, Norm_Dir)
        If SurfaceTyp = 23 Or SurfaceTyp = 67 Then
            SurfaceTyp = 22
        End If

        'Surfaces_Colors(Flaechen_tag, SurfaceTyp)
        theUFSession.Modl.AskFaceParm2(Flaechen_tag, Point, uv, uv_Open_SurfacesPoint)

        Surfaces_NX_Data_Dict.Type._Entry(Flaechen_tag, SurfaceTyp)
        Dim Typ_fuer_Dict As String = String.Format("nx_{0}", SurfaceTyp)
        Distribution_NX_Surfaces_body(Typ_fuer_Dict) += 1
        Distribution_NX_Surfaces_Body_based(Typ_fuer_Dict) += Surfaces_NX_Data_Dict.Surfacecontents._ValueOutput(Flaechen_tag)
        Number_of_NX_Surfaces += 1
        Surfaces_NX_Data_Dict.Point._Entry(Flaechen_tag, Point)
        Surfaces_NX_Data_Dict.Dir._Entry(Flaechen_tag, dir)
        Surfaces_NX_Data_Dict.Radius._Entry(Flaechen_tag, Radius)
        Surfaces_NX_Data_Dict.Raidus_data._Entry(Flaechen_tag, Rad_Data)
        Surfaces_NX_Data_Dict.Norm_Dir._Entry(Flaechen_tag, Norm_Dir)
        Surfaces_NX_Data_Dict.uv._Entry(Flaechen_tag, uv)

        Table_Output_NX.Filling_AskData(SurfaceTyp, Point(0), Point(1), Point(2), dir(0), dir(1), dir(2),
                                         Radius, Rad_Data, Norm_Dir, uv(0), uv(1))
        theUFSession.Modl.AskFaceEdges(Flaechen_tag, Edgelist)
        Surfaces_NX_Data_Dict.Edge._Entry(Flaechen_tag, Edgelist)

        theUFSession.Modl.AskFaceProps(Flaechen_tag, uv, P_Point, u1, v1, u2, v2, P_Norm, radii)
        Surfaces_NX_Data_Dict.P_Point._Entry(Flaechen_tag, P_Point)
        Surfaces_NX_Data_Dict.u1._Entry(Flaechen_tag, v1)
        Surfaces_NX_Data_Dict.v1._Entry(Flaechen_tag, u1)
        Surfaces_NX_Data_Dict.u2._Entry(Flaechen_tag, u2)
        Surfaces_NX_Data_Dict.v2._Entry(Flaechen_tag, v2)
        Surfaces_NX_Data_Dict.P_Norm._Entry(Flaechen_tag, P_Norm)
        Surfaces_NX_Data_Dict.P_Radius._Entry(Flaechen_tag, radii)

        Table_Output_NX.Filling_AskProbs(P_Point(0), P_Point(1), P_Point(2),
                                          u1(0), u1(1), u1(2),
                                          v1(0), v1(1), v1(2),
                                          u2(0), u2(1), u2(2),
                                          v2(0), v2(1), v2(2),
                                          P_Norm(0), P_Norm(1), P_Norm(2),
                                          radii(0), radii(1))

    End Sub

    Public Sub Surfaces_Colors(ByVal _Tag As Tag, ByVal _Typ As Integer)
        Dim Color As Integer
        If _Typ = 16 Then
            Color = 103 'blue
            Sub_Color(_Tag, Color)
        ElseIf _Typ = 17 Then
            Color = 17
            Sub_Color(_Tag, Color)
        ElseIf _Typ = 18 Then
            Color = 6 'yellow
            Sub_Color(_Tag, Color)
        ElseIf _Typ = 19 Then
            Color = 19
            Sub_Color(_Tag, Color)
        ElseIf _Typ = 20 Then
            Color = 20
            Sub_Color(_Tag, Color)
        ElseIf _Typ = 22 Then
            Color = 36 'green
            Sub_Color(_Tag, Color)
        ElseIf _Typ = 23 Then
            Color = 23
            Sub_Color(_Tag, Color)
        ElseIf _Typ = 43 Then
            Color = 186 'red
            Sub_Color(_Tag, Color)
        ElseIf _Typ = 65 Then
            Color = 65
            Sub_Color(_Tag, Color)
        ElseIf _Typ = 66 Then
            Color = 66
            Sub_Color(_Tag, Color)
        End If
    End Sub
End Module
