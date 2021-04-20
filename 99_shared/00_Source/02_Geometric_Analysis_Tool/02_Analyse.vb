Imports NXOpen
Imports System
Imports NXOpen.UF
Imports NXOpen.UI
Imports NXOpen.Utilities
Imports NXOpen.VectorArithmetic
Imports Math_Net = MathNet.Numerics
Imports System.Math

Public Module _02_Analyse
    Public Sub _start()
        Console.WriteLine("## Start Of Analysis")
        Curvature_Output_Points.Entries_definition()
        Table_Distributions_body_PointCloud.Entries_Definition()
        For Each Category In Curvature_categories
            Distribution_curvature_categories_body(Category) = 0
        Next
        Console.WriteLine("## Start 2")
        'Dim Time_2 As DateTime = DateTime.Now
        Dim Is_Curvature_Output_Points_Filling_Allowed As Boolean = True
        Number_Points_AskMinDist(Is_Curvature_Output_Points_Filling_Allowed)
        'Dim Time_3 As DateTime = DateTime.Now
        'Dim TotalTime_1 As DateTime = Time_3 - Time_2
        'Console.WriteLine("## Time 2 =" & TotalTime_1.ToString("hh':'mm':'ss"))
        Console.WriteLine("## End Of Analysis")
        Curvature_Output_Points.Output()
        Table_Distributions_body_PointCloud.Filling(Distribution_curvature_categories_body,
                                              Number_of_krPoints)
        Table_Distributions_body_PointCloud.Output()

    End Sub

    Private Sub Sub_Point_Reduction(ByVal Coordinate_act As Tuple(Of Integer, Integer, Integer),
                                 ByVal Distances_act As List(Of Double),
                                 ByRef PointCloud As Dictionary(Of Tuple(Of Integer, Integer, Integer), Double()))



        Dim Coord_Limit_0 As Integer = Math.Floor(Distances_act(0) / delta_R0)
        If Coord_Limit_0 > 0 Then
            Coord_Limit_0 -= 1
        End If
        Dim Coord_Limit_1 As Integer = Math.Floor(Distances_act(1) / delta_R1)
        If Coord_Limit_1 > 0 Then
            Coord_Limit_1 -= 1
        End If
        Dim Coord_Limit_2 As Integer = Math.Floor(Distances_act(2) / delta_R2)
        If Coord_Limit_2 > 0 Then
            Coord_Limit_2 -= 1
        End If

        Dim Radius As Double = Math.Sqrt((Coord_Limit_0 * delta_R0) ^ 2 + (Coord_Limit_1 * delta_R1) ^ 2 + (Coord_Limit_2 * delta_R2) ^ 2)

        Dim Coord_Circle_0 As Integer = Math.Floor(Radius / delta_R0)
        Dim Coord_Circle_1 As Integer = Math.Floor(Radius / delta_R1)
        Dim Coord_Circle_2 As Integer = Math.Floor(Radius / delta_R2)

        For i_2 = -Coord_Circle_2 To Coord_Circle_2 Step 1
            For i_1 = -Coord_Circle_1 To Coord_Circle_1 Step 1
                For i_0 = -Coord_Circle_0 To Coord_Circle_0 Step 1

                    Dim RadiusTest As Double = Math.Sqrt((i_0 * delta_R0) ^ 2 + (i_1 * delta_R1) ^ 2 + (i_2 * delta_R2) ^ 2)
                    If RadiusTest <= Radius Then
                        Dim Coord_0 = Coordinate_act.Item1 + i_0
                        Dim Coord_1 = Coordinate_act.Item2 + i_1
                        Dim Coord_2 = Coordinate_act.Item3 + i_2

                        Dim Coord2Sub = Tuple.Create(Of Integer, Integer, Integer)(
                            Coord_0, Coord_1, Coord_2)

                        If (Coord_0 < 0 Or Coord_1 < 0 Or Coord_2 < 0) Or
                            (Coord_0 > Number_of_R0 Or Coord_1 > Number_of_R1 Or Coord_2 > Number_of_R2) Then
                            Continue For
                        ElseIf PointCloud.ContainsKey(Coord2Sub) Then
                            PointCloud.Remove(Coord2Sub)
                        End If
                    End If
                Next
            Next
        Next

    End Sub


    Private Function Func_Next_Coordinate(ByVal Coordinate_act As Tuple(Of Integer, Integer, Integer),
                                               ByVal Distances_act As List(Of Double), ByVal PointCloud As Dictionary(Of
                                               Tuple(Of Integer, Integer, Integer), Double())
                                          ) As List(Of Tuple(Of Integer, Integer, Integer))

        Dim Sign_array() As Double = {-1, 1}
        Dim List_next_Point As New List(Of Tuple(Of Integer, Integer, Integer))

        For Each CurrSign In Sign_array
            Dim Coord_Limit_0 As Integer = Math.Floor(Distances_act(0) * CurrSign / delta_R0) + (CurrSign * 1)
            Dim Coord_Limit_1 As Integer = Math.Floor(Distances_act(1) * CurrSign / delta_R1) + (CurrSign * 1)
            Dim Coord_Limit_2 As Integer = Math.Floor(Distances_act(2) * CurrSign / delta_R2) + (CurrSign * 1)

            Dim List_next_Point_zw As New List(Of Tuple(Of Integer, Integer, Integer))
            List_next_Point_zw.Add(Tuple.Create(Of Integer, Integer, Integer)(
                                          Coordinate_act.Item1 + Coord_Limit_0,
                                          Coordinate_act.Item2,
                                          Coordinate_act.Item3))
            List_next_Point_zw.Add(Tuple.Create(Of Integer, Integer, Integer)(
                                          Coordinate_act.Item1,
                                          Coordinate_act.Item2 + Coord_Limit_1,
                                          Coordinate_act.Item3))
            List_next_Point_zw.Add(Tuple.Create(Of Integer, Integer, Integer)(
                                          Coordinate_act.Item1,
                                          Coordinate_act.Item2,
                                          Coordinate_act.Item3 + Coord_Limit_2))

            For Each Point In List_next_Point_zw
                If (Point.Item1 < 0 Or Point.Item2 < 0 Or Point.Item3 < 0) Or
                (Point.Item1 > Number_of_R0 Or Point.Item2 > Number_of_R1 Or Point.Item3 > Number_of_R2) Then
                    Continue For
                ElseIf PointCloud.ContainsKey(Point) Then
                    List_next_Point.Add(Point)
                End If
            Next
        Next
        Return List_next_Point
    End Function

    Public Sub Number_Points_AskMinDist(ByVal Is_Curvature_Output_Points_Filling_Allowed As Boolean)

        Dim Point_Surface_Act As Double() = Nothing
        Dim Surface_tag_act As Tag = Nothing
        Dim uv_act(1) As Double

        Dim Points_pass As New HashSet(Of Tuple(Of Integer, Integer, Integer))
        'First the corners
        Points_pass.Add(Tuple.Create(Of Integer, Integer, Integer)(0, 0, 0))
        Points_pass.Add(Tuple.Create(Of Integer, Integer, Integer)(Number_of_R0 - 1, 0, 0))
        Points_pass.Add(Tuple.Create(Of Integer, Integer, Integer)(0, Number_of_R1 - 1, 0))
        Points_pass.Add(Tuple.Create(Of Integer, Integer, Integer)(Number_of_R0 - 1, Number_of_R1 - 1, 0))
        Points_pass.Add(Tuple.Create(Of Integer, Integer, Integer)(0, 0, Number_of_R2 - 1))
        Points_pass.Add(Tuple.Create(Of Integer, Integer, Integer)(Number_of_R0 - 1, 0, Number_of_R2 - 1))
        Points_pass.Add(Tuple.Create(Of Integer, Integer, Integer)(0, Number_of_R1 - 1, Number_of_R2 - 1))
        Points_pass.Add(Tuple.Create(Of Integer, Integer, Integer)(Number_of_R0 - 1, Number_of_R1 - 1, Number_of_R2 - 1))

        Dim RescuePoints As List(Of Tuple(Of Integer, Integer, Integer, Double())) = Func_Points_Rescue()

        Dim Set_next_Point_basis As New HashSet(Of Tuple(Of Integer, Integer, Integer))

        Dim Switch_data_reduction As Boolean = False
        Dim Coordinate_act As Tuple(Of Integer, Integer, Integer) = Nothing
        Dim Point_act As Double()
        Dim Distances_act As List(Of Double) = Nothing
        Dim Points_pass_act As New List(Of Tuple(Of Integer, Integer, Integer))

        Dim List_Point_Grid As New List(Of Tag)

        Dim Liste_Point_Surface As New List(Of Tag)

        Dim HashSet_Points_coords_Surface As New HashSet(Of Double())


        Dim NumberOfPoints_0 = PointsCloud.Count()
        Dim Process_act_1 As Double = 100
        Dim Process_act_5 As Double = 100
        Dim Time_Process As TimeSpan = TimeSpan.Zero
        Dim Process_rest As Double = Nothing
        Dim Status_Process As Double = Nothing

        While PointsCloud.Count() > 0 = True

            If Points_pass_act.Count > 0 Then

                For Each Each_Pass_Point In Points_pass_act
                    Points_pass.Remove(Each_Pass_Point)
                    PointsCloud.Remove(Each_Pass_Point)
                Next

                If Switch_data_reduction = True Then
                    Sub_Point_Reduction(Coordinate_act,
                                     Distances_act,
                                     PointsCloud
                                     )
                    If Not Set_next_Point_basis.Contains(Coordinate_act) Then
                        Dim nextCoord_Act = Func_Next_Coordinate(Coordinate_act,
                                                                          Distances_act,
                                                                          PointsCloud
                                                                          )
                        Set_next_Point_basis.Add(Coordinate_act)
                        Points_pass.UnionWith(nextCoord_Act)
                    End If
                End If

                Dim Dist_single_step As List(Of Double) = New List(Of Double)({0, 0, 0})
                Dim List_next_Coordinate As New List(Of Tuple(Of Integer, Integer, Integer))

                For Each Each_Pass_Point In Points_pass_act
                    If Not Set_next_Point_basis.Contains(Each_Pass_Point) Then
                        Dim nextCoord_Act = Func_Next_Coordinate(Each_Pass_Point,
                                                                          Dist_single_step,
                                                                          PointsCloud
                                                                          )
                        Points_pass.UnionWith(nextCoord_Act)
                        Set_next_Point_basis.Add(Each_Pass_Point)
                    End If
                Next

                Switch_data_reduction = False
            End If
            If Points_pass.Count = 0 And PointsCloud.Count() > 0 Then
                Points_pass.Add(PointsCloud.ElementAt(0).Key)
            End If
            Points_pass_act.Clear()

            Process_rest = Math.Round(PointsCloud.Count() / NumberOfPoints_0 * 100, 0)
            If Process_rest <= Process_act_1 - 0.5 Then
                theSession.DeleteAllUndoMarks()
                If Process_rest <= Process_act_5 - 5 Then
                    Status_Process = 100 - Process_rest
                    Console.WriteLine("Fortschritt " & Status_Process.ToString & "% " &
                                      "Pkte_Rest " & PointsCloud.Count() &
                                      " Delta_Zeit " & Time_Process.ToString("hh':'mm':'ss"))
                    Process_act_5 = Process_rest
                End If

                Process_act_1 = Process_rest
            End If

            For Each Coordinate_act In Points_pass
                Points_pass_act.Add(Coordinate_act)
                If Coordinate_act.Equals(New Tuple(Of Integer, Integer, Integer)(1, 8, 3)) Then
                    Dim ia As Integer = 2
                End If
                If PointsCloud.ContainsKey(Coordinate_act) Then
                    Point_act = PointsCloud(Coordinate_act)

                    Dim Output As Tuple(Of Double(), Double(), Tag, Double()) = Nothing
                    Dim min_dist As Double = Nothing, pt_on_obj1(2) As Double, pt_on_obj2(2) As Double, accuracy As Double = Nothing

                    theUFSession.Modl.AskMinimumDist3(2, Body_act.Tag, NXOpen.Tag.Null, 0, {0, 0, 0},
                                                1, Point_act, min_dist, pt_on_obj1, pt_on_obj2, accuracy)

                    Distances_act = Func_DistanceGridDirections(Point_act, pt_on_obj1)

                    If Distances_act(0) < delta_R0 / 2 And Distances_act(1) < delta_R1 / 2 And Distances_act(2) < delta_R2 / 2 Then

                        Dim Point_Check As Boolean = False
                        Sub_Point_which_Surface_rule(Is_Curvature_Output_Points_Filling_Allowed, pt_on_obj1, Surface_tag_act, uv_act, Point_Check)

                        If Point_Check = True Then

                            Point_Surface_Act = pt_on_obj1

                            Output = Tuple.Create(Of Double(), Double(), Tag, Double())(Point_act, Point_Surface_Act, Surface_tag_act, uv_act)
                            Dim Rating = Rating_Point(Is_Curvature_Output_Points_Filling_Allowed, Output, Coordinate_act)

                            Dim ID As String = Distances_act(0).ToString & "," & Distances_act(1).ToString & "," & Distances_act(2).ToString & "," & Rating.Item2 & "," & Coordinate_act.ToString
                            Dim HashCount_old As Integer = HashSet_Points_coords_Surface.Count()
                            HashSet_Points_coords_Surface.Add(Point_Surface_Act)
                            If Draft_Mode = True Then
                                If HashCount_old < HashSet_Points_coords_Surface.Count() Then
                                    Dim point_t As Point = Nothing
                                    List_Point_Grid.Add(Func_Point_To_Draw(Point_act, point_t, ID))
                                    Sub_Point_Color(point_t, Rating.Item2)
                                    Liste_Point_Surface.Add(Func_Point_To_Draw(Point_Surface_Act, point_t, ID))

                                    Sub_Point_Color(point_t, Rating.Item2)
                                End If
                            End If
                            Number_of_krPoints += 1
                        End If

                    ElseIf Distances_act(0) > delta_R0 * 2 Or Distances_act(1) > delta_R1 * 2 Or Distances_act(2) > delta_R2 * 2 Then

                        Switch_data_reduction = True
                        Exit For
                    End If
                End If
            Next
        End While
        Status_Process = 100 - Process_rest

        ' if no points created, create one in the center
        If HashSet_Points_coords_Surface.Count() = 0 Then
            HashSet_Points_coords_Surface = Func_CenterPoints(Is_Curvature_Output_Points_Filling_Allowed, RescuePoints, List_Point_Grid, Liste_Point_Surface)
        End If

        Console.WriteLine("progress " & Status_Process.ToString & "%")
        If Draft_Mode = True Then
            Sub_Create_FeatureGroup(List_Point_Grid.ToArray(), "Grid_Askmin")

            Sub_Create_FeatureGroup(Liste_Point_Surface.ToArray(), "Surface_Askmin")
        End If

        ' save points for box calculation
        If Is_Curvature_Output_Points_Filling_Allowed = False Then
            Matrix_Points_coords = Func_Double3D_to_MathNetMatrix(HashSet_Points_coords_Surface.ToArray())
        End If




    End Sub
    Private Function Rating_Point(ByVal Is_Curvature_Output_Points_Filling_Allowed As Boolean,
                                  ByVal _Point As Tuple(Of Double(), Double(), Tag, Double()),
                                      ByVal Coordinate_act As Tuple(Of Integer, Integer, Integer)) As Tuple(Of Double(), String)


        Dim Gauss_curvature As Double
        Dim Mean_curvature As Double
        Dim principal_curvatures(1) As Double
        Dim Category As String = "99"
        Dim curvature_radii(1) As Double
        Dim Point_uv = _Point.Item4
        Dim Surface_Tag = _Point.Item3
        Dim Change_PointLocation_ifFalse As Boolean = True
        Dim Origin_CurvatureCalc As Boolean = True
        Dim Normale(2) As Double
        Sub_Calculate_Curvatures(Surface_Tag,
                                   Point_uv, Gauss_curvature,
                                   Mean_curvature,
                                   principal_curvatures,
                                   Category,
                                   curvature_radii,
                                   Origin_CurvatureCalc,
                                   Change_PointLocation_ifFalse,
                                  Normale)
        Dim Point_Of_Surface(2) As Double
        If Not Point_uv.Equals(_Point.Item4) Then
            Point_Of_Surface = Func_Determine_point_on_surface(Surface_Tag, Point_uv)
        Else
            Point_Of_Surface = _Point.Item2
        End If
        If (Is_Curvature_Output_Points_Filling_Allowed) And Category <> "99" Then
            Distribution_curvature_categories_body(Category) += 1
            Dim Tag_in As String = Coordinate_act.ToString
            Curvature_Output_Points.Filling(Tag_in,
                                              Gauss_curvature,
                                              Mean_curvature,
                                              Category,
                                              curvature_radii(0),
                                              curvature_radii(1),
                                              _Point.Item1(0),
                                              _Point.Item1(1),
                                              _Point.Item1(2),
                                              Point_uv(0),
                                              Point_uv(1),
                                              Point_Of_Surface(0),
                                              Point_Of_Surface(1),
                                              Point_Of_Surface(2),
                                              Normale(0),
                                              Normale(1),
                                              Normale(2))
        End If

        Rating_Point = Tuple.Create(Of Double(), String)(Point_Of_Surface, Category)
    End Function


    Private Sub Sub_Calculate_Curvatures(ByVal Surface As Tag,
                                          ByRef Point_uv() As Double,
                                          ByRef Gauss_curvature As Double,
                                          ByRef Mean_curvature As Double,
                                          ByRef principal_curvatures() As Double,
                                          ByRef Category As String,
                                          ByRef curvature_radii_round() As Double,
                                          ByVal Origin_CurvatureCalc As Boolean,
                                          ByRef Change_PointLocation_ifFalse As Boolean,
                                          ByRef Normale As Double())

        Dim surfacevalues As NXOpen.UF.ModlSrfValue = Nothing
        Dim mode As Integer = NXOpen.UF.UFConstants.UF_MODL_EVAL_DERIV2
        theUFSession.Modl.EvaluateFace(Surface, mode, Point_uv, surfacevalues)

        Dim Default_Point(2) As Double
        Dim VectorDU(2) As Double
        Dim VectorDV(2) As Double
        Dim VectorDU2(2) As Double
        Dim VectorDV2(2) As Double
        Dim normal(2) As Double
        Dim radii(1) As Double
        theUFSession.Modl.AskFaceProps(Surface, Point_uv, Default_Point, VectorDU, VectorDV, VectorDU2, VectorDV2, normal, radii)

        Dim VecUxV(2) As Double
        theUFSession.Vec3.Cross(VectorDU, VectorDV, VecUxV)
        Dim mag_un As Double = Nothing
        Dim VecUxVNorm(2) As Double
        theUFSession.Vec3.Unitize(normal, 0.1, mag_un, VecUxVNorm)
        Normale = VecUxVNorm

        Dim En As Double
        Dim FFn As Double
        Dim Gn As Double
        theUFSession.Vec3.Dot(VectorDU, VectorDU, En)
        theUFSession.Vec3.Dot(VectorDU, VectorDV, FFn)
        theUFSession.Vec3.Dot(VectorDV, VectorDV, Gn)

        Dim Ln As Double
        Dim Mn As Double
        Dim Nn As Double
        theUFSession.Vec3.Dot(VecUxVNorm, VectorDU2, Ln)
        theUFSession.Vec3.Dot(VecUxVNorm, surfacevalues.srf_dudv, Mn)
        theUFSession.Vec3.Dot(VecUxVNorm, VectorDV2, Nn)

        '# Calculation of the Gauss curvature and mean curvature
        Gauss_curvature = ((Ln * Nn - Mn * Mn) / (En * Gn - FFn * FFn))
        Mean_curvature = (Ln * Gn - 2 * Mn * FFn + Nn * En) / (2 * (En * Gn - FFn * FFn))

        If Double.IsNaN(Gauss_curvature) = False And Double.IsNaN(Mean_curvature) = False Then
            Dim Root_Term = Mean_curvature * Mean_curvature - Gauss_curvature
            If Root_Term < 0 Then
                Root_Term = 0
            End If
            Dim Hk1 = Mean_curvature + Sqrt(Root_Term)
            Dim Hk2 = Mean_curvature - Sqrt(Root_Term)

            '# Calculation of the principal curvatures with the mean curvature
            ReDim principal_curvatures(1)
            principal_curvatures(0) = Hk1
            principal_curvatures(1) = Hk2

            Dim curvature_radii_0 As Double = 1 / principal_curvatures(0)
            Dim curvature_radii_1 As Double = 1 / principal_curvatures(1)

            curvature_radii_round(0) = Round(curvature_radii_0, 3)
            curvature_radii_round(1) = Round(curvature_radii_1, 3)

            Dim Control As Double = Double.PositiveInfinity
            Dim Control_neg As Double = Double.NegativeInfinity

            '# Defined Boundary: If Radius is greater than 10000mm, then the area in that direction is assumed to be "flat", so the Boundary Radius is infinite
            For i = 0 To 1
                If curvature_radii_round(i).Equals(Control_neg) Or curvature_radii_round(i) >= 50000000 Or curvature_radii_round(i) <= -50000000 Then
                    curvature_radii_round(i) = Double.PositiveInfinity

                    Gauss_curvature = 0
                End If
            Next



            '# Mapping of points into categories of Gaussian curvature and radii
            If Gauss_curvature = 0 And curvature_radii_round(0).Equals(Control) And curvature_radii_round(1).Equals(Control) Then
                '# Category 0:

                '# Planar Surface
                '# Gauss_curvature K=0 and r1=∞ and r2=∞
                Category = "k_00"

            ElseIf (Gauss_curvature = 0 And curvature_radii_round(0).Equals(Control) And curvature_radii_round(1) >= 0) Or
                (Gauss_curvature = 0 And curvature_radii_round(1).Equals(Control) And curvature_radii_round(0) >= 0) Then
                '# Category 0.5
                '# Simply curved Surface

                '# Gauss_curvature K=0 and r1=∞ and r2 positive bzw. r1 positive and r2=∞
                Category = "k_p_05"

            ElseIf (Gauss_curvature = 0 And curvature_radii_round(0).Equals(Control) And curvature_radii_round(1) < 0) Or
                (Gauss_curvature = 0 And curvature_radii_round(1).Equals(Control) And curvature_radii_round(0) < 0) Then
                '# Category -0.5
                '# Simply curved Surface

                '# Gauss_curvature K=0 and r1=∞ and r2 negative bzw. r1 negative and r2=∞
                Category = "k_n_05"

            ElseIf (Gauss_curvature > 0 And curvature_radii_round(0) = curvature_radii_round(1) And curvature_radii_round(0) > 0) Then
                '# Category 1

                '# Sphere
                '# Gauss_curvature K>0 and r1=r2 and r1>0 bzw. r2>0
                Category = "k_p_10"

            ElseIf (Gauss_curvature > 0 And curvature_radii_round(0) = curvature_radii_round(1) And curvature_radii_round(0) < 0) Then
                '# Category -1

                '# Negative Sphere
                '# Gauss_curvature K>0 and r1=r2 and r1<0 bzw. r2<0
                Category = "k_n_10"

            ElseIf (Gauss_curvature > 0 And curvature_radii_round(0) <> curvature_radii_round(1) And curvature_radii_round(0) > 0 And curvature_radii_round(1) > 0) Then
                '# Category 1.5
                '# spherical
                '# Gauss_curvature K>0 and r1<>r2 and r1>0 and r2>0
                Category = "k_p_15"


            ElseIf (Gauss_curvature > 0 And curvature_radii_round(0) <> curvature_radii_round(1) And curvature_radii_round(0) < 0 And curvature_radii_round(1) < 0) Then
                '# Category -1.5
                '# spherical
                '# Gauss_curvature K>0 and r1<>r2 and r1<0 and r2<0
                Category = "k_n_15"


            ElseIf (Gauss_curvature <= 0 And (Abs(curvature_radii_round(0)) = Abs(curvature_radii_round(1)))) Then
                '# Category 2
                '# saddle ball
                '# Gauss_curvature K<0 and Betrag(r1)=Betrag(r2)
                Category = "k_20"

            ElseIf (Gauss_curvature <= 0 And (Abs(curvature_radii_round(0)) <> Abs(curvature_radii_round(1)))) Then

                If (Abs(curvature_radii_round(0)) > Abs(curvature_radii_round(1)) And curvature_radii_round(0) > 0) Or
                   (Abs(curvature_radii_round(1)) > Abs(curvature_radii_round(0)) And curvature_radii_round(1) > 0) Then
                    '# Category 2.5
                    '# Saddle Spherical


                    '# Gauss_curvature K<0 and r1<>r2
                    '# Bigger radius is positive
                    Category = "k_p_25"

                ElseIf (Abs(curvature_radii_round(0)) > Abs(curvature_radii_round(1)) And curvature_radii_round(0) < 0) Or
                    (Abs(curvature_radii_round(1)) > Abs(curvature_radii_round(0)) And curvature_radii_round(1) < 0) Then
                    '# Category 2.5
                    '# Saddle Spherical


                    '# Gauss_curvature K>0 and r1<>r2
                    '# Bigger radius is negative
                    Category = "k_n_25"

                End If
            End If
        End If

        '# Control if category found and if gaus mean is not ok
        If Category = "99" And Change_PointLocation_ifFalse = True And Origin_CurvatureCalc = True Then
            'Gauss_curvature = "NaN"
            Sub_About_testing_Real_curvatures(Surface,
                                                 Point_uv,
                                                 Gauss_curvature,
                                                 Mean_curvature,
                                                 principal_curvatures,
                                                 Category,
                                                 curvature_radii_round,
                                                 Change_PointLocation_ifFalse,
                                                 Normale)
        End If


    End Sub
    Private Sub Sub_About_testing_Real_curvatures(ByVal Surface As Tag,
                                                     ByRef Act_uv() As Double,
                                                     ByRef Gauss_curvature As Double,
                                                     ByRef Mean_curvature As Double,
                                                     ByRef principal_curvatures() As Double,
                                                     ByRef Category As String,
                                                     ByRef curvature_radii() As Double,
                                                     ByRef Change_PointLocation_ifFalse As Boolean,
                                                     ByRef Normale As Double())
        '# This function deals with the case when an analysis point at which the curvature is calculated lies on the edge of the surface and therefore produces an error.
        '# It can happen that the Gaussian curvature at a point on the edge of the surface is not calculated correctly, ie it has the value "NaN".
        '# The following function then moves this point in small steps from the edge into the surface until a real value for the curvature is found.

        If Category = "99" Then

            Dim Real_Value As Boolean = False
            Dim Errors As Integer = 1
            Dim Counter_adjustments = 0
            Dim Increment As Double = 0.0001

            Do While Real_Value = False

                Dim test_uv() As Double = Nothing
                Dim multiplicator_u As Double = 1

                Dim multiplicator_v As Double = 1


                If Errors = 1 Then
                    If Act_uv(0) >= 1 Then
                        multiplicator_u = -1
                    End If
                    test_uv = {Act_uv(0) + multiplicator_u * Increment, Act_uv(1)}

                ElseIf Errors = 2 Then
                    If Act_uv(1) >= 1 Then

                        multiplicator_v = -1
                    End If
                    test_uv = {Act_uv(0), Act_uv(1) + multiplicator_v * Increment}

                ElseIf Errors = 3 Then
                    If Act_uv(0) >= 1 Then
                        multiplicator_u = -1
                    End If
                    If Act_uv(1) >= 1 Then

                        multiplicator_v = -1
                    End If
                    test_uv = {Act_uv(0) + multiplicator_u * Increment, Act_uv(1) + multiplicator_v * Increment}
                End If


                Errors += 1



                If Errors > 3 Then
                    Errors = 1
                    Increment = Increment + 0.0001
                End If

                Dim Origin_CurvatureCalc As Boolean = False
                Counter_adjustments += 1
                Sub_Calculate_Curvatures(Surface,
                                          test_uv,
                                          Gauss_curvature,
                                          Mean_curvature,
                                          principal_curvatures,
                                          Category,
                                          curvature_radii,
                                          Origin_CurvatureCalc,
                                          Change_PointLocation_ifFalse,
                                          Normale)

                If Category <> "99" Then
                    Real_Value = True
                    Act_uv = test_uv
                ElseIf Counter_adjustments = 30 Then
                    Change_PointLocation_ifFalse = False
                    Exit Do
                End If
            Loop
        End If
    End Sub


    Private Sub Sub_Point_which_Surface_tray(ByVal _Point As Double(),
                                              ByVal _Point_grid As Double(),
                                              ByRef _Surface_act As Tag,
                                              ByRef _Point_uv As Double())

        Dim direction() As Double = Nothing
        theUFSession.Vec3.Scale(1000, _Point_grid, _Point_grid)
        If Math.Round(_Point(0), 2) = 0 And Math.Round(_Point(1), 2) = 0 And Math.Round(_Point(2), 2) = 0 Then
            direction = _Point_grid
        ElseIf Math.Round(_Point_grid(0), 2) = 0 And Math.Round(_Point_grid(1), 2) = 0 And Math.Round(_Point_grid(2), 2) = 0 Then
            direction = {1, 0, 0}
        Else
            theUFSession.Vec3.Sub(_Point_grid, _Point, direction)
        End If

        Dim identity(15) As Double
        theUFSession.Mtx4.Identity(identity)
        Dim num_results As Integer = Nothing
        Dim hits() As UFModl.RayHitPointInfo = Nothing

        theUFSession.Modl.TraceARay(1, {Body_act.Tag}, _Point, direction, identity, 1, num_results, hits)

        Dim face = Utilities.NXObjectManager.Get(hits(0).hit_face)
        Dim status As Integer = Nothing
        theUFSession.Modl.AskPointContainment(_Point, face.Tag, status)
        If status = 1 Or status = 3 Then
            _Surface_act = face.Tag
            Dim point_real(2) As Double
            theUFSession.Modl.AskFaceParm2(face.Tag, _Point, _Point_uv, point_real)
        End If

    End Sub

    Private Sub Sub_Point_which_Surface_rule(ByVal Is_Curvature_Output_Points_Filling_Allowed As Boolean,
                                             ByVal _Point As Double(),
                                             ByRef _Surface_Act As Tag,
                                             ByRef _Point_uv As Double(),
                                             ByRef _point_check As Boolean)

        Dim bodyhostpointer = Part_act.RuleManager.GetReferenceText(Body_act)
        Dim rule = "ug_body_askFaceClosestToPoint(" & bodyhostpointer & ", " & "Point(" & _Point(0).ToString.Replace(",", ".") & "," & _Point(1).ToString.Replace(",", ".") & "," + _Point(2).ToString.Replace(",", ".") & "))"
        Dim rulename As String = ""
        theUFSession.Cfi.GetUniqueFilename(rulename)
        Part_act.RuleManager.CreateDynamicRule("root:", rulename, "List", rule, "")

        Dim closefaces As New System.Collections.ArrayList()

        Dim list = Part_act.RuleManager.Evaluate(rulename & ":")
        For Each object_act In list
            closefaces.Add(CType(object_act, Face))
        Next
        Part_act.RuleManager.DeleteDynamicRule("root:", rulename)

        Dim status As Integer = Nothing
        For Each face In closefaces
            theUFSession.Modl.AskPointContainment(_Point, face.Tag, status)
            If status = 1 Or status = 3 Then

                Dim punkt_real(2) As Double
                _Surface_Act = face.Tag
                theUFSession.Modl.AskFaceParm2(_Surface_Act, _Point, _Point_uv, punkt_real)
                If Is_Curvature_Output_Points_Filling_Allowed = False Then
                    _point_check = True
                    Exit For
                Else

                    Dim edgeList As Tag() = Nothing
                    theUFSession.Modl.AskFaceEdges(face.Tag, edgeList)
                    For Each edge_i In edgeList

                        Dim pntEdgeDist As Double = 0.0
                        Dim pntE(2) As Double, pntF(2) As Double
                        Dim acc As Double = 0.0
                        theUFSession.Modl.AskMinimumDist3(1,
                                                          edge_i, NXOpen.Tag.Null,
                                                          0, {0, 0, 0}, 1, _Point,
                                                          pntEdgeDist,
                                                          pntE, pntF, acc)

                        Dim distancesToEdge = Func_DistanceGridDirections(pntF, pntE)
                        If distancesToEdge(0) < delta_R0 / 100 And distancesToEdge(1) < delta_R1 / 100 And distancesToEdge(2) < delta_R2 / 100 Then
                            _point_check = False
                            Exit For
                        Else
                            _point_check = True
                        End If
                    Next
                    If _point_check = False Then
                        Exit For
                    End If
                End If

            End If
        Next


    End Sub

    Private Function Func_Points_Rescue() As List(Of Tuple(Of Integer, Integer, Integer, Double()))

        Dim Points_Box As New HashSet(Of Tuple(Of Integer, Integer, Integer))
        ' Box side centers
        Dim PosR0 As Integer = Floor((Convert.ToDouble(Number_of_R0) - 1) / 2.0)
        Dim PosR1 As Integer = Floor((Convert.ToDouble(Number_of_R1) - 1) / 2.0)
        Dim PosR2 As Integer = Floor((Convert.ToDouble(Number_of_R2) - 1) / 2.0)
        Points_Box.Add(Tuple.Create(Of Integer, Integer, Integer)(PosR0, PosR1, 0))
        Points_Box.Add(Tuple.Create(Of Integer, Integer, Integer)(PosR0, PosR1, Number_of_R2 - 1))
        Points_Box.Add(Tuple.Create(Of Integer, Integer, Integer)(PosR0, 0, PosR2))
        Points_Box.Add(Tuple.Create(Of Integer, Integer, Integer)(PosR0, Number_of_R1 - 1, PosR2))
        Points_Box.Add(Tuple.Create(Of Integer, Integer, Integer)(0, PosR1, PosR2))
        Points_Box.Add(Tuple.Create(Of Integer, Integer, Integer)(Number_of_R0 - 1, PosR1, PosR2))

        Dim RescuePoints As New List(Of Tuple(Of Integer, Integer, Integer, Double()))

        For Each pointCoordinate In Points_Box
            If PointsCloud.ContainsKey(pointCoordinate) Then
                Dim Point_act As Double() = PointsCloud(pointCoordinate)
                RescuePoints.Add(Tuple.Create(Of Integer, Integer, Integer, Double())(
                                 pointCoordinate.Item1, pointCoordinate.Item2, pointCoordinate.Item3,
                                 Point_act))
            End If
        Next

        Func_Points_Rescue = RescuePoints

    End Function
    Private Function Func_CenterPoints(
                                ByVal Is_Curvature_Output_Points_Filling_Allowed As Boolean,
                                ByVal RescuePoints As List(Of Tuple(Of Integer, Integer, Integer, Double())),
                                ByRef List_Point_Grid As List(Of Tag),
                                ByRef Liste_Point_Surface As List(Of Tag)) As HashSet(Of Double())


        Dim Points_Box As New HashSet(Of Tuple(Of Integer, Integer, Integer))
        Dim Surface_tag_act As Tag = Nothing
        Dim uv_act(1) As Double
        Dim Distances_act As List(Of Double) = Nothing
        Dim HashSet_Points_coords_Surface As New HashSet(Of Double())

        For Each RescuePoint In RescuePoints
            Dim pointCoordinate As Tuple(Of Integer, Integer, Integer) = Tuple.Create(Of Integer, Integer, Integer)(
                RescuePoint.Item1, RescuePoint.Item2, RescuePoint.Item3
            )
            Dim Point_act As Double() = RescuePoint.Item4
            Dim Output As Tuple(Of Double(), Double(), Tag, Double()) = Nothing
            Dim min_dist As Double = Nothing, pt_on_obj1(2) As Double, pt_on_obj2(2) As Double, accuracy As Double = Nothing

            theUFSession.Modl.AskMinimumDist3(2, Body_act.Tag, NXOpen.Tag.Null, 0, {0, 0, 0},
                                        1, Point_act, min_dist, pt_on_obj1, pt_on_obj2, accuracy)

            Distances_act = Func_DistanceGridDirections(Point_act, pt_on_obj1)

            Dim Point_Check As Boolean = False
            Sub_Point_which_Surface_rule(False, pt_on_obj1, Surface_tag_act, uv_act, Point_Check)

            If Point_Check = True Then
                Output = Tuple.Create(Of Double(), Double(), Tag, Double())(Point_act, pt_on_obj1, Surface_tag_act, uv_act)
                Dim Rating = Rating_Point(Is_Curvature_Output_Points_Filling_Allowed, Output, pointCoordinate)
                Dim ID As String = Distances_act(0).ToString & "," & Distances_act(1).ToString & "," & Distances_act(2).ToString & "," & Rating.Item2 & "," & pointCoordinate.ToString

                HashSet_Points_coords_Surface.Add(pt_on_obj1)
                If Draft_Mode = True Then
                    Dim point_t As Point = Nothing
                    List_Point_Grid.Add(Func_Point_To_Draw(Point_act, point_t, ID))
                    Sub_Point_Color(point_t, Rating.Item2)
                    Liste_Point_Surface.Add(Func_Point_To_Draw(pt_on_obj1, point_t, ID))

                    Sub_Point_Color(point_t, Rating.Item2)
                End If
                Number_of_krPoints += 1
            End If
        Next
        Func_CenterPoints = HashSet_Points_coords_Surface
    End Function

    Private Sub Sub_Point_which_Surface(ByVal _Point As Double(),
                                               ByRef _Surface_act As Tag,
                                               ByRef _Point_uv As Double())
        Dim Surfaces = Body_act.GetFaces()
        Dim status As Integer = Nothing

        For Each Surface In Surfaces
            theUFSession.Modl.AskPointContainment(_Point, Surface.Tag, status)
            If status = 1 Or status = 3 Then

                _Surface_act = Surface.Tag
                Dim punkt_echt(2) As Double
                theUFSession.Modl.AskFaceParm2(_Surface_act, _Point, _Point_uv, punkt_echt)
                Exit For
            End If
        Next

    End Sub
    Private Function Func_Determine_point_on_surface(ByVal surface As Tag, ByVal uv() As Double) As Double()

        Dim point_on_surface(2) As Double
        Dim u1n(2) As Double
        Dim v1n(2) As Double
        Dim u2n(2) As Double
        Dim v2n(2) As Double
        Dim normaln(2) As Double
        Dim radiin(1) As Double

        theUFSession.Modl.AskFaceProps(surface, uv, point_on_surface, u1n, v1n, u2n, v2n, normaln, radiin)

        Func_Determine_point_on_surface = point_on_surface

    End Function
    Private Sub Sub_Point_Color(ByRef point_t As Point, ByVal Category As String)
        Dim displayModification1 As DisplayModification
        displayModification1 = theSession.DisplayManager.NewDisplayModification()
        displayModification1.ApplyToAllFaces = False
        displayModification1.ApplyToOwningParts = False

        If Category = "k_00" Then
            displayModification1.NewColor = 123 '# orange

        ElseIf Category = "k_p_05" Then
            displayModification1.NewColor = 6 '# yellow

        ElseIf Category = "k_n_05" Then
            displayModification1.NewColor = 75 '# salmon 

        ElseIf Category = "k_p_10" Then
            displayModification1.NewColor = 36 '# green

        ElseIf Category = "k_n_10" Then
            displayModification1.NewColor = 89 '# olive

        ElseIf Category = "k_p_15" Then
            displayModification1.NewColor = 216 '# black

        ElseIf Category = "k_n_15" Then
            displayModification1.NewColor = 189 '# brown

        ElseIf Category = "k_20" Then
            displayModification1.NewColor = 181 '# pink

        ElseIf Category = "k_p_25" Then
            displayModification1.NewColor = 186 '# Red

        ElseIf Category = "k_n_25" Then
            displayModification1.NewColor = 25 '# Lightblue
        End If

        Dim objects2(0) As DisplayableObject
        objects2(0) = point_t
        displayModification1.Apply(objects2)
        displayModification1.Dispose()
    End Sub

    Private Function Func_DistanceGridDirections(ByVal point_1 As Double(), ByVal point_2 As Double()) As List(Of Double)

        Dim point_1_3d = Func_Double_to_Vector3(point_1)
        Dim point_2_3d = Func_Double_to_Vector3(point_2)
        Dim vector12 As Vector3 = point_2_3d - point_1_3d

        Dim projection_1 = Math.Abs(vector12.Dot(DirsSorted(0)))
        Dim projection_2 = Math.Abs(vector12.Dot(DirsSorted(1)))
        Dim projection_3 = Math.Abs(vector12.Dot(DirsSorted(2)))

        Func_DistanceGridDirections = New List(Of Double)({projection_1, projection_2, projection_3})

    End Function


End Module
