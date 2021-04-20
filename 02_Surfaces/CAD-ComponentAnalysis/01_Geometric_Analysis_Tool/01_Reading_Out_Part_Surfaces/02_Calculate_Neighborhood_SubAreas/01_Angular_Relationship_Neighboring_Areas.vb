Imports NXOpen
Imports NXOpen.UF
Imports System.Math
Imports System.Data
Imports SharedModule.Public_Variable
Imports SharedModule.Public_Switch
Imports SharedModule.Typ_Transformations
Imports SharedModule.NX_Functions

Module _01_Angular_relationship_of_neighboring_surfaces

    Public Function Func_Angular_Relationship_AdjacentSurfaces(ByVal _Tag As Tag, ByRef _Neighboring_Surfaces As List(Of Tag), ByVal _Surfaces_Analysis As HashSet(Of Tag), ByRef _Connected_Surfaces As List(Of Tag)) As Boolean

        '# Definition
        Dim Definition_Angle_Level_Transition As Double = 1 '#in Grad

        '# Calculation of the angular relationship of adjacent surfaces. Output as Boolean: True = no adjacent surfaces
        Dim Status_Flat_Surfaces = Func_Calculate_Angle_Relationship(_Tag, Definition_Angle_Level_Transition, _Neighboring_Surfaces)
        '# Analysis of whether all newly connected surfaces were analyzed. + Output of the number of convex / concave boundaries
        '# Status_Flat_Surfaces = True, all adjoining surfaces have been analyzed
        Status_Flat_Surfaces = Funk_Check_Surface_Connection_End_Complete(_Tag, _Surfaces_Analysis, Status_Flat_Surfaces, _Connected_Surfaces)
        Func_Angular_Relationship_AdjacentSurfaces = Status_Flat_Surfaces

    End Function
    Private Function Func_Calculate_Angle_Relationship(ByVal _Tag As Tag, ByVal _Definition_Angle_Level_Transition As Double, ByRef _Neighbouring_Surfaces As List(Of Tag)) As Boolean


        Dim Angle_Level_Transition As Double = (Math.PI / 180) * _Definition_Angle_Level_Transition '#Grad in Rad
        Dim Surface_Neighbour_min As Double = 2000.0
        Dim Surface_Neighbour_min_1 As Double = 200.0
        Dim Surface_Neighbour_min_2 As Double = 1.0
        Dim Number_oF_Convex_Surface As Integer = 0
        Dim Number_oF_Concave_Surface As Integer = 0
        Dim Number_of_Flat_Surfaces As Integer = 0

        Dim Flat_adjacent_Surfaces As New HashSet(Of Tag)
        Dim Not_flat_adjacent_surfaces As New HashSet(Of Tag)
        Dim Neighbouring_Surfaces_List As New HashSet(Of Tag)

        'Dim Flat_adjacent_Surfaces As New List(Of Tag)
        'Dim Not_flat_adjacent_surfaces As New List(Of Tag)
        'Dim Neighbouring_Surfaces_List As New List(Of Tag)

        Dim NXID = Surfaces_NX_Data_Dict.NXID._ValueOutput(_Tag)

        If NXID = 97 Then
            Console.WriteLine("uh")
        End If

        '# Traversing all edges of the current surface
        For Each Edge As KeyValuePair(Of Tag, List(Of Tag)) In Surfaces_NX_Data_Dict.NeighbourSurfaces._ValueOutput(_Tag)
            '# Each adjacent surface is analyzed. NORMALLY only one adjoining surface per edge !!
            For Each Neighbour In Edge.Value
                Dim neighborhood As String = ""
                '# If standard calculation for neighboring surface is not yet calculated

                '# Query whether calculations of the surface relationship between current and Neighbor surface already existing or incorrect
                Dim Tag_array_Surfaces = Tuple.Create(Of Integer, Integer, Integer)(_Tag, Neighbour, Edge.Key)
                Dim Dummy_value_1 As String = Nothing
                Dim Query_norm As Boolean = Neighbouring_Surfaces_relationship.TryGetValue(Tag_array_Surfaces, Dummy_value_1)
                If Query_norm = False Or Dummy_value_1 = "Error" Then
                    Neighbouring_Surfaces_List.Add(Neighbour)

                    Dim Factor_distance_transition_max As Double = 5 '# Distance in mm
                    Dim Factor_distance_transition_min As Double = 0.01
                    Dim Number_of_Iterations_Distance As Double = 3
                    Dim Gradient_distance_waste As Double = 0 '# x²-Function. Only positive values, the higher the flatter
                    Dim Points_on_Edge As Integer = 5  '# must be odd !!

                    '# If standard calculation for neighboring surface is not yet calculated
                    If Not Surfaces_NX_Data_Dict.P_Norm._DictOutput.ContainsKey(Neighbour) Then
                        Surfaces_Analysis_NX(Neighbour)
                    End If
                    Dim Neighbouring_Surface_Area As Double = Surfaces_NX_Data_Dict.Surfacecontents._ValueOutput(Neighbour)
                    If Neighbouring_Surface_Area <= Surface_Neighbour_min_2 Then
                        Factor_distance_transition_max = 0.1 '# Distance in mm
                        Factor_distance_transition_min = 0.01
                        Number_of_Iterations_Distance = 1
                        Gradient_distance_waste = 0 '# x²-Function. Only positive values, the higher the flatter
                        Points_on_Edge = 1  '# must be odd!
                    ElseIf Neighbouring_Surface_Area <= Surface_Neighbour_min_1 Then
                        Factor_distance_transition_max = 1 '# Distance in mm
                        Factor_distance_transition_min = 0.01
                        Number_of_Iterations_Distance = 2
                        Gradient_distance_waste = 0 '# x²-Function. Only positive values, the higher the flatter
                        Points_on_Edge = 1  '# must be odd!
                    ElseIf Neighbouring_Surface_Area <= Surface_Neighbour_min Then
                        Factor_distance_transition_max = 5.0 '# Distance in mm
                        Factor_distance_transition_min = 0.1
                        Number_of_Iterations_Distance = 2
                        Gradient_distance_waste = 0 '# x²-Function. Only positive values, the higher the flatter
                        Points_on_Edge = 3  '# must be odd!
                    End If

                    '# Definition of the evaluation counter for the points on the current edge
                    Dim Number_of_Convex_Neighbour As Integer = 0
                    Dim Number_of_Concave_Neighbour As Integer = 0
                    Dim Number_Plane_Neighbours As Integer = 0
                    Dim Number_of_misaligned_normals_neighbor As Integer = 0

                    '# Create n points on edge
                    For Point As Integer = 1 To Points_on_Edge Step 1
                        '# Parameterized point is created at a discrete distance and derivation is determined in the point
                        Dim Para_act As Double = 0
                        If Points_on_Edge = 1 Then
                            Para_act = 0.5
                        Else
                            Para_act = Math.Round((Point - 1) *
                                                      ((0.95 - 0.05) / (Points_on_Edge - 1)) + 0.05, 2)
                        End If
                        Dim evaluator As IntPtr
                        Dim limits(1) As Double
                        theUFSession.Eval().Initialize(Edge.Key, evaluator)
                        theUFSession.Eval().AskLimits(evaluator, limits)
                        Dim Point_curve = limits(0) + (limits(1) - limits(0)) * Para_act
                        Dim Point_Edge(2) As Double
                        Dim derivatives(2) As Double
                        theUFSession.Eval().Evaluate(evaluator, 1, Point_curve, Point_Edge, derivatives)
                        theUFSession.Eval().Free(evaluator)

                        '# Point parameter on edge is determined for both neighbor surfaces incl. Normal
                        Dim Point_act = Func_Parameter_EdgeDirection(_Tag, Point_Edge)
                        Dim Point_neighbour = Func_Parameter_EdgeDirection(Neighbour, Point_Edge)
                        Dim Norm_act = Func_N_Vector_Point(_Tag, Point_act(0))
                        Dim Norm_neighbour = Func_N_Vector_Point(Neighbour, Point_neighbour(0))

                        '# Direction vector for the offset in the surface, transverse to the derivative on the Edge, is determined and normalized
                        Dim Order As Double
                        Dim Cross_act(2) As Double
                        theUFSession.Vec3.Cross(Norm_act, derivatives, Cross_act)
                        theUFSession.Vec3.Unitize(Cross_act, 0.00001, Order, Cross_act)
                        Dim Cross_neighbour(2) As Double
                        theUFSession.Vec3.Cross(Norm_neighbour, derivatives, Cross_neighbour)
                        theUFSession.Vec3.Unitize(Cross_neighbour, 0.00001, Order, Cross_neighbour)

                        '# Definitions for the calculation
                        Dim Point_act_offset As New List(Of Double())
                        Dim Point_neighbour_offset As New List(Of Double())
                        Dim Iteration As Integer = 0
                        Dim Distance_current As Double = Nothing
                        Dim Norm_act_Offset As Double() = Nothing
                        Dim Norm_neighbour_offset As Double() = Nothing
                        Dim Supportvector_Norm_Offset(2) As Double
                        Dim Angle_between_normal_vectors As Double = Nothing
                        Dim Auxiliary_angle_akt As Double = Nothing
                        Dim Auxiliary_angle_neighbour As Double = Nothing
                        Dim Auxiliary_angle_neighbour_switch As Double = Nothing
                        Dim Auxillary_Vector(2) As Double
                        Dim Switch_Wrong_orientation As Boolean = False
                        Dim Point_io As Boolean = False

                        '# Calculation of the angular relationship of the offset points to the discrete point on the edge.
                        '# If no point is found, the distance of the offset is reduced quadratically to a minimum (definition at the beginning of the function)
                        While Point_io = False
                            If Iteration > Number_of_Iterations_Distance Then
                                Exit While
                            End If
                            Dim Switch_Point_act As Boolean = False
                            Dim Switch_Point_neighbour As Boolean = False
                            '# Control function: If point is not on surface, then mirror direction, if still not, reduce distance.
                            Sub_Create_the_offset_points(Switch_Point_act,
                                                                    Switch_Point_neighbour,
                                                                    Point_act_offset,
                                                                    Point_neighbour_offset,
                                                                    Distance_current,
                                                                    _Tag,
                                                                    Neighbour,
                                                                    Point_act(1),
                                                                    Cross_act,
                                                                    Cross_neighbour,
                                                                    Iteration,
                                                                    Factor_distance_transition_max,
                                                                    Factor_distance_transition_min,
                                                                    Number_of_Iterations_Distance,
                                                                    Gradient_distance_waste)

                            '# Evaluation of the offset points
                            If Switch_Point_act = True And Switch_Point_neighbour = True Then

                                '# Calculate the normals in the point
                                Norm_act_Offset = Func_N_Vector_Point(_Tag,
                                                                            Point_act_offset(0))
                                Norm_neighbour_offset = Func_N_Vector_Point(Neighbour,
                                                                                Point_neighbour_offset(0))

                                '# If current surface is known to be misoriented (definition later), reorientation of the normal by 180 °
                                If Surfaces_NX_Data_Dict.Orientation._ValueOutput(_Tag) = "Wrong" Then
                                    Dim Norm_akt_versetzt_neg(2) As Double
                                    theUFSession.Vec3.Negate(Norm_act_Offset,
                                                                 Norm_akt_versetzt_neg)
                                    Norm_act_Offset = Norm_akt_versetzt_neg
                                End If
                                '# Same for Neighbor
                                Dim Oriention_Neighbour As String = Nothing
                                Dim Oriention_Entry As Boolean = Surfaces_NX_Data_Dict.Orientation._DictOutput.TryGetValue(Neighbour, Oriention_Neighbour)
                                If Oriention_Entry = True And Oriention_Neighbour = "Wrong" Then
                                    Dim Norm_neighbour_offset_neg(2) As Double
                                    theUFSession.Vec3.Negate(Norm_neighbour_offset,
                                                                 Norm_neighbour_offset_neg)
                                    Norm_neighbour_offset = Norm_neighbour_offset_neg
                                End If

                                '# Calculation of the vectors for the evaluation
                                theUFSession.Vec3.Cross(Norm_act_Offset,
                                                            Norm_neighbour_offset,
                                                            Supportvector_Norm_Offset)
                                '# Auxiliary Vector: Vector between the offset points
                                theUFSession.Vec3.Sub(Point_neighbour_offset(1),
                                                          Point_act_offset(1),
                                                          Auxillary_Vector)
                                Dim Support_vector_act(2) As Double
                                theUFSession.Vec3.Cross(Auxillary_Vector,
                                                            Norm_act_Offset,
                                                            Support_vector_act)
                                '# Angle between normal at the offset point on the current surface and the auxiliary vector
                                theUFSession.Vec3.AngleBetween(Auxillary_Vector,
                                                                   Norm_act_Offset,
                                                                   Support_vector_act,
                                                                   Auxiliary_angle_akt)
                                Dim Support_vector_neighbour(2) As Double
                                theUFSession.Vec3.Cross(Auxillary_Vector,
                                                            Norm_neighbour_offset,
                                                            Support_vector_neighbour)
                                '# Angle between normal at the offset point on adjacent surface and the auxiliary vector
                                theUFSession.Vec3.AngleBetween(Auxillary_Vector,
                                                                   Norm_neighbour_offset,
                                                                   Support_vector_neighbour,
                                                                   Auxiliary_angle_neighbour)
                                '# Change angle of the Neighbor normal
                                Auxiliary_angle_neighbour_switch = Math.PI - Auxiliary_angle_neighbour
                                '# Angle between the normals
                                Angle_between_normal_vectors = Math.Abs(Auxiliary_angle_akt - Auxiliary_angle_neighbour)

                                '# Check whether both normals point in the same direction (both surface normals oriented outwards / inwards)
                                '# -> Possibly wrong orientation of the neighboring surface
                                '# If both angles are in the same angle quadrant
                                If (Auxiliary_angle_akt < (Math.PI / 2) And
                                            Auxiliary_angle_neighbour < (Math.PI / 2)) Or
                                            (Auxiliary_angle_akt > (Math.PI / 2) And
                                            Auxiliary_angle_neighbour > (Math.PI / 2)) Then

                                    '# Difference of angles to 90 °, since often in the same quadrant on flat, tangential surfaces
                                    Dim Angle_diff_90_akt = Math.Abs(Auxiliary_angle_akt - 90 * (Math.PI / 180))
                                    Dim Angle_diff_90_neighbour = Math.Abs(Auxiliary_angle_neighbour - 90 * (Math.PI / 180))
                                    '# If the difference is greater than 3 ° then the surface is not flat -> false orientation
                                    If (Angle_diff_90_akt >= 3 * (Math.PI / 180) Or Angle_diff_90_neighbour >= 3 * (Math.PI / 180)) And Angle_between_normal_vectors >= 3 * (Math.PI / 180) Then
                                        '# First reduction of the distance by jumping upwards
                                        '# When distance is minimal, wrong orientation
                                        If Iteration > Number_of_Iterations_Distance Then
                                            Switch_Wrong_orientation = True
                                            Number_of_misaligned_normals_neighbor += 1
                                            Point_io = True
                                        End If
                                    Else
                                        Point_io = True
                                    End If
                                Else
                                    Point_io = True
                                End If
                            End If
                        End While

                        '# Save the angular relationship
                        Dim Score_discrete_point As String = ""
                        Dim Comparison_Angle_Neighbour As Double = Auxiliary_angle_neighbour_switch
                        If Switch_Wrong_orientation = True Then
                            Comparison_Angle_Neighbour = Auxiliary_angle_neighbour
                        End If
                        If Point_io = True Then
                            '# If angle is greater 90 ° + x °, then convex
                            If Auxiliary_angle_akt >= (Math.PI / 2) + Angle_Level_Transition Or Comparison_Angle_Neighbour >= (Math.PI / 2) + Angle_Level_Transition Then '# Konvex
                                Number_of_Convex_Neighbour += 1
                                Score_discrete_point = "Convex"

                                '# If angle is less than 90 ° - x °, then concave
                            ElseIf Auxiliary_angle_akt <= (Math.PI / 2) - Angle_Level_Transition Or Comparison_Angle_Neighbour <= (Math.PI / 2) - Angle_Level_Transition Then '# Konkav
                                Number_of_Concave_Neighbour += 1
                                Score_discrete_point = "Concave"

                                '# Plane
                            Else
                                Number_Plane_Neighbours += 1
                                Score_discrete_point = "Plane"
                            End If
                        End If

                        '# Output the Normal in NX
                        If Output_of_calculation_normal_in_NX = True Then
                            '# Points with correct orientation
                            If Switch_Wrong_orientation = False And Point_io = True Then
                                List_Correct_SurfacesRelationship.Add(Func_Plotting_the_normals_and_angles(Point_act_offset(1), Norm_act_Offset, Point_neighbour_offset(1), Norm_neighbour_offset,
                                                               Auxillary_Vector, Auxiliary_angle_akt * 180 / Math.PI, Score_discrete_point, _Tag, Neighbour, Edge.Key, Supportvector_Norm_Offset, Angle_between_normal_vectors * 180 / Math.PI))
                            Else
                                '# no point found, can move
                                If Norm_act_Offset Is Nothing Or Norm_neighbour_offset Is Nothing Then
                                    List_Wrong_SurfacesRelationship.Add(Func_Plotting_the_normals_and_angles(Point_act_offset(1), Norm_act, Point_neighbour_offset(1), Norm_neighbour,
                                                                                    {1, 1, 1}, 0 * 180 / Math.PI, Score_discrete_point, _Tag, Neighbour, Edge.Key, {1, 1, 1}, 0 * 180 / Math.PI))
                                    '# Neighbor False Oriented
                                Else
                                    List_Wrong_SurfacesRelationship.Add(Func_Plotting_the_normals_and_angles(Point_act_offset(1), Norm_act_Offset, Point_neighbour_offset(1), Norm_neighbour_offset,
                                                                                    Auxillary_Vector, Auxiliary_angle_akt * 180 / Math.PI, Score_discrete_point, _Tag, Neighbour, Edge.Key, Supportvector_Norm_Offset, Angle_between_normal_vectors * 180 / Math.PI))
                                End If
                            End If
                        End If
                        '# Next discrete point
                    Next

                    '# Evaluating all points on Edge, can never be the same, because odd number of points
                    If Number_of_Convex_Neighbour > Number_of_Concave_Neighbour And Number_of_Convex_Neighbour > Number_Plane_Neighbours Then
                        If Not Not_flat_adjacent_surfaces.Contains(Neighbour) Then
                            neighborhood = "Convex"
                            Number_oF_Convex_Surface += 1
                            Not_flat_adjacent_surfaces.Add(Neighbour)
                        End If
                        '# If surface relationship previously declared as plane, delete relationship
                        If Flat_adjacent_Surfaces.Contains(Neighbour) = True Then
                            Flat_adjacent_Surfaces.Remove(Neighbour)
                            Related_Neighbor(_Tag).Remove(Neighbour)
                            Related_Neighbor(Neighbour).Remove(_Tag)
                            Number_of_Flat_Surfaces -= 1
                        End If
                    ElseIf Number_of_Concave_Neighbour > Number_of_Convex_Neighbour And Number_of_Concave_Neighbour > Number_Plane_Neighbours Then
                        If Not Not_flat_adjacent_surfaces.Contains(Neighbour) Then
                            neighborhood = "Concave"
                            Number_oF_Concave_Surface += 1
                            Not_flat_adjacent_surfaces.Add(Neighbour)
                        End If
                        '# If surface relationship previously declared as plane, delete relationship
                        If Flat_adjacent_Surfaces.Contains(Neighbour) = True Then
                            Flat_adjacent_Surfaces.Remove(Neighbour)
                            Related_Neighbor(_Tag).Remove(Neighbour)
                            Related_Neighbor(Neighbour).Remove(_Tag)
                            Number_of_Flat_Surfaces -= 1
                        End If
                    ElseIf Number_Plane_Neighbours <> 0 Then
                        '# If relationship is not already convex or concave
                        If Not_flat_adjacent_surfaces.Contains(Neighbour) = False And Flat_adjacent_Surfaces.Contains(Neighbour) = False Then
                            neighborhood = "Plane"
                            '# If first entry in Global Dict. Related surfaces then definition
                            Dim Dummy_Value As New HashSet(Of Tag)
                            If Related_Neighbor.TryGetValue(_Tag, Dummy_Value) = False Then
                                Related_Neighbor(_Tag) = New HashSet(Of Tag)()
                            End If
                            '# Entry also for Neighbor
                            If Related_Neighbor.TryGetValue(Neighbour, Dummy_Value) = False Then
                                Related_Neighbor(Neighbour) = New HashSet(Of Tag)()
                            End If
                            '# Local list for current surface
                            Flat_adjacent_Surfaces.Add(Neighbour)
                            '# Globale Dictionary
                            Related_Neighbor(_Tag).Add(Neighbour)
                            Related_Neighbor(Neighbour).Add(_Tag)
                            Number_of_Flat_Surfaces += 1
                        End If
                    Else
                        '# Occurs in poorly constructed surfaces
                        neighborhood = "Error"
                    End If

                    '# Save the surface relationship
                    Dim Tag_array_Surfaces_switch = Tuple.Create(Of Integer, Integer, Integer)(Neighbour, _Tag, Edge.Key)
                    Neighbouring_Surfaces_relationship(Tag_array_Surfaces) = neighborhood
                    Neighbouring_Surfaces_relationship(Tag_array_Surfaces_switch) = neighborhood

                    '# Save if surface is misaligned
                    Dim Proportion_of_misaligned_normals_neighbor As Double = Number_of_misaligned_normals_neighbor / Points_on_Edge
                    Dim Orientation_Status As String = Nothing
                    Dim Orientation_Entry = Surfaces_NX_Data_Dict.Orientation._DictOutput.TryGetValue(Neighbour, Orientation_Status)
                    '# If surface has already been analyzed, value will not be overridden
                    If Orientation_Entry = False Then
                        '# When proportion of misaligned offset points on Edge is greater than 60%
                        If Proportion_of_misaligned_normals_neighbor > 0.6 Then
                            Surfaces_NX_Data_Dict.Orientation._Entry(Neighbour, "Wrong")
                        Else
                            Surfaces_NX_Data_Dict.Orientation._Entry(Neighbour, "Correct")
                        End If
                    End If

                Else
                    '# If relationship of the two adjoining surfaces has already been calculated
                    Neighbouring_Surfaces_relationship.TryGetValue(Tag_array_Surfaces, neighborhood)
                    If neighborhood = "Convex" Then
                        If Flat_adjacent_Surfaces.Contains(Neighbour) = True Then
                            Flat_adjacent_Surfaces.Remove(Neighbour)
                            Number_of_Flat_Surfaces -= 1
                        End If
                        Number_oF_Convex_Surface += 1
                        Not_flat_adjacent_surfaces.Add(Neighbour)
                    ElseIf neighborhood = "Concave" Then
                        If Flat_adjacent_Surfaces.Contains(Neighbour) = True Then
                            Flat_adjacent_Surfaces.Remove(Neighbour)
                            Number_of_Flat_Surfaces -= 1
                        End If
                        Number_oF_Concave_Surface += 1
                        Not_flat_adjacent_surfaces.Add(Neighbour)
                    ElseIf neighborhood = "Plane" Then
                        If Not_flat_adjacent_surfaces.Contains(Neighbour) = False Then
                            neighborhood = "Plane"
                            Flat_adjacent_Surfaces.Add(Neighbour)
                            Number_of_Flat_Surfaces += 1
                        End If
                    End If
                End If
            Next
        Next

        '# Entries in the global Flaechen_Daten_Dict
        Surfaces_NX_Data_Dict.Number_Of_Convex._Entry(_Tag, Number_oF_Convex_Surface)
        Surfaces_NX_Data_Dict.number_of_Concave._Entry(_Tag, Number_oF_Concave_Surface)
        Surfaces_NX_Data_Dict.NumberOf_Plane._Entry(_Tag, Number_of_Flat_Surfaces)


        '# If no flat, coherent surface exists, neighbor location can be calculated
        If Number_of_Flat_Surfaces = 0 Then
            Dim Dummy_Value As New HashSet(Of Tag)
            If Related_Neighbor.TryGetValue(_Tag, Dummy_Value) = True Then
                Related_Neighbor.Remove(_Tag)
            End If
            Func_Calculate_Angle_Relationship = True

            '# Otherwise, wait until all related ones are parsed (see Sub_WinkelDownload Count)
        Else
            Func_Calculate_Angle_Relationship = False
        End If
        _Neighbouring_Surfaces.AddRange(Neighbouring_Surfaces_List)

    End Function
    Private Function Funk_Check_Surface_Connection_End_Complete(ByVal _Current_Surface As Tag, ByVal _Analysed_Surfaces As HashSet(Of Tag), ByVal Angular_relationship_status As Boolean, ByRef _Related_Surfaces As List(Of Tag)) As Boolean

        '# If even-adjacent Neighbor Surfaces
        If Angular_relationship_status = False Then
            '# Go through all flat-adjacent surfaces
            Dim Related_Surfaces_zw As New List(Of Tag)
            Dim All_Neighbour_analysed = Func_going_through_neighbor(_Current_Surface, _Analysed_Surfaces, Related_Surfaces_zw)
            If All_Neighbour_analysed = True Then
                Angular_relationship_status = True
                _Related_Surfaces.AddRange(Related_Surfaces_zw.Distinct.ToList)
            End If
        Else
            _Related_Surfaces.Add(_Current_Surface)
        End If
        Funk_Check_Surface_Connection_End_Complete = Angular_relationship_status
    End Function

    '# Calculate sub-functions of the function AngleRelationship:
    Private Function Func_Parameter_EdgeDirection(ByVal _Surface As Tag, ByVal _Point As Double()) As List(Of Double())
        Dim List_zw As New List(Of Double())
        Dim uv_Surface(1) As Double
        Dim Pointt_Control(2) As Double
        theUFSession.Modl.AskFaceParm2(_Surface, _Point, uv_Surface, Pointt_Control)
        List_zw.Add(uv_Surface)
        List_zw.Add(Pointt_Control)
        Func_Parameter_EdgeDirection = List_zw
    End Function
    Private Sub Sub_Create_the_offset_points(ByRef Switch_Point_act As Boolean,
                                                    ByRef Switch_Point_neighbour As Boolean,
                                                    ByRef Point_act_offset As List(Of Double()),
                                                    ByRef Point_neighbour_offset As List(Of Double()),
                                                    ByRef Distance_Current As Double,
                                                    ByVal _Tag As Tag,
                                                    ByVal Neighbour As Tag,
                                                    ByVal Point_act As Double(),
                                                    ByVal Cross_act As Double(),
                                                    ByVal Cross_neighbour As Double(),
                                                    ByRef Iteration As Double,
                                                    ByVal Factor_distance_transition_max As Double,
                                                    ByVal Factor_distance_transition_min As Double,
                                                    ByVal Number_of_Iterations_Distance As Double,
                                                    ByVal Gradient_distance_waste As Double)
        If Number_of_Iterations_Distance = 0 Then
            Distance_Current = Factor_distance_transition_max
            Point_act_offset = Func_Offset__edge_points(_Tag, Point_act, Cross_act, Distance_Current, Switch_Point_act)
            Point_neighbour_offset = Func_Offset__edge_points(Neighbour, Point_act, Cross_neighbour, Distance_Current, Switch_Point_neighbour)
            Iteration += 1
        Else
            While Switch_Point_act = False Or Switch_Point_neighbour = False
                Point_act_offset.Clear()
                Point_neighbour_offset.Clear()

                Distance_Current = Func_Reduce_Distance(Iteration, Factor_distance_transition_max, Factor_distance_transition_min, Number_of_Iterations_Distance, Gradient_distance_waste)

                Point_act_offset = Func_Offset__edge_points(_Tag, Point_act, Cross_act, Distance_Current, Switch_Point_act)
                Point_neighbour_offset = Func_Offset__edge_points(Neighbour, Point_act, Cross_neighbour, Distance_Current, Switch_Point_neighbour)
                If Iteration > Number_of_Iterations_Distance Then
                    Exit While
                End If
            End While
        End If
    End Sub
    Private Function Func_Reduce_Distance(ByRef _Iteration As Double, ByVal _Factor_distance_transition_max As Double, ByVal _Factor_distance_transition_min As Double,
                                              ByVal _Number_of_Iterations_Distance As Double, ByVal _Gradient_distance_waste As Double) As Double
        Dim a As Double = (_Factor_distance_transition_max - _Factor_distance_transition_min) / (_Number_of_Iterations_Distance * (_Number_of_Iterations_Distance + 2 * _Gradient_distance_waste))
        Dim b As Double = -2 * (_Factor_distance_transition_max - _Factor_distance_transition_min) / _Number_of_Iterations_Distance * (1 - (_Gradient_distance_waste / (_Number_of_Iterations_Distance + 2 * _Gradient_distance_waste)))
        Dim c As Double = _Factor_distance_transition_max

        Dim Distance_Current = a * _Iteration ^ 2 + b * _Iteration + c
        _Iteration += 1
        Func_Reduce_Distance = Distance_Current
    End Function
    Private Function Func_Offset__edge_points(ByVal Surface As Tag, ByVal Point As Double(), ByVal Direction As Double(), ByRef Factor_Distance As Double, ByRef Switch_Point As Boolean) As List(Of Double())
        Dim List_zw As New List(Of Double())

        Dim Point_new As New List(Of Double())
        Dim Point_new_Switch As Boolean = False
        Dim _Direction_1 = Direction
        Dim Distance_1 As Double = Nothing
        Dim Status As Integer = Nothing
        Dim Distance_2 As Double = Nothing
        Dim _Direction_2 = Direction
        Dim Tolerance = 0.7

        Dim Switch_Points_Correct_plot As Boolean = False
        Dim Switch_Points_Error_plot As Boolean = False

        Point_new = Func_Point_Manipulator(Surface, Factor_Distance, _Direction_1, Point, Distance_1, Status)

        If Distance_1 < (Factor_Distance * Tolerance) Or Distance_1 > (Factor_Distance * (2 - Tolerance)) Or Status = 2 Then

            '# Passing the first values for plot:
            Dim Point_zw_ue = Point_new(0)
            Dim Point_new_ue = Point_new(2)

            Dim _Factor_Distance_new = -Factor_Distance
            Point_new = Func_Point_Manipulator(Surface, _Factor_Distance_new, _Direction_2, Point, Distance_2, Status)

            If Distance_2 < (Factor_Distance * Tolerance) Or Distance_2 > (Factor_Distance * (2 - Tolerance)) Or Status = 2 Then

                '# Point in geg. Distance not displaceable anyway
                Point_new_Switch = False
                If Switch_Points_Error_plot = True Then
                    Sub_Plot_the_manipulator_Points(Point, Point_zw_ue, Point_new_ue, _Direction_1, Distance_1, Surface)
                End If
                If Switch_Points_Error_plot = True Then
                    Sub_Plot_the_manipulator_Points(Point, Point_new(0), Point_new(2), _Direction_2, Distance_2, Surface)
                End If
            Else
                Point_new_Switch = True
                If Switch_Points_Correct_plot = True Then
                    Sub_Plot_the_manipulator_Points(Point, Point_new(0), Point_new(2), _Direction_2, Distance_2, Surface)
                End If
            End If
        Else
            Point_new_Switch = True
            If Switch_Points_Correct_plot = True Then
                Sub_Plot_the_manipulator_Points(Point, Point_new(0), Point_new(2), _Direction_1, Distance_1, Surface)
            End If
        End If

        Switch_Point = Point_new_Switch
        List_zw.Add(Point_new(1))
        List_zw.Add(Point_new(2))
        Func_Offset__edge_points = List_zw
    End Function
    Private Function Func_Point_Manipulator(ByVal Surface As Tag, ByVal _Factor_Distance As Double, ByRef Direction As Double(), ByVal Point As Double(), ByRef Distance As Double, ByRef Status As Integer) As List(Of Double())
        Dim List_zw As New List(Of Double())
        Dim _Direction(2) As Double
        Dim Point_new(2) As Double

        theUFSession.Vec3.Scale(_Factor_Distance, Direction, _Direction)
        theUFSession.Vec3.Add(Point, _Direction, Point_new)
        Direction = _Direction
        Dim evaluator As IntPtr
        Dim Position_pos3_1_f As New UFEvalsf.Pos3
        theUFSession.Evalsf.Initialize2(Surface, evaluator)
        'theUFSession.Evalsf.AskMinimumFaceDist(evaluator, Point_new, Position_pos3_1_f)
        theUFSession.Evalsf.FindClosestPoint2(evaluator, Point_new, Position_pos3_1_f)
        theUFSession.Evalsf.Free(evaluator)

        List_zw.Add(Point_new)
        List_zw.Add(Position_pos3_1_f.uv)
        List_zw.Add(Position_pos3_1_f.pnt3)

        Distance = Func_Point_Distance(Point, Position_pos3_1_f.pnt3)
        Try
            Status = Func_Control_Point_on_Surface(Surface, Position_pos3_1_f.pnt3)
        Catch ex As Exception
            Status = 0
        End Try


        Func_Point_Manipulator = List_zw
    End Function
    Private Sub Sub_Plot_the_manipulator_Points(ByVal Point As Double(), ByVal Point_zw As Double(), ByVal Point_new As Double(), ByVal Direction As Double(), ByVal Distance As Double, ByVal Surface As Tag)
        Dim Tag_list As New List(Of Tag)

        Dim Point_draw = Func_Point_To_Draw(Point)
        Tag_list.Add(Point_draw)
        Dim Point_zw_draw = Func_Point_To_Draw(Point_zw)
        Tag_list.Add(Point_zw_draw)
        Dim Point_new_draw = Func_Point_To_Draw(Point_new)
        Tag_list.Add(Point_new_draw)
        Dim Normal_draw = Draw_edge_normal_2(Point, Point_new)
        If Not Normal_draw = Tag.Null Then
            Tag_list.Add(Normal_draw)
        End If
        Dim Normal_lang_draw = Draw_edge_normal_1(Point, Direction, 10)
        Tag_list.Add(Normal_lang_draw)

        Dim Tag_array = Tag_list.ToArray

        Dim Name = String.Format("Surfaces {0}, Distance1= {1}", Surface, Distance)
        Sub_Create_FeatureGroup(Tag_array, Name)
    End Sub
    Private Function Func_Plotting_the_normals_and_angles(ByVal Point_akt As Double(), ByVal Normal_akt As Double(),
                                       ByVal Point_neighbour As Double(), ByVal Normal_neighbour As Double(),
                                       ByVal Auxillaryvector As Double(), ByVal Auxillaryangle As Double,
                                       ByVal Result As String, ByVal Surface_akt As Tag, ByVal Surface_neighbour As Tag, ByVal Edge As Tag, ByVal Cross_Angle As Double(), ByVal Between_Angle As Double) As Tag
        Dim Tag_list As New List(Of Tag)

        Dim Point_act_draw = Func_Point_To_Draw(Point_akt)
        Tag_list.Add(Point_act_draw)
        Dim Normal_akt_draw = Draw_edge_normal_1(Point_akt, Normal_akt, 10)
        Tag_list.Add(Normal_akt_draw)
        Dim Point_neighbour_draw = Func_Point_To_Draw(Point_neighbour)
        Tag_list.Add(Point_neighbour_draw)
        Dim Normal_neighbour_draw = Draw_edge_normal_1(Point_neighbour, Normal_neighbour, 10)
        Tag_list.Add(Normal_neighbour_draw)
        Dim Auxillaryvector_draw = Draw_edge_normal_1(Point_akt, Auxillaryvector, 1)
        Tag_list.Add(Auxillaryvector_draw)

        Dim Tag_array = Tag_list.ToArray

        Dim Name = String.Format("Surface {0}-{1}-{2} = {3}, Auxillaryangle= {4}, Crossproduct= [{5},{6},{7}], Temp angle= {8}", Surface_akt, Surface_neighbour, Edge, Result, Auxillaryangle, Cross_Angle(0), Cross_Angle(1), Cross_Angle(2), Between_Angle)
        Func_Plotting_the_normals_and_angles = Func_Create_FeatureGroup(Tag_array, Name)
    End Function
    Private Function Draw_edge_normal_1(ByVal Point As Double(), ByVal Direction As Double(), ByVal Distance As Double) As Tag

        Dim _Direction(2) As Double
        Dim Point_new(2) As Double

        theUFSession.Vec3.Scale(Distance, Direction, _Direction)
        theUFSession.Vec3.Add(Point, _Direction, Point_new)

        Dim StartPoint = Part_act.Points.CreatePoint(Func_Double_to_Point3d(Point))
        Dim EndPoint = Part_act.Points.CreatePoint(Func_Double_to_Point3d(Point_new))
        Dim Linien_Feature As Features.AssociativeLineBuilder
        Dim nullNXOpen_Features_Feature As NXOpen.Features.Feature = Nothing

        Linien_Feature = Part_act.BaseFeatures.CreateAssociativeLineBuilder(nullNXOpen_Features_Feature)
        Linien_Feature.StartPointOptions = Features.AssociativeLineBuilder.StartOption.Point
        Linien_Feature.EndPointOptions = Features.AssociativeLineBuilder.EndOption.Point
        Linien_Feature.StartPoint.Value = StartPoint
        Linien_Feature.EndPoint.Value = EndPoint

        Dim nXObject1 As NXOpen.NXObject
        nXObject1 = Linien_Feature.Commit()
        Draw_edge_normal_1 = nXObject1.Tag
        Linien_Feature.Destroy()

    End Function
    Private Function Draw_edge_normal_2(ByVal Point_1 As Double(), ByVal Point_2 As Double()) As Tag

        Dim Distance = Func_Point_Distance(Point_1, Point_2)
        If Math.Round(Distance, 2) <> 0 Then

            Dim StartPoint = Part_act.Points.CreatePoint(Func_Double_to_Point3d(Point_1))
            Dim EndPoint = Part_act.Points.CreatePoint(Func_Double_to_Point3d(Point_2))
            Dim Linien_Feature As Features.AssociativeLineBuilder
            Dim nullNXOpen_Features_Feature As NXOpen.Features.Feature = Nothing

            Linien_Feature = Part_act.BaseFeatures.CreateAssociativeLineBuilder(nullNXOpen_Features_Feature)
            Linien_Feature.StartPointOptions = Features.AssociativeLineBuilder.StartOption.Point
            Linien_Feature.EndPointOptions = Features.AssociativeLineBuilder.EndOption.Point
            Linien_Feature.StartPoint.Value = StartPoint
            Linien_Feature.EndPoint.Value = EndPoint

            Dim nXObject1 As NXOpen.NXObject
            nXObject1 = Linien_Feature.Commit()
            Draw_edge_normal_2 = nXObject1.Tag
            Linien_Feature.Destroy()
        Else
            Draw_edge_normal_2 = Tag.Null
        End If


    End Function

    Private Function Func_Coordinate_UV(ByVal _Surface As Tag, ByVal u As Double, ByVal v As Double) As Double()
        Dim Point_uv_min_zw As New ModlSrfValue
        '#Inaccurate according to Huebel..Aksfaceprobs possibly better!
        theUFSession.Modl.EvaluateFace(_Surface, 0, {u, v}, Point_uv_min_zw)
        Func_Coordinate_UV = Point_uv_min_zw.srf_pos

    End Function
    Private Function Func_N_Vector_Point(ByVal _Surface As Tag, ByVal _Point_uv As Double()) As Double()
        Dim P_Point(0 To 2), u1(0 To 2), u2(0 To 2), v1(0 To 2), v2(0 To 2), P_Norm(0 To 2), radii(0 To 1), uv_Open_SurfacePoint(2) As Double
        theUFSession.Modl.AskFaceProps(_Surface, _Point_uv, P_Point, u1, v1, u2, v2, P_Norm, radii)
        Func_N_Vector_Point = P_Norm
    End Function

    '# Subfunctions of the Function Func AngleDelete Counting
    Private Function Func_going_through_neighbor(ByVal _Current_Surface As Tag, ByVal _Analysed_Surface As HashSet(Of Tag), ByRef Output_Neighbourelements As List(Of Tag)) As Boolean

        Dim Level_neighbor_list As New HashSet(Of Tag)
        If Related_Neighbor.TryGetValue(_Current_Surface, Level_neighbor_list) = True Then
            If Level_neighbor_list.Count > 0 Then
                For Each Nachbar In Level_neighbor_list
                    If Not Output_Neighbourelements.Contains(Nachbar) Then
                        If _Analysed_Surface.Contains(Nachbar) = False Then
                            Output_Neighbourelements.Add(Nachbar)
                            Func_going_through_neighbor = True
                            Func_going_through_neighbor = Func_going_through_neighbor(Nachbar, _Analysed_Surface, Output_Neighbourelements)
                            If Func_going_through_neighbor = False Then
                                Exit Function
                            End If
                        Else
                            Func_going_through_neighbor = False
                            Exit Function
                        End If
                    Else
                        Func_going_through_neighbor = True
                    End If
                Next
            End If
        End If
    End Function

End Module
