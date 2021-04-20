
Public Module Declaration_Tables
    ' 01 Start
    Public Class CSV_Output_BoundingBox
        Private Entries As New List(Of List(Of String))
        Private Table_Columns As DataTable

        Public Sub Entries_definition()
            Entries.Add(New List(Of String) From {"dim_box_1", "System.Double"})
            Entries.Add(New List(Of String) From {"dim_box_2", "System.Double"})
            Entries.Add(New List(Of String) From {"dim_box_3", "System.Double"})
            Entries.Add(New List(Of String) From {"volume_part", "System.Double"})
            Entries.Add(New List(Of String) From {"volume_box", "System.Double"})
            Entries.Add(New List(Of String) From {"coordinate_p1_x", "System.Double"})
            Entries.Add(New List(Of String) From {"coordinate_p1_y", "System.Double"})
            Entries.Add(New List(Of String) From {"coordinate_p1_z", "System.Double"})
            Entries.Add(New List(Of String) From {"coordinate_p2_x", "System.Double"})
            Entries.Add(New List(Of String) From {"coordinate_p2_y", "System.Double"})
            Entries.Add(New List(Of String) From {"coordinate_p2_z", "System.Double"})
            Entries.Add(New List(Of String) From {"orientation_1_x", "System.Double"})
            Entries.Add(New List(Of String) From {"orientation_1_y", "System.Double"})
            Entries.Add(New List(Of String) From {"orientation_1_z", "System.Double"})
            Entries.Add(New List(Of String) From {"orientation_2_x", "System.Double"})
            Entries.Add(New List(Of String) From {"orientation_2_y", "System.Double"})
            Entries.Add(New List(Of String) From {"orientation_2_z", "System.Double"})
            Entries.Add(New List(Of String) From {"orientation_3_x", "System.Double"})
            Entries.Add(New List(Of String) From {"orientation_3_y", "System.Double"})
            Entries.Add(New List(Of String) From {"orientation_3_z", "System.Double"})
            Entries.Add(New List(Of String) From {"cog_part_x", "System.Double"})
            Entries.Add(New List(Of String) From {"cog_part_y", "System.Double"})
            Entries.Add(New List(Of String) From {"cog_part_z", "System.Double"})
            Entries.Add(New List(Of String) From {"date", "System.String"})
            Table_Columns = Func_Create_Table(Entries).Tables(0)
        End Sub

        Public Sub Filling(ByVal Length As Double, ByVal Height As Double, ByVal width As Double, ByVal Volume_Part As Double,
                            ByVal Volume_Box As Double, ByVal Coordinate_P1_x As Double, ByVal Coordinate_P1_y As Double,
                            ByVal Coordinate_P1_z As Double, ByVal Coordinate_P2_x As Double, ByVal Coordinate_P2_y As Double,
                            ByVal Coordinate_P2_z As Double, ByVal Orientation_1_x As Double, ByVal Orientation_1_y As Double,
                            ByVal Orientation_1_z As Double, ByVal Orientation_2_x As Double, ByVal Orientation_2_y As Double,
                            ByVal Orientation_2_z As Double, ByVal Orientation_3_x As Double, ByVal Orientation_3_y As Double,
                            ByVal Orientation_3_z As Double, ByVal CoG_Part_x As Double,
                            ByVal CoG_Part_y As Double, ByVal CoG_Part_z As Double, ByVal Date_now As String)

            Dim Filling_temp As DataRow = Nothing
            Filling_temp = Table_Columns.NewRow

            Filling_temp("dim_box_1") = Length
            Filling_temp("dim_box_2") = Height
            Filling_temp("dim_box_3") = width
            Filling_temp("volume_part") = Volume_Part
            Filling_temp("volume_box") = Volume_Box
            Filling_temp("coordinate_p1_x") = Coordinate_P1_x
            Filling_temp("coordinate_p1_y") = Coordinate_P1_y
            Filling_temp("coordinate_p1_z") = Coordinate_P1_z
            Filling_temp("coordinate_p2_x") = Coordinate_P2_x
            Filling_temp("coordinate_p2_y") = Coordinate_P2_y
            Filling_temp("coordinate_p2_z") = Coordinate_P2_z
            Filling_temp("orientation_1_x") = Orientation_1_x
            Filling_temp("orientation_1_y") = Orientation_1_y
            Filling_temp("orientation_1_z") = Orientation_1_z
            Filling_temp("orientation_2_x") = Orientation_2_x
            Filling_temp("orientation_2_y") = Orientation_2_y
            Filling_temp("orientation_2_z") = Orientation_2_z
            Filling_temp("orientation_3_x") = Orientation_3_x
            Filling_temp("orientation_3_y") = Orientation_3_y
            Filling_temp("orientation_3_z") = Orientation_3_z
            Filling_temp("cog_part_x") = CoG_Part_x
            Filling_temp("cog_part_y") = CoG_Part_y
            Filling_temp("cog_part_z") = CoG_Part_z
            Filling_temp("date") = Date_now
            Table_Columns.Rows.Add(Filling_temp)

        End Sub

        Public Sub Output()
            Sub_Table_exporting(Part_Name_org + Data_Name + ".csv", Table_Columns)
        End Sub
    End Class

    ' 01 End

    ' 02 Start
    Public Class CSV_Output_SurfaceData
        Private Entries As New List(Of List(Of String))
        Public Table_Columns_NX As DataTable
        Public Filling_temp As DataRow

        Public Sub Entries_Definition()
            Entries.Add(New List(Of String) From {"id", "System.Int32"}) '# ID reference number
            Entries.Add(New List(Of String) From {"surface", "System.Double"}) '# Surface
            Entries.Add(New List(Of String) From {"tag", "System.Int32"}) '# Day = NX-internal index of the Surface
            Entries.Add(New List(Of String) From {"nxid", "System.Int32"}) '# NXID = NX-internal ID-index of the Surface
            Entries.Add(New List(Of String) From {"neighboringsurfaces_list", "System.String"}) '#List of Tags of adjacent surfaces
            '# askFaceData
            Entries.Add(New List(Of String) From {"typ", "System.Int32"}) '# Surfacetype
            Entries.Add(New List(Of String) From {"point_x", "System.Double"}) '# Characteristic point after askFaceData function
            Entries.Add(New List(Of String) From {"point_y", "System.Double"}) '# Characteristic point after askFaceData function
            Entries.Add(New List(Of String) From {"point_z", "System.Double"}) '# Characteristic point after askFaceData function
            Entries.Add(New List(Of String) From {"dir_x", "System.Double"}) '# specific vector to askFaceData
            Entries.Add(New List(Of String) From {"dir_y", "System.Double"}) '# specific vector to askFaceData
            Entries.Add(New List(Of String) From {"dir_z", "System.Double"}) '# specific vector to askFaceData
            Entries.Add(New List(Of String) From {"radius", "System.Double"}) '# Radius at specific point according to askFaceData function
            Entries.Add(New List(Of String) From {"radius_data", "System.Double"}) '# Radius_min at specific point after askFaceData function
            Entries.Add(New List(Of String) From {"norm_dir", "System.Double"}) '# Normal direction at specific point according to askFaceData function
            '# askFaceParam
            Entries.Add(New List(Of String) From {"u", "System.Double"}) '# U-coordinates in Surfacecoordinatesystem
            Entries.Add(New List(Of String) From {"v", "System.Double"}) '# U-coordinates in Surfacecoordinatesystem
            '# askFaceProbs
            Entries.Add(New List(Of String) From {"p_point_x", "System.Double"}) '# Base of the normal vector
            Entries.Add(New List(Of String) From {"p_point_y", "System.Double"}) '# Base of the normal vector
            Entries.Add(New List(Of String) From {"p_point_z", "System.Double"}) '# Base of the normal vector
            Entries.Add(New List(Of String) From {"u_1_x", "System.Double"})
            Entries.Add(New List(Of String) From {"u_1_y", "System.Double"})
            Entries.Add(New List(Of String) From {"u_1_z", "System.Double"})
            Entries.Add(New List(Of String) From {"v_1_x", "System.Double"})
            Entries.Add(New List(Of String) From {"v_1_y", "System.Double"})
            Entries.Add(New List(Of String) From {"v_1_z", "System.Double"})
            Entries.Add(New List(Of String) From {"u_2_x", "System.Double"})
            Entries.Add(New List(Of String) From {"u_2_y", "System.Double"})
            Entries.Add(New List(Of String) From {"u_2_z", "System.Double"})
            Entries.Add(New List(Of String) From {"v_2_x", "System.Double"})
            Entries.Add(New List(Of String) From {"v_2_y", "System.Double"})
            Entries.Add(New List(Of String) From {"v_2_z", "System.Double"})
            Entries.Add(New List(Of String) From {"p_norm_x", "System.Double"}) '# Normal vector according to askFaceProps
            Entries.Add(New List(Of String) From {"p_norm_y", "System.Double"}) '# Normal vector according to askFaceProps
            Entries.Add(New List(Of String) From {"p_norm_z", "System.Double"}) '# Normal vector according to askFaceProps
            Entries.Add(New List(Of String) From {"p_radius_1", "System.Double"}) '# Main radius after askFaceProps
            Entries.Add(New List(Of String) From {"p_radius_2", "System.Double"}) '# Main radius after askFaceProps
            '# eigene Analyse
            Entries.Add(New List(Of String) From {"number_of_convex", "System.Int32"}) '# ID reference number
            Entries.Add(New List(Of String) From {"number_of_concave", "System.Int32"}) '# ID reference number
            Entries.Add(New List(Of String) From {"number_of_plane", "System.Int32"}) '# ID reference number
            Entries.Add(New List(Of String) From {"neighbour_type", "System.String"}) '# Surface category according to definition in diploma thesis
            Entries.Add(New List(Of String) From {"date", "System.String"})
            Table_Columns_NX = Func_Create_Table(Entries).Tables(0)
        End Sub

        Public Sub Create_Line(ByVal Index As Integer) 'As DataRow
            If Index <> 0 Then
                Table_Columns_NX.Rows.Add(Filling_temp)
            End If
            Filling_temp = Table_Columns_NX.NewRow
            Filling_temp("ID") = Index
        End Sub

        Public Sub Fill_Surface_angle(ByVal Number_of_Convex As Integer, ByVal Number_of_Concave As Integer, ByVal Number_Of_Plane As Integer, ByVal Neighbour_Type As String)
            Filling_temp("number_of_convex") = Number_of_Convex
            Filling_temp("number_of_concave") = Number_of_Concave
            Filling_temp("number_of_plane") = Number_Of_Plane
            Filling_temp("neighbour_type") = Neighbour_Type
        End Sub
        Public Sub Filling_general(ByVal Surface As Double, ByVal Tag As Integer, ByVal NXID As Integer, ByVal Neighboringsurfaces As String)
            Filling_temp("surface") = Surface
            Filling_temp("tag") = Tag
            Filling_temp("nxid") = NXID
            Filling_temp("neighboringsurfaces_list") = Neighboringsurfaces
            Filling_temp("date") = Date_now
        End Sub

        Public Sub Filling_AskData(ByVal Type As Integer, ByVal Point_x As Double, ByVal Point_y As Double, ByVal Point_z As Double,
                                    ByVal Dir_x As Double, ByVal Dir_y As Double, ByVal Dir_z As Double,
                                    ByVal Radius As Double, ByVal Radius_data As Double, ByVal Norm_Dir As Double,
                                    ByVal u As Double, ByVal v As Double)
            Filling_temp("typ") = Type
            Filling_temp("point_x") = Point_x
            Filling_temp("point_y") = Point_y
            Filling_temp("point_z") = Point_z
            Filling_temp("dir_x") = Dir_x
            Filling_temp("dir_y") = Dir_y
            Filling_temp("dir_z") = Dir_z
            Filling_temp("radius") = Radius
            Filling_temp("radius_data") = Radius_data
            Filling_temp("Norm_Dir") = Norm_Dir
            '# askFaceParam
            Filling_temp("u") = u
            Filling_temp("v") = v
        End Sub

        Public Sub Filling_AskProbs(ByVal P_Point_x As Double, ByVal P_Point_y As Double, ByVal P_Point_z As Double,
                                    ByVal u_1_x As Double, ByVal u_1_y As Double, ByVal u_1_z As Double,
                                    ByVal v_1_x As Double, ByVal v_1_y As Double, ByVal v_1_z As Double,
                                    ByVal u_2_x As Double, ByVal u_2_y As Double, ByVal u_2_z As Double,
                                    ByVal v_2_x As Double, ByVal v_2_y As Double, ByVal v_2_z As Double,
                                    ByVal P_Norm_x As Double, ByVal P_Norm_y As Double, ByVal P_Norm_z As Double,
                                    ByVal P_Radius_1 As Double, ByVal P_Radius_2 As Double)
            Filling_temp("p_point_x") = P_Point_x
            Filling_temp("p_point_y") = P_Point_y
            Filling_temp("p_point_z") = P_Point_z
            Filling_temp("u_1_x") = u_1_x
            Filling_temp("u_1_y") = u_1_y
            Filling_temp("u_1_z") = u_1_z
            Filling_temp("v_1_x") = v_1_x
            Filling_temp("v_1_y") = v_1_y
            Filling_temp("v_1_z") = v_1_z
            Filling_temp("u_2_x") = u_2_x
            Filling_temp("u_2_y") = u_2_y
            Filling_temp("u_2_z") = u_2_z
            Filling_temp("v_2_x") = v_2_x
            Filling_temp("v_2_y") = v_2_y
            Filling_temp("v_2_z") = v_2_z
            Filling_temp("p_norm_x") = P_Norm_x
            Filling_temp("p_norm_y") = P_Norm_y
            Filling_temp("p_norm_z") = P_Norm_z
            Filling_temp("p_radius_1") = P_Radius_1
            Filling_temp("p_radius_2") = P_Radius_2
        End Sub

        Public Sub Sorting()
            Sub_Table_sorting("surface", Table_Columns_NX)
        End Sub

        Public Sub Output()
            Sub_Table_exporting(Part_Name_org + Data_Name + "_NX.csv", Table_Columns_NX)
        End Sub
    End Class

    Public Class CSV_Output_NeighborData
        Private Entries As New List(Of List(Of String))
        Private Table_Columns_Neighbour As DataTable
        Public Sub Entries_Definition()
            Entries.Add(New List(Of String) From {"id", "System.Int32"}) '# ID reference number
            Entries.Add(New List(Of String) From {"tags_of_the_surfaces_list", "System.String"})
            Entries.Add(New List(Of String) From {"surfacecontent", "System.Double"})
            Entries.Add(New List(Of String) From {"number_of_convex", "System.Int32"})
            Entries.Add(New List(Of String) From {"number_of_concave", "System.Int32"})
            Entries.Add(New List(Of String) From {"neighbortype", "System.String"})
            Entries.Add(New List(Of String) From {"date", "System.String"})
            Table_Columns_Neighbour = Func_Create_Table(Entries).Tables(0)
        End Sub
        Public Sub Filling(ByVal ID As Integer, ByVal Tags_der_Flaechen As String, ByVal Surfacecontent As Double,
                            ByVal Number_Of_Convex As Integer, ByVal Number_Of_Concave As Integer, ByVal Neighbortype As String)
            Dim Filling_temp As DataRow = Nothing
            Filling_temp = Table_Columns_Neighbour.NewRow

            Filling_temp("id") = ID
            Filling_temp("tags_of_the_surfaces_list") = Tags_der_Flaechen
            Filling_temp("surfacecontent") = Surfacecontent
            Filling_temp("number_of_convex") = Number_Of_Convex
            Filling_temp("number_of_concave") = Number_Of_Concave
            Filling_temp("neighbortype") = Neighbortype
            Filling_temp("date") = Date_now
            Table_Columns_Neighbour.Rows.Add(Filling_temp)

        End Sub
        Public Sub Sorting()
            Sub_Table_sorting("surfacecontent", Table_Columns_Neighbour)
        End Sub
        Public Sub Output()
            Sub_Table_exporting(Part_Name_org + Data_Name + "_Connected.csv", Table_Columns_Neighbour)
        End Sub
    End Class

    Public Class Table_FaceType_distribution_perNumber
        Private Entries As New List(Of List(Of String))
        Private distributionvalues As DataTable

        Public Sub Entries_Definition()

            For Each classification In Classification_of_surface_categories
                Entries.Add(New List(Of String) From {classification, "System.Double"})
            Next
            Entries.Add(New List(Of String) From {"surface_quantity", "System.Int32"})
            For Each NX_Surface In NX_Surface_Categories
                Entries.Add(New List(Of String) From {NX_Surface, "System.Double"})
            Next
            Entries.Add(New List(Of String) From {"nx_surface_quantity", "System.Int32"})
            Entries.Add(New List(Of String) From {"date", "System.String"})
            distributionvalues = Func_Create_Table(Entries).Tables(0)
        End Sub
        Public Sub Filling(ByVal _Classification_Surface_distribution As Dictionary(Of String, Double),
                           ByVal Number_Of_Classification As Integer,
                           ByVal _NX_Surface_Distribution As Dictionary(Of String, Double),
                           ByVal Number_Of_NX_Surface As Integer)

            Dim Filling_temp As DataRow = Nothing
            Filling_temp = distributionvalues.NewRow

            For Each Einordnung In _Classification_Surface_distribution.Keys
                Filling_temp(Einordnung) = Math.Round(_Classification_Surface_distribution(Einordnung) / Number_Of_Classification, 3)
            Next
            Filling_temp("surface_quantity") = Number_Of_Classification
            For Each NX_Surface In _NX_Surface_Distribution.Keys
                Filling_temp(NX_Surface) = Math.Round(_NX_Surface_Distribution(NX_Surface) / Number_Of_NX_Surface, 3)
            Next
            Filling_temp("nx_surface_quantity") = Number_Of_NX_Surface
            Filling_temp("date") = Date_now
            distributionvalues.Rows.Add(Filling_temp)
        End Sub

        Public Function DataTable_Output() As DataTable
            DataTable_Output = distributionvalues
        End Function
        Public Sub Output()
            Sub_Table_exporting(Part_Name_org + Data_Name + "_Distribution_perNumber.csv", distributionvalues)
        End Sub

    End Class

    Public Class Table_FaceType_distribution_perArea
        Private Entries As New List(Of List(Of String))
        Private distributionvalues As DataTable

        Public Sub Entries_Definition()

            For Each classification In Classification_of_surface_categories
                Entries.Add(New List(Of String) From {classification, "System.Double"})
            Next
            For Each NX_Surface In NX_Surface_Categories
                Entries.Add(New List(Of String) From {NX_Surface, "System.Double"})
            Next
            Entries.Add(New List(Of String) From {"area_total_part", "System.Double"})
            Entries.Add(New List(Of String) From {"date", "System.String"})
            distributionvalues = Func_Create_Table(Entries).Tables(0)
        End Sub
        Public Sub Filling(ByVal _Classification_Surface_distribution As Dictionary(Of String, Double),
                           ByVal _NX_Surface_Distribution As Dictionary(Of String, Double),
                           ByVal _Total_Surface_Area As Double)

            Dim FillingTemp As DataRow = Nothing
            FillingTemp = distributionvalues.NewRow

            For Each Classification In _Classification_Surface_distribution.Keys
                FillingTemp(Classification) = Math.Round(_Classification_Surface_distribution(Classification) / _Total_Surface_Area, 3)
            Next
            For Each NX_Surface In _NX_Surface_Distribution.Keys
                FillingTemp(NX_Surface) = Math.Round(_NX_Surface_Distribution(NX_Surface) / _Total_Surface_Area, 3)
            Next
            FillingTemp("area_total_part") = _Total_Surface_Area

            FillingTemp("date") = Date_now
            distributionvalues.Rows.Add(FillingTemp)
        End Sub

        Public Function DataTable_Output() As DataTable
            DataTable_Output = distributionvalues
        End Function
        Public Sub Output()
            Sub_Table_exporting(Part_Name_org + Data_Name + "_Distribution_perArea.csv", distributionvalues)
        End Sub

    End Class

    'Public Class Class_Table_Curvature_Distribution_Surface
    '    Private Entries As New List(Of List(Of String))
    '    Private Curvature_Values As DataTable

    '    Public Sub Entries_Definition()

    '        Entries.Add(New List(Of String) From {"tag", "System.Int32"})
    '        For Each Category In Curvature_categories
    '            Entries.Add(New List(Of String) From {Category, "System.Double"})
    '        Next
    '        Entries.Add(New List(Of String) From {"number_of", "System.Int32"})
    '        Entries.Add(New List(Of String) From {"date", "System.String"})
    '        Curvature_Values = Func_Create_Table(Entries).Tables(0)
    '    End Sub

    '    Public Sub Filling(ByVal Surface_Tag As Integer, ByVal _Curvature_distribution As Dictionary(Of String, Integer), ByVal _Number_of_Curvature_Categories_Surface As Integer)

    '        Dim Filling_temp As DataRow = Nothing
    '        Filling_temp = Curvature_Values.NewRow
    '        Filling_temp("tag") = Surface_Tag
    '        For Each Category In _Curvature_distribution.Keys
    '            Filling_temp(Category) = Math.Round(_Curvature_distribution(Category) / _Number_of_Curvature_Categories_Surface, 3)
    '        Next
    '        Filling_temp("_number_of_curvature_categories_surface") = _Number_of_Curvature_Categories_Surface
    '        Filling_temp("date") = Date_now
    '        Curvature_Values.Rows.Add(Filling_temp)
    '    End Sub

    '    Public Sub Sorting()
    '        Sub_Table_sorting("Bereich", Curvature_Values)
    '    End Sub

    '    Public Function DataTable_Output() As DataTable
    '        DataTable_Output = Curvature_Values
    '    End Function
    '    Public Sub Output()
    '        'Sub_Table_exporting(Output_Designation_Curvature_Surface + ".csv", Curvature_Values)
    '        Sub_Table_exporting(Part_ID + "_" + Part_Name_org + "_yyy.csv", Curvature_Values)
    '    End Sub
    'End Class

    Public Class Table_Curvature_Points_pro_Surface
        Private Entries As New List(Of List(Of String))
        Private Curvature_Values As DataTable

        Public Sub Entries_Definition()

            Entries.Add(New List(Of String) From {"tag", "System.Int32"})
            Entries.Add(New List(Of String) From {"gausscurvature", "System.Double"})
            Entries.Add(New List(Of String) From {"meancurvature", "System.Double"})
            Entries.Add(New List(Of String) From {"category", "System.String"})
            Entries.Add(New List(Of String) From {"curvatureradius_1", "System.Double"})
            Entries.Add(New List(Of String) From {"curvatureradius_2", "System.Double"})
            Entries.Add(New List(Of String) From {"x", "System.Double"})
            Entries.Add(New List(Of String) From {"y", "System.Double"})
            Entries.Add(New List(Of String) From {"z", "System.Double"})
            Entries.Add(New List(Of String) From {"u", "System.Double"})
            Entries.Add(New List(Of String) From {"v", "System.Double"})
            Entries.Add(New List(Of String) From {"date", "System.String"})
            Curvature_Values = Func_Create_Table(Entries).Tables(0)
        End Sub

        Public Sub Filling(ByVal Surface_Tag As Integer, ByVal Gauss_Curvature As Double, ByVal Mean_Curvature As Double,
                            ByVal Category As String, ByVal r1 As Double, ByVal r2 As Double,
                            ByVal x As Double, ByVal y As Double, ByVal z As Double, ByVal u As Double, ByVal v As Double)
            Dim Filling_temp As DataRow = Nothing
            Filling_temp = Curvature_Values.NewRow
            Filling_temp("tag") = Surface_Tag
            Filling_temp("gausscurvature") = Gauss_Curvature
            Filling_temp("meancurvature") = Mean_Curvature
            Filling_temp("category") = Category
            Filling_temp("curvatureradius_1") = r1
            Filling_temp("curvatureradius_2") = r2
            Filling_temp("x") = x
            Filling_temp("y") = y
            Filling_temp("z") = z
            Filling_temp("u") = u
            Filling_temp("v") = v
            Filling_temp("date") = Date_now
            Curvature_Values.Rows.Add(Filling_temp)
        End Sub

        Public Function DataTable_Output() As DataTable
            DataTable_Output = Curvature_Values
        End Function
        Public Sub Output(ByVal _Name As String)
            Sub_Table_exporting(Output_Subfolder_Curvature + _Name + ".csv", Curvature_Values)
        End Sub
    End Class
    ' 02 End

    '03 start
    Public Class Class_Table_Distributions_Body_PointCloud
        Private Entries As New List(Of List(Of String))
        Private Distribution_Values As DataTable

        Public Sub Entries_Definition()

            For Each Curvature In Curvature_categories
                Entries.Add(New List(Of String) From {Curvature, "System.Double"})
            Next
            Entries.Add(New List(Of String) From {"k_quantity", "System.Int32"})
            Entries.Add(New List(Of String) From {"date", "System.String"})
            Distribution_Values = Func_Create_Table(Entries).Tables(0)
        End Sub

        Public Sub Filling(ByVal _Curvature_distribution As Dictionary(Of String, Double),
                           ByVal Number_Of_krPunkte As Integer)

            Dim Fillng_temp As DataRow = Nothing
            Fillng_temp = Distribution_Values.NewRow

            For Each Category In _Curvature_distribution.Keys
                Fillng_temp(Category) = Math.Round(_Curvature_distribution(Category) / Number_Of_krPunkte, 3)
            Next
            Fillng_temp("k_quantity") = Number_Of_krPunkte

            Fillng_temp("date") = Date_now
            Distribution_Values.Rows.Add(Fillng_temp)
        End Sub

        Public Function DataTable_Output() As DataTable
            DataTable_Output = Distribution_Values
        End Function
        Public Sub Output()
            'Sub_Table_exporting(Output_Designation_Curvature_Body + ".csv", Distribution_Values)
            Sub_Table_exporting(Part_Name_org + Data_Name + "_Distribution.csv", Distribution_Values)
        End Sub
    End Class
    Public Class Table_Curvature_Points
        Private EntryList As New List(Of List(Of String))
        Private Degree_Of_Curvature As DataTable

        Public Sub Entries_definition()

            EntryList.Add(New List(Of String) From {"id", "System.String"})
            EntryList.Add(New List(Of String) From {"gauss_curvature", "System.Double"})
            EntryList.Add(New List(Of String) From {"mean_curvature", "System.Double"})
            EntryList.Add(New List(Of String) From {"category", "System.String"})
            EntryList.Add(New List(Of String) From {"curvatureradius_1", "System.Double"})
            EntryList.Add(New List(Of String) From {"curvatureradius_2", "System.Double"})
            EntryList.Add(New List(Of String) From {"x", "System.Double"})
            EntryList.Add(New List(Of String) From {"y", "System.Double"})
            EntryList.Add(New List(Of String) From {"z", "System.Double"})
            EntryList.Add(New List(Of String) From {"u", "System.Double"})
            EntryList.Add(New List(Of String) From {"v", "System.Double"})
            EntryList.Add(New List(Of String) From {"x_f", "System.Double"})
            EntryList.Add(New List(Of String) From {"y_f", "System.Double"})
            EntryList.Add(New List(Of String) From {"z_f", "System.Double"})
            EntryList.Add(New List(Of String) From {"normx_f", "System.Double"})
            EntryList.Add(New List(Of String) From {"normy_f", "System.Double"})
            EntryList.Add(New List(Of String) From {"normz_f", "System.Double"})
            EntryList.Add(New List(Of String) From {"date", "System.String"})
            Degree_Of_Curvature = Func_Create_Table(EntryList).Tables(0)
        End Sub

        Public Sub Filling(ByVal Tag_in As String, ByVal Gauss_curvature As Double, ByVal Mean_curvature As Double,
                            ByVal Category As String, ByVal r1 As Double, ByVal r2 As Double,
                            ByVal x As Double, ByVal y As Double, ByVal z As Double,
                            ByVal u As Double, ByVal v As Double,
                            ByVal x_f As Double, ByVal y_f As Double, ByVal z_f As Double,
                            ByVal normx_f As Double, ByVal normy_f As Double, ByVal normz_f As Double)
            Dim Filling_temp As DataRow = Nothing
            Filling_temp = Degree_Of_Curvature.NewRow
            Filling_temp("id") = Tag_in
            Filling_temp("gauss_curvature") = Gauss_curvature
            Filling_temp("mean_curvature") = Mean_curvature
            Filling_temp("category") = Category
            Filling_temp("curvatureradius_1") = r1
            Filling_temp("curvatureradius_2") = r2
            Filling_temp("x") = x
            Filling_temp("y") = y
            Filling_temp("z") = z
            Filling_temp("u") = u
            Filling_temp("v") = v
            Filling_temp("x_f") = x_f
            Filling_temp("y_f") = y_f
            Filling_temp("z_f") = z_f
            Filling_temp("normx_f") = normx_f
            Filling_temp("normy_f") = normy_f
            Filling_temp("normz_f") = normz_f
            Filling_temp("date") = Date_now
            Degree_Of_Curvature.Rows.Add(Filling_temp)
        End Sub

        Public Sub Output()
            'Sub_Table_exporting(Output_Designation_Curvature_Surface + ".csv", Degree_Of_Curvature)
            Sub_Table_exporting(Part_Name_org + Data_Name + ".csv", Degree_Of_Curvature)
        End Sub
    End Class
    '03 end
End Module