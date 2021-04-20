
Imports NXOpen
Imports NXOpen.UF
Imports System.Math
Imports System.Data
Imports SharedModule.Public_Variable
Imports SharedModule.Public_Switch
Imports SharedModule.File_Management
Imports SharedModule.NX_Functions

Module Mod_Individual_SurfacesAnalysis

    '# Neighbouring determine
    '###########################################################################
    Public Sub Neighbouring(ByVal _Tag As Tag, ByRef _Neighbouring_Surface As List(Of Tag), ByVal _Analysing_Surfaces As HashSet(Of Tag))

        'Dim st As Integer = 0
        Dim Surfaces_ID_NeighbouringAnalysis = Surfaces_Merged_Data_Dict.Max_ID

        Dim Related_Surfaces As New List(Of Tag)
        Related_Surfaces.Clear()

        '# Analysis of the neighbor relationship between surfaces
        '# Incl. Check if surfaces have even flat neighbors, which still have to be calculated.
        Dim Surfaces_completely_connected = Func_Angular_Relationship_AdjacentSurfaces(_Tag, _Neighbouring_Surface, _Analysing_Surfaces, Related_Surfaces)

        If Surfaces_completely_connected = True Then
            Surfaces_Merged_Data_Dict.Neighbour_Tags._Entry(Surfaces_ID_NeighbouringAnalysis, Related_Surfaces)
            Sub_Surfaces_Data(Surfaces_ID_NeighbouringAnalysis)

            '# All surfaces analyzed:
            If _Analysing_Surfaces.Count = 0 Then
                Sub_determine_the_neighbour_place(Surfaces_ID_NeighbouringAnalysis)
                '# Add last entry in Table_Output_NX
                Table_Output_NX.Table_Columns_NX.Rows.Add(Table_Output_NX.Filling_temp)
            End If

            Sub_Surfaces_Color(Surfaces_ID_NeighbouringAnalysis)
            Surfaces_Merged_Data_Dict.Max_ID += 1

        End If

    End Sub

    Private Sub Sub_Surfaces_Data(ByVal _Surfaces_ID As Integer)
        Dim Related_Surfaces As List(Of Tag) = Surfaces_Merged_Data_Dict.Neighbour_Tags._ValueOutput(_Surfaces_ID)
        Dim Number_of_Convex As Integer = 0
        Dim Number_of_Concave As Integer = 0
        Dim SurfacesContent As Double = 0
        For Each Surface In Related_Surfaces
            Number_of_Convex += Surfaces_NX_Data_Dict.Number_Of_Convex._ValueOutput(Surface)
            Number_of_Concave += Surfaces_NX_Data_Dict.number_of_Concave._ValueOutput(Surface)
            SurfacesContent += Surfaces_NX_Data_Dict.Surfacecontents._ValueOutput(Surface)
        Next
        Surfaces_Merged_Data_Dict.Number_Of_Convex._Entry(_Surfaces_ID, Number_of_Convex)
        Surfaces_Merged_Data_Dict.number_of_Concave._Entry(_Surfaces_ID, Number_of_Concave)
        Surfaces_Merged_Data_Dict.Surfacecontents._Entry(_Surfaces_ID, SurfacesContent)
    End Sub
    Private Sub Sub_Surfaces_Color(ByVal _Surfaces_ID As Integer)
        Dim Number_of_Convex As Integer = Surfaces_Merged_Data_Dict.Number_Of_Convex._ValueOutput(_Surfaces_ID)
        Dim Number_of_Concave As Integer = Surfaces_Merged_Data_Dict.number_of_Concave._ValueOutput(_Surfaces_ID)
        Dim Surfaces As List(Of Tag) = Surfaces_Merged_Data_Dict.Neighbour_Tags._ValueOutput(_Surfaces_ID)
        Dim Color As Integer = 1

        If Coloring_of_combined_surfaces Then
            If Surfaces.Count > 1 Then
                Color = CInt(Math.Ceiling(Rnd() * 215)) + 1
            End If
            For Each Surface In Surfaces
                Sub_Color(Surface, Color)
            Next
            '# Alle Surfaces analyzed = Neighbouring._DictOutput.Count <> 0
            If Surfaces_Merged_Data_Dict.Neighbours._DictOutput.Count <> 0 Then
                Dim myOptions As UFPart.ExportOptions
                myOptions.params_mode = UFPart.ExportParamsMode.RemoveParams
                myOptions.new_part = True
                Dim Name As String = Part_Folder_Path + Part_Name_org + Data_Name + "_Connected.prt"
                Sub_Delete_Existing_Files(Name)
                Dim BodyTag(0) As Tag
                BodyTag(0) = Body_act.Tag
                theUFSession.Part.ExportWithOptions(Name, 1, BodyTag, myOptions)
            End If

        End If

        '# All Surfaces analysed = Neighbouring._DictOutput.Count <> 0
        If ColorBy_type_of_surface And Surfaces_Merged_Data_Dict.Neighbours._DictOutput.Count <> 0 Then
            Table_Output_Neighbour.Entries_Definition()
            Dim Neighbour_dict = Surfaces_Merged_Data_Dict.Neighbours._DictOutput
            For Each Surface_connected In Neighbour_dict
                If Surface_connected.Value = "mainsurface" Then
                    Color = 123 '# gray 
                ElseIf Surface_connected.Value = "transitionsurface" Then
                    Color = 75 '# light red
                ElseIf Surface_connected.Value = "featuresurface_concave" Then
                    Color = 91 '# light green
                ElseIf Surface_connected.Value = "featuresurface_convex" Then
                    Color = 18 '# light yellow
                End If
                For Each Surface In Surfaces_Merged_Data_Dict.Neighbour_Tags._ValueOutput(Surface_connected.Key)
                    Sub_Color(Surface, Color)
                    Sub_Describe_TablesExchange_NX(Surface, Surface_connected.Value)
                Next
                Sub_Describe_Table_Output_Neighbour(Surface_connected.Key)
            Next
            Dim myOptions As UFPart.ExportOptions
            myOptions.params_mode = UFPart.ExportParamsMode.MaintainAllParams
            myOptions.new_part = True
            Dim Name As String = Part_Folder_Path + Part_Name_org + Data_Name + "_NeighborTypes.prt"
            Sub_Delete_Existing_Files(Name)
            Dim BodyTag(0) As Tag
            BodyTag(0) = Body_act.Tag
            theUFSession.Part.ExportWithOptions(Name, 1, BodyTag, myOptions)
        End If
    End Sub
    Private Sub Sub_determine_the_neighbour_place(ByVal _Surfaces_ID As Integer)
        Dim SurfacesContent = Surfaces_Merged_Data_Dict.Surfacecontents._DictOutput()
        Dim SurfacesContent_sorted = SurfacesContent.OrderByDescending(Function(x) x.Value).ToList
        Dim SurfacesContent_max As Double = SurfacesContent_sorted(0).Value

        For Each Surface In SurfacesContent_sorted
            If Surface.Value >= 0.7 * SurfacesContent_max Then
                Surfaces_Merged_Data_Dict.Neighbours._Entry(Surface.Key, "mainsurface")
                Distribution_classification_surfaces_body("mainsurface") += 1
                Distribution_Arrangement_Surfaces_Body_based("mainsurface") += Surfaces_Merged_Data_Dict.Surfacecontents._ValueOutput(Surface.Key)
            ElseIf Surfaces_Merged_Data_Dict.Number_Of_Convex._ValueOutput(Surface.Key) <> 0 And Surfaces_Merged_Data_Dict.number_of_Concave._ValueOutput(Surface.Key) <> 0 Then
                Surfaces_Merged_Data_Dict.Neighbours._Entry(Surface.Key, "transitionsurface")
                Distribution_classification_surfaces_body("transitionsurface") += 1
                Distribution_Arrangement_Surfaces_Body_based("transitionsurface") += Surfaces_Merged_Data_Dict.Surfacecontents._ValueOutput(Surface.Key)
            ElseIf Surfaces_Merged_Data_Dict.Number_Of_Convex._ValueOutput(Surface.Key) = 0 Then
                Surfaces_Merged_Data_Dict.Neighbours._Entry(Surface.Key, "featuresurface_concave")
                Distribution_classification_surfaces_body("featuresurface_concave") += 1
                Distribution_Arrangement_Surfaces_Body_based("featuresurface_concave") += Surfaces_Merged_Data_Dict.Surfacecontents._ValueOutput(Surface.Key)
            ElseIf Surfaces_Merged_Data_Dict.number_of_Concave._ValueOutput(Surface.Key) = 0 Then
                Surfaces_Merged_Data_Dict.Neighbours._Entry(Surface.Key, "featuresurface_convex")
                Distribution_classification_surfaces_body("featuresurface_convex") += 1
                Distribution_Arrangement_Surfaces_Body_based("featuresurface_convex") += Surfaces_Merged_Data_Dict.Surfacecontents._ValueOutput(Surface.Key)
            End If
            TotalSurfaces += Surfaces_Merged_Data_Dict.Surfacecontents._ValueOutput(Surface.Key)
            Number_of_classification_surfaces += 1
        Next

    End Sub
    Private Sub Sub_Describe_TablesExchange_NX(ByVal _Tag As Integer, ByVal _Neighbour_type As String)
        '# Table_Output_NX befuellen
        Dim Line_in_table_Output_NX = Table_Output_NX.Table_Columns_NX.Select("tag = '" & _Tag & "'")
        Line_in_table_Output_NX(0).Item("number_of_convex") = Surfaces_NX_Data_Dict.Number_Of_Convex._ValueOutput(_Tag)
        Line_in_table_Output_NX(0).Item("number_of_concave") = Surfaces_NX_Data_Dict.number_of_Concave._ValueOutput(_Tag)
        Line_in_table_Output_NX(0).Item("number_of_plane") = Surfaces_NX_Data_Dict.NumberOf_Plane._ValueOutput(_Tag)
        Line_in_table_Output_NX(0).Item("neighbour_type") = _Neighbour_type
    End Sub
    Private Sub Sub_Describe_Table_Output_Neighbour(ByVal ID As Integer)
        Dim Tags_of_the_Surfaces As List(Of Tag) = Surfaces_Merged_Data_Dict.Neighbour_Tags._ValueOutput(ID)
        Dim Tags_of_the_Surfaces_String As String = String.Join(",", Tags_of_the_Surfaces.ToArray)
        Dim SurfacesContent As Double = Surfaces_Merged_Data_Dict.Surfacecontents._ValueOutput(ID)
        Dim Number_of_Convex As Integer = Surfaces_Merged_Data_Dict.Number_Of_Convex._ValueOutput(ID)
        Dim Number_of_Concave As Integer = Surfaces_Merged_Data_Dict.number_of_Concave._ValueOutput(ID)
        Dim Neighbouring As String = Surfaces_Merged_Data_Dict.Neighbours._ValueOutput(ID)
        Table_Output_Neighbour.Filling(ID, Tags_of_the_Surfaces_String, SurfacesContent, Number_of_Convex, Number_of_Concave, Neighbouring)
    End Sub
End Module