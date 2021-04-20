Imports NXOpen
Imports NXOpen.UF
Imports System.Math
Imports System.Data
Imports SharedModule.Public_Variable
Imports SharedModule.Public_Switch
Imports SharedModule.File_Management
Imports SharedModule.NX_Functions

Module Mod_Readingout_Part_Surface

    '# Data Reading
    '###########################################################################
    Public Sub Sub_Part_Surface_Data()

        '# Tables for storing the NX surface data
        Table_Output_NX.Entries_Definition()
        Table_FaceType_Distribution_perNumber.Entries_Definition()
        Table_FaceType_Distribution_perArea.Entries_Definition()
        For Each Categorie In Classification_of_surface_categories
            Distribution_classification_surfaces_body(Categorie) = 0
            Distribution_Arrangement_Surfaces_Body_based(Categorie) = 0
        Next
        For Each Categorie In NX_Surface_Categories
            Distribution_NX_Surfaces_body(Categorie) = 0
            Distribution_NX_Surfaces_Body_based(Categorie) = 0
        Next

        Dim Surfaces_NULL = Body_act.GetFaces(0).Tag
        Dim All_Surfaces_tags As HashSet(Of Tag) = New HashSet(Of Tag)(Array.ConvertAll(Body_act.GetFaces, Function(Flaechen) Flaechen.Tag))
        Dim Number_Of_Surfaces_max = All_Surfaces_tags.Count
        Dim Switch_Surfaces_Analysis = True
        Dim Surfaces_act As New List(Of Tag)
        Surfaces_act.Add(Surfaces_NULL)

        Console.WriteLine("## NX surface analysis: progress of the surface analysis in percent")

        While Switch_Surfaces_Analysis = True
            Dim Neighbour_Between_List As New List(Of Tag)

            For Each Surface In Surfaces_act
                All_Surfaces_tags.Remove(Surface)
                Dim Neighbour_of_the_Surface As New List(Of Tag)
                '# Calculation of NX surface data
                Surfaces_Analysis_NX(Surface)
                '# Calculation of Surfaces Neighbour
                Neighbouring(Surface, Neighbour_of_the_Surface, All_Surfaces_tags)
                Neighbour_Between_List.AddRange(Neighbour_of_the_Surface)
            Next

            Dim Progress_surface_analysis = CDec((1 - All_Surfaces_tags.Count / Number_Of_Surfaces_max) * 100)
            Console.Write(vbCrLf)
            Console.Write("## nx Surfaces Analysis: " + Progress_surface_analysis.ToString("00.00") & " %")
            Neighbour_Between_List = Neighbour_Between_List.Distinct().ToList
            Neighbour_Between_List = Neighbour_Between_List.Intersect(All_Surfaces_tags).ToList
            Surfaces_act.Clear()
            Surfaces_act.AddRange(Neighbour_Between_List)
            If All_Surfaces_tags.Count = 0 Then
                Switch_Surfaces_Analysis = False
            ElseIf Neighbour_Between_List.Count = 0 Then
                Surfaces_act.Add(All_Surfaces_tags.First())
            End If

        End While


        If Output_of_calculation_normal_in_NX Then
            Dim Surfacesorientation As New List(Of Tag)
            Surfacesorientation.Add(Func_Create_FeatureGroup(List_Correct_SurfacesRelationship.ToArray, "Correct_Surfaces"))
            Surfacesorientation.Add(Func_Create_FeatureGroup(List_Wrong_SurfacesRelationship.ToArray, "Wrong_Surfaces"))
            Sub_Create_FeatureGroup(Surfacesorientation.ToArray, "Surfacesorientation")
        End If

        '# Color all surfaces to NX Type
        For Each Surface In Body_act.GetFaces()
            Surfaces_Colors(Surface.Tag, Surfaces_NX_Data_Dict.Type._ValueOutput(Surface.Tag))
        Next
        Dim Name As String = Part_Folder_Path + Part_Name_org + Data_Name + "_NX.prt"
        Sub_Delete_Existing_Files(Name)
        Dim PartsSaveStatus As PartSaveStatus = Nothing
        Dim Output_Part As Part = theSession.Parts.Display
        PartsSaveStatus = Output_Part.SaveAs(Name)

        Table_Output_NX.Sorting()
        Table_Output_NX.Output()
        Table_Output_Neighbour.Sorting()
        Table_Output_Neighbour.Output()
        Table_FaceType_Distribution_perNumber.Filling(Distribution_classification_surfaces_body,
                                                      Number_of_classification_surfaces,
                                                      Distribution_NX_Surfaces_body,
                                                      Number_of_NX_Surfaces)
        Table_FaceType_Distribution_perArea.Filling(Distribution_Arrangement_Surfaces_Body_based,
                                                    Distribution_NX_Surfaces_Body_based,
                                                    TotalSurfaces)

        Table_FaceType_Distribution_perNumber.Output()
        Table_FaceType_Distribution_perArea.Output()
    End Sub

    Friend Sub Surfaces_Analysis_NX(ByVal _Tag As Tag)
        Dim Status As Boolean
        If Surfaces_NX_Data_Dict.Surfacecontents._DictOutput.Count = 0 Then
            Status = False
        Else
            Status = Surfaces_NX_Data_Dict.Surfacecontents._DictOutput.ContainsKey(_Tag)
        End If

        If Not Status Then
            Dim Index = Surfaces_NX_Data_Dict.Surfacecontents._DictOutput.Count()
            '# Create the data line
            Table_Output_NX.Create_Line(Index)
            '# General surface data
            Dim Surface_ID = Func_NX_ID_ReadingOut(_Tag)
            Surfaces_NX_Data_Dict.NXID._Entry(_Tag, Surface_ID)
            Dim Surface_contents = Func_Surface_contents(_Tag)
            Surfaces_NX_Data_Dict.Surfacecontents._Entry(_Tag, Surface_contents)
            '# Analysis of the surfaces with the help of NX functions
            Sub_Surface_Analysis(_Tag)
            '# Determine neighboring surfaces
            Dim Surfaces_Edges_and_Surfaces As New Dictionary(Of Tag, List(Of Tag))
            Dim Surfaces_Neighbours As New List(Of Tag)
            Surfaces_Edges_and_Surfaces = Func_Query_Surfaces(_Tag, Surfaces_NX_Data_Dict.Edge._ValueOutput(_Tag), Surfaces_Neighbours)
            Dim NeighbouringSurfaces_str As String = String.Join(",", Surfaces_Neighbours.Distinct.ToArray())
            '# Filling the table with general data
            Surfaces_NX_Data_Dict.NeighbourSurfaces._Entry(_Tag, Surfaces_Edges_and_Surfaces)
            Table_Output_NX.Filling_general(Surface_contents, _Tag, Surface_ID, NeighbouringSurfaces_str)
        End If
    End Sub

    '# Identify adjacent faces of a given face
    '###########################################################################
    Private Function Func_Query_Surfaces(ByVal _Tag As Tag, ByVal Edgelist() As Tag, ByRef Neighbours_of_the_Surface As List(Of Tag)) As Dictionary(Of Tag, List(Of Tag))

        Dim NeighbouringSurfaces_internal As New Dictionary(Of Tag, List(Of Tag))
        For l = 0 To Edgelist.Length - 1
            Dim Surfaces_array() As Tag = Nothing
            theUFSession.Modl.AskEdgeFaces(Edgelist(l), Surfaces_array)
            Dim Surfaces_list = Surfaces_array.ToList
            Neighbours_of_the_Surface.AddRange(Surfaces_list)
            Neighbours_of_the_Surface.Remove(_Tag)
            Surfaces_list.Remove(_Tag)
            NeighbouringSurfaces_internal.Add(Edgelist(l), Surfaces_list)
        Next
        Func_Query_Surfaces = NeighbouringSurfaces_internal
    End Function
    Private Function Func_Surface_contents(ByVal _Surface As Tag) As Double

        Dim Surface As Face = Utilities.NXObjectManager.Get(_Surface)
        Dim area_units As Unit = Part_act.UnitCollection.GetBase("Area")
        Dim length_units As Unit = Part_act.UnitCollection.GetBase("Length")

        Dim para_face(0) As IParameterizedSurface
        para_face(0) = Surface

        Dim Mass = Part_act.MeasureManager.NewFaceProperties(area_units, length_units, 0.999, para_face)
        Func_Surface_contents = Mass.Area

    End Function
End Module
