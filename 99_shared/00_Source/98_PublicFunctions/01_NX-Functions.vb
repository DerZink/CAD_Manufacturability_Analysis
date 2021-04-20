Imports NXOpen
Imports System
Imports NXOpen.UF
Imports NXOpen.UI
Imports NXOpen.Utilities
Imports Math_Net = MathNet.Numerics
Public Module NX_Functions
    Dim Database_data As New List(Of Tuple(Of Integer, Integer, Double(), Double, Double, Double(), Double()))
    Public Function Func_NX_ID_ReadingOut(ByVal Tag_input As NXOpen.Tag) As Integer
        Dim ID_info As Int32 = 0
        Dim Handle As String = Nothing
        Dim filedata As String = Nothing
        Dim version As Int32 = 0
        theUFSession.Tag.AskHandleFromTag(Tag_input, Handle)
        theUFSession.Tag.DecomposeHandle(Handle, filedata, ID_info, version)
        Func_NX_ID_ReadingOut = ID_info
    End Function
    Public Sub Sub_Color(ByVal Object_Tag As Tag, ByVal Farbe As Integer)
        theUFSession.Obj.SetColor(Object_Tag, Farbe)
    End Sub

    Public Sub Sub_Create_FeatureGroup(ByVal CurrDate() As Tag, ByVal Name As String, Optional ByVal Status As Integer = 1)
        Dim Group_Name As String = Name
        Dim Group_Tag As Tag = NXOpen.Tag.Null
        theUFSession.Modl.CreateSetOfFeature(Group_Name, CurrDate, CurrDate.Length, Status, Group_Tag)
    End Sub
    Public Function Func_Create_FeatureGroup(ByVal CurrDate() As Tag, ByVal Name As String, Optional ByVal Status As Integer = 1) As Tag
        Dim Group_Name As String = Name
        Dim Group_Tag As Tag = NXOpen.Tag.Null
        theUFSession.Modl.CreateSetOfFeature(Group_Name, CurrDate, CurrDate.Length, Status, Group_Tag)
        Func_Create_FeatureGroup = Group_Tag
    End Function
    Public Function Func_Point_To_Draw(ByVal Vector() As Double, Optional ByRef point As Point = Nothing, Optional ByVal ID As String = "") As Tag
        Dim point_t As NXOpen.Point
        Dim Point3 As NXOpen.Point3d
        Point3.X = Vector(0)
        Point3.Y = Vector(1)
        Point3.Z = Vector(2)
        point_t = Part_act.Points.CreatePoint(Point3)
        point_t.SetVisibility(NXOpen.SmartObject.VisibilityOption.Visible)
        Dim nullNXOpen_Features_Feature As NXOpen.Features.Feature = Nothing
        Dim pointFeatureBuilder1 As NXOpen.Features.PointFeatureBuilder
        pointFeatureBuilder1 = Part_act.BaseFeatures.CreatePointFeatureBuilder(nullNXOpen_Features_Feature)

        pointFeatureBuilder1.Point = point_t
        point = point_t
        Dim nXObject1 As NXOpen.NXObject
        nXObject1 = pointFeatureBuilder1.Commit()
        nXObject1.SetName(ID)
        Func_Point_To_Draw = nXObject1.Tag
        pointFeatureBuilder1.Destroy()
    End Function
    Public Function Func_Draw_Curve(ByVal CurrObject As NXObject) As Tag
        '# Determine the type of curve
        Dim Object_Typ = CurrObject.GetType()

        '# Line:
        If Object_Typ = GetType(Line) Then
            Dim Line_input = CType(CurrObject, Line)
            Dim Startpoint = Part_act.Points.CreatePoint(Line_input.StartPoint)
            Dim Endpoint = Part_act.Points.CreatePoint(Line_input.EndPoint)
            Dim Curve_Features As Features.AssociativeLineBuilder
            Dim nullNXOpen_Features_Feature As NXOpen.Features.Feature = Nothing

            Curve_Features = Part_act.BaseFeatures.CreateAssociativeLineBuilder(nullNXOpen_Features_Feature)
            Curve_Features.StartPointOptions = Features.AssociativeLineBuilder.StartOption.Point
            Curve_Features.EndPointOptions = Features.AssociativeLineBuilder.EndOption.Point
            Curve_Features.StartPoint.Value = Startpoint
            Curve_Features.EndPoint.Value = Endpoint

            Dim nXObject1 As NXOpen.NXObject
            nXObject1 = Curve_Features.Commit()
            Func_Draw_Curve = nXObject1.Tag
            Curve_Features.Destroy()

            '# Spline
        ElseIf Object_Typ = GetType(Spline) Then
            Dim Spline_input = CType(CurrObject, Spline)
            Dim Spline_Feature As Features.StudioSplineBuilderEx
            Dim nullNXOpen_Features_Feature As NXOpen.NXObject = Nothing

            Spline_Feature = Part_act.Features.CreateStudioSplineBuilderEx(nullNXOpen_Features_Feature)
            Spline_Feature.MatchKnotsType = Features.StudioSplineBuilderEx.MatchKnotsTypes.None
            Spline_Feature.InputCurveOption = Features.StudioSplineBuilderEx.InputCurveOptions.Delete
            Spline_Feature.Type = Features.StudioSplineBuilderEx.Types.ThroughPoints

            For Each Spline_Pol In Spline_input.Get3DPoles
                Dim Data = Spline_Feature.ConstraintManager.CreateGeometricConstraintData
                Dim Spline_Point = Part_act.Points.CreatePoint(Spline_Pol)
                Data.Point = Spline_Point
                Spline_Feature.ConstraintManager.Append(Data)
            Next
            Dim nXObject1 As NXOpen.NXObject
            nXObject1 = Spline_Feature.Commit()
            Func_Draw_Curve = nXObject1.Tag
            Spline_Feature.Destroy()

            '# Ellipse
        ElseIf Object_Typ = GetType(Ellipse) Then
            '# Replacement function over Spline, since BUG in NX10
            Dim Ellipse_input = CType(CurrObject, Ellipse)
            Dim Spline_Feature As Features.StudioSplineBuilderEx
            Dim nullNXOpen_Features_Feature As NXOpen.NXObject = Nothing

            Spline_Feature = Part_act.Features.CreateStudioSplineBuilderEx(nullNXOpen_Features_Feature)
            Spline_Feature.MatchKnotsType = Features.StudioSplineBuilderEx.MatchKnotsTypes.None
            Spline_Feature.InputCurveOption = Features.StudioSplineBuilderEx.InputCurveOptions.Delete
            Spline_Feature.Type = Features.StudioSplineBuilderEx.Types.ThroughPoints

            Dim Start_Angle = Ellipse_input.StartAngle
            Dim End_Angle = Ellipse_input.EndAngle
            Dim Origin() As Double = {Ellipse_input.CenterPoint.X, Ellipse_input.CenterPoint.Y, Ellipse_input.CenterPoint.Z}
            Dim Radius_large = Ellipse_input.MajorRadius
            Dim Radius_small = Ellipse_input.MinorRadius
            Dim Orientation = Ellipse_input.Matrix.Element
            Dim Transformationsmatrix_1(11) As Double
            Dim Actual_CSYS = Part_act.WCS.CoordinateSystem.Orientation.Element
            Dim Actual_Ursp = Part_act.WCS.Origin
            Dim Trans_Status As Integer
            Dim Var_0() As Double = {0, 0, 0, 1, 0, 0, 0, 1, 0}
            Dim Var_1() As Double = {Origin(0), Origin(1), Origin(2), Orientation.Xx, Orientation.Xy, Orientation.Xz, Orientation.Yx, Orientation.Yy, Orientation.Yz}
            theUFSession.Trns.CreateCsysMappingMatrix(Var_1, Var_0, Transformationsmatrix_1, Trans_Status)

            Dim Wi_Counter As Integer = 0
            Dim Wi_Step As Double = ((End_Angle - Start_Angle) / 4.0)
            Dim Buffer As Double = 0.0001
            For Wi = Start_Angle To End_Angle + Buffer Step Wi_Step
                Dim Parameter_Temp As Double = Math.Atan(Radius_large / Radius_small * Math.Tan(Wi))
                Dim Sign As Double = 0
                Dim Above As Double = (3 * Math.PI / 2)
                Dim Below As Double = (Math.PI / 2)
                If Wi > Below And Wi <= Above Then
                    Sign = -1
                Else
                    Sign = 1
                End If
                Dim Coordinate() As Double = {0 + Sign * Radius_large * Math.Cos(Parameter_Temp), 0 + Sign * Radius_small * Math.Sin(Parameter_Temp), 0}
                theUFSession.Trns.MapPosition(Coordinate, Transformationsmatrix_1)

                Dim Data = Spline_Feature.ConstraintManager.CreateGeometricConstraintData
                Dim Spline_Point = Part_act.Points.CreatePoint(Func_Double_to_Point3d(Coordinate))
                Data.Point = Spline_Point
                Spline_Feature.ConstraintManager.Append(Data)
            Next
            Dim nXObject1 As NXOpen.NXObject
            nXObject1 = Spline_Feature.Commit()
            Func_Draw_Curve = nXObject1.Tag
            Spline_Feature.Destroy()

            '# Arc
        ElseIf Object_Typ = GetType(Arc) Then
            Dim Arc_input = CType(CurrObject, Arc)
            Dim Arc_Feature As Features.AssociativeArcBuilder
            Dim nullNXOpen_Features_Feature As NXOpen.Features.Feature = Nothing

            Arc_Feature = Part_act.BaseFeatures.CreateAssociativeArcBuilder(nullNXOpen_Features_Feature)
            Arc_Feature.Type = Features.AssociativeArcBuilder.Types.ArcFromCenter

            Dim Angle(1) As Double
            Angle(0) = Arc_input.StartAngle
            Angle(1) = Arc_input.EndAngle
            Dim Origin() As Double = {Arc_input.CenterPoint.X, Arc_input.CenterPoint.Y, Arc_input.CenterPoint.Z}
            Dim Radius = Arc_input.Radius
            Dim Orientation = Arc_input.Matrix.Element
            Dim Transformationsmatrix_1(11) As Double
            Dim Aktual_CSYS = Part_act.WCS.CoordinateSystem.Orientation.Element
            Dim Aktual_Ursp = Part_act.WCS.Origin
            Dim Trans_Status As Integer
            Dim Var_0() As Double = {0, 0, 0, 1, 0, 0, 0, 1, 0}
            Dim Var_1() As Double = {Origin(0), Origin(1), Origin(2), Orientation.Xx, Orientation.Xy, Orientation.Xz, Orientation.Yx, Orientation.Yy, Orientation.Yz}
            theUFSession.Trns.CreateCsysMappingMatrix(Var_1, Var_0, Transformationsmatrix_1, Trans_Status)

            Arc_Feature.CenterPoint.Value = Part_act.Points.CreatePoint(Func_Double_to_Point3d(Origin))
            Arc_Feature.Radius.Value = Radius
            Dim Wi_Counter As Integer = 0
            For Each Wi In Angle
                Dim Coordinate() As Double = {0 + Radius * Math.Cos(Wi), 0 + Radius * Math.Sin(Wi), 0}
                theUFSession.Trns.MapPosition(Coordinate, Transformationsmatrix_1)
                If Wi = 0 Then
                    Arc_Feature.StartPointOptions = Features.AssociativeArcBuilder.StartOption.Point
                    Arc_Feature.StartPoint.Value = Part_act.Points.CreatePoint(Func_Double_to_Point3d(Coordinate))
                Else
                    Arc_Feature.EndPointOptions = Features.AssociativeArcBuilder.EndOption.Point
                    Arc_Feature.EndPoint.Value = Part_act.Points.CreatePoint(Func_Double_to_Point3d(Coordinate))
                End If
                Wi += 1
            Next

            Dim nXObject1 As NXOpen.NXObject
            nXObject1 = Arc_Feature.Commit()
            Func_Draw_Curve = nXObject1.Tag
            Arc_Feature.Destroy()

        End If
    End Function
    Public Function Func_Join_Curves_Together(ByVal section_curve As Features.Feature, ByVal Section_curve_elements() As NXObject, ByRef Joinfeatures() As Tag, ByRef Joincounter As Integer) As NXOpen.Curve()

        '# Transfer of the projected curves to local variables
        Dim Curve_elements_actual = Section_curve_elements
        Dim Curve_elements_Length = Curve_elements_actual.Length
        Dim Func_Curves_Counter As Integer = 0
        Dim Func_Curves_Temp() As NXOpen.Curve = Nothing

        '# Going through all the curves
        Do While Curve_elements_Length > 0

            '# Joining the curves via JoinCurvesBuilder
            Dim nullFeatures_Feature As Features.Feature = Nothing
            Dim joinCurvesBuilder1 As Features.JoinCurvesBuilder
            joinCurvesBuilder1 = Part_act.Features.CreateJoinCurvesBuilder(nullFeatures_Feature)
            joinCurvesBuilder1.DistanceTolerance = 0.01
            joinCurvesBuilder1.AngleTolerance = 0.5
            joinCurvesBuilder1.Section.DistanceTolerance = 0.01
            joinCurvesBuilder1.Section.ChainingTolerance = 0.0095
            joinCurvesBuilder1.Section.AngleTolerance = 0.5
            joinCurvesBuilder1.Section.SetAllowedEntityTypes(Section.AllowTypes.OnlyCurves)
            joinCurvesBuilder1.Section.AllowSelfIntersection(True)

            '# Select all connected curves via CurveFeatureChainRule. First curve element must be given
            Dim features1(0) As NXOpen.Features.Feature
            features1(0) = section_curve
            Dim nullNXOpen_Curve As NXOpen.Curve = Nothing
            Dim curveFeatureChainRule1 As NXOpen.CurveFeatureChainRule
            curveFeatureChainRule1 = Part_act.ScRuleFactory.CreateRuleCurveFeatureChain(features1, Curve_elements_actual(0), nullNXOpen_Curve, False, 0.0095)

            '# Transfer of the selected curves to JoinCurvesBuilder
            Dim rules1(0) As NXOpen.SelectionIntentRule
            rules1(0) = curveFeatureChainRule1
            Dim nullNXOpen_NXObject As NXOpen.NXObject = Nothing
            Dim helpPoint1 As NXOpen.Point3d = New NXOpen.Point3d(0, 0, 0)
            joinCurvesBuilder1.Section.AddToSection(rules1, section_curve, nullNXOpen_NXObject, nullNXOpen_NXObject, helpPoint1, NXOpen.Section.Mode.Create, False)
            '# Determination of the number of selected curves
            Dim CurvesinSection() As NXObject = Nothing
            joinCurvesBuilder1.Section.GetOutputCurves(CurvesinSection)
            Dim CurvesinSection_Length = CurvesinSection.Length
            rules1(0).Dispose()

            '# Create an NXObject through curves
            '# For several (merged) curves:
            If CurvesinSection_Length > 1 Then
                '# Create the NXObject
                Dim nXObject1 As NXOpen.NXObject
                nXObject1 = joinCurvesBuilder1.Commit()
                '# Passing the merged curves to join features to create FeatureGroup in NX
                Dim joincurves1 As Features.JoinCurves = Nothing
                joincurves1 = CType(nXObject1, Features.JoinCurves)
                ReDim Preserve Joinfeatures(Joincounter)
                Joinfeatures(Joincounter) = joincurves1.Tag
                joinCurvesBuilder1.Destroy()
                '# Transfer of merged curves to function output (joincurves1 has an entry)
                Dim JoinCurveElemente() As NXObject = joincurves1.GetEntities()
                ReDim Preserve Func_Curves_Temp(Func_Curves_Counter)
                Func_Curves_Temp(Func_Curves_Counter) = JoinCurveElemente(0)

                '# At a curve:
            ElseIf CurvesinSection_Length = 1 Then
                '# "Drawing" the curve over its own function
                Dim Tag_Curve = Func_Draw_Curve(CurvesinSection(0))
                '# Transfer of the combined curves to the function output
                Dim Curves_Feature As Features.Feature = NXOpen.Utilities.NXObjectManager.Get(Tag_Curve)
                Dim CurveElemente() As NXObject = Curves_Feature.GetEntities()
                ReDim Preserve Func_Curves_Temp(Func_Curves_Counter)
                Func_Curves_Temp(Func_Curves_Counter) = CurveElemente(0)
                '# Passing the curve to join features to create FeatureGroup in NX
                ReDim Preserve Joinfeatures(Joincounter)
                Joinfeatures(Joincounter) = Tag_Curve
                joinCurvesBuilder1.Destroy()
            End If

            '# Remove already used curves from CurveArray of the projected curves (Curve_elements_actual)
            Dim CurvesinSection_Positions() As Integer
            '# Create an array with all elements up to a place (eg place 7 -> [0,1,2,3,4,5,6])
            CurvesinSection_Positions = Enumerable.Range(0, CurvesinSection_Length).ToArray
            Func_Array_Element_Delete(Curve_elements_actual, CurvesinSection_Positions)
            Curve_elements_Length = Curve_elements_actual.Length
            Joincounter += 1
            Func_Curves_Counter += 1
        Loop
        Func_Join_Curves_Together = Func_Curves_Temp

    End Function
    Public Sub Func_Array_Element_Delete(ByRef Array As NXObject(), ByVal Elements() As Integer)
        Dim u_Limit = Array.GetLowerBound(0)
        Dim o_Limit = Array.GetUpperBound(0)
        Dim Index_Counter As Integer = 0
        Dim Elements_x() As Integer = Nothing

        For Each Index In Elements
            If Index < u_Limit OrElse Index > o_Limit Then
                Console.WriteLine(String.Format("Deleting the element from array is not possible. Index {0} out of range {1} to {2}!", Index, u_Limit, o_Limit))
            Else
                Dim Index_Actual = Index - Index_Counter
                Array = Array.Except({Array(Index_Actual)}).ToArray
                Index_Counter += 1
            End If
        Next

    End Sub

    Public Function Func_Curve_From_Edge(ByVal Kante_ As Edge) As NXOpen.Features.CompositeCurve

        Dim theEdgeToDumbRule(0) As Edge

        Dim helpPoint As NXOpen.Point3d = New NXOpen.Point3d(0.0, 0.0, 0.0)

        Dim nullNXOpen_Features_Feature As NXOpen.Features.Feature = Nothing
        Dim compositeCurveBuilder As NXOpen.Features.CompositeCurveBuilder = theSession.Parts.Work.Features.CreateCompositeCurveBuilder(nullNXOpen_Features_Feature)

        compositeCurveBuilder.Tolerance = 0.01
        compositeCurveBuilder.Associative = True
        compositeCurveBuilder.FixAtCurrentTimestamp = True
        compositeCurveBuilder.HideOriginal = False
        compositeCurveBuilder.InheritDisplayProperties = False
        compositeCurveBuilder.JoinOption = NXOpen.Features.CompositeCurveBuilder.JoinMethod.Genernal
        compositeCurveBuilder.Section.ChainingTolerance = 0.0095

        theEdgeToDumbRule(0) = Kante_
        Dim EdgeDumbRule As NXOpen.EdgeDumbRule = theSession.Parts.Work.ScRuleFactory.CreateRuleEdgeDumb(theEdgeToDumbRule)

        Dim rules(0) As NXOpen.SelectionIntentRule
        rules(0) = EdgeDumbRule

        compositeCurveBuilder.Section.AddToSection(rules, Kante_, Nothing, Nothing, helpPoint, NXOpen.Section.Mode.Create, False)
        Func_Curve_From_Edge = compositeCurveBuilder.Commit()
        compositeCurveBuilder.Destroy()

    End Function

    Public Function Func_Isoparametric_Curve_Create(ByVal _Surface As Tag, ByVal direction As String, ByVal _Number_of_directions As Integer) As Dictionary(Of Tag, Double)

        Dim Curve_List_zw As New List(Of Tag)
        Dim Curve_Dict As New Dictionary(Of Tag, Double)
        Dim Opposite_Direction As String = "U"
        If direction = "U" Then
            Opposite_Direction = "V"
        End If
        _Number_of_directions -= 1

        Dim uvminmax(3) As Double
        theUFSession.Modl.AskFaceUvMinmax(_Surface, uvminmax)
        Dim uvminmax_dict As New Dictionary(Of String, Double())
        uvminmax_dict("U") = {uvminmax(0), uvminmax(1)}
        uvminmax_dict("V") = {uvminmax(2), uvminmax(3)}
        Dim Increment_uv As New Dictionary(Of String, Double)
        Increment_uv("U") = Math.Abs(uvminmax(1) - uvminmax(0)) / _Number_of_directions
        Increment_uv("V") = Math.Abs(uvminmax(3) - uvminmax(2)) / _Number_of_directions
        Dim P_Point_0(0 To 2), P_Point_1(0 To 2), u1(0 To 2), u2(0 To 2), v1(0 To 2), v2(0 To 2), P_Norm(0 To 2), radii(0 To 1) As Double

        Dim Number_of_Point_OppositeDirection_StartValue = 5
        Dim Number_of_Point_OppositeDirection_max = 50
        Dim Number_of_Point_OppositeDirection_EndValue = 5 '# mm
        Dim i = uvminmax_dict(direction)(0)
        Dim i_counter = 0
        Do While i >= uvminmax_dict(direction)(0) And i <= uvminmax_dict(direction)(1)
            Try
                '# Calculate increment in opposite direction
                Dim increment_in_opposite_direction = Math.Abs(uvminmax_dict(Opposite_Direction)(0) - uvminmax_dict(Opposite_Direction)(1)) / Number_of_Point_OppositeDirection_StartValue
                Dim Number_of_Point_OppositeDirection_current As Integer = Number_of_Point_OppositeDirection_StartValue
                Dim uv_length_0() As Double = {i, uvminmax_dict(Opposite_Direction)(0)}
                Dim uv_length_1() As Double = {i, uvminmax_dict(Opposite_Direction)(0) + increment_in_opposite_direction}
                If direction = "V" Then
                    uv_length_0 = {uvminmax_dict(Opposite_Direction)(0), i}
                    uv_length_1 = {uvminmax_dict(Opposite_Direction)(0) + increment_in_opposite_direction, i}
                End If
                theUFSession.Modl.AskFaceProps(_Surface, uv_length_0, P_Point_0, u1, v1, u2, v2, P_Norm, radii)
                theUFSession.Modl.AskFaceProps(_Surface, uv_length_1, P_Point_1, u1, v1, u2, v2, P_Norm, radii)

                Dim Length_opposite_direction As Double = Func_Point_Distance(P_Point_0, P_Point_1)
                If Length_opposite_direction > Number_of_Point_OppositeDirection_EndValue Then
                    Dim Multiple_distance_currently = Length_opposite_direction / Number_of_Point_OppositeDirection_EndValue
                    increment_in_opposite_direction = increment_in_opposite_direction / Multiple_distance_currently
                    Number_of_Point_OppositeDirection_current = Math.Abs(uvminmax_dict(Opposite_Direction)(0) - uvminmax_dict(Opposite_Direction)(1)) / increment_in_opposite_direction
                    If Number_of_Point_OppositeDirection_current > Number_of_Point_OppositeDirection_max Then
                        increment_in_opposite_direction = Math.Abs(uvminmax_dict(Opposite_Direction)(0) - uvminmax_dict(Opposite_Direction)(1)) / Number_of_Point_OppositeDirection_max
                        Number_of_Point_OppositeDirection_current = Number_of_Point_OppositeDirection_max
                    End If
                End If

                '# Spline on Surfaces
                Dim studioSplineBuilderEx1 As NXOpen.Features.StudioSplineBuilderEx
                Dim nullNXOpen_NXObject As NXOpen.NXObject = Nothing
                studioSplineBuilderEx1 = Part_act.Features.CreateStudioSplineBuilderEx(nullNXOpen_NXObject)
                Dim j = uvminmax_dict(Opposite_Direction)(0)
                Dim j_counter As Integer = 0
                Do While j >= uvminmax_dict(Opposite_Direction)(0) And j <= uvminmax_dict(Opposite_Direction)(1) + increment_in_opposite_direction / 3

                    Dim uv() As Double = {i, j}
                    If direction = "V" Then
                        uv = {j, i}
                    End If

                    theUFSession.Modl.AskFaceProps(_Surface, uv, P_Point_0, u1, v1, u2, v2, P_Norm, radii)

                    Dim point1 As NXOpen.Point
                    point1 = Part_act.Points.CreatePoint(Func_Double_to_Point3d(P_Point_0))
                    Dim geometricConstraintData1 As NXOpen.Features.GeometricConstraintData
                    geometricConstraintData1 = studioSplineBuilderEx1.ConstraintManager.CreateGeometricConstraintData()
                    geometricConstraintData1.Point = point1
                    geometricConstraintData1.CanInferConstraintFromAttachmentParent = True
                    geometricConstraintData1.AutomaticConstraintType = NXOpen.Features.GeometricConstraintData.AutoConstraintType.Tangent
                    geometricConstraintData1.AutomaticConstraintDirection = NXOpen.Features.GeometricConstraintData.ParameterDirection.Iso
                    studioSplineBuilderEx1.ConstraintManager.Append(geometricConstraintData1)
                    j += increment_in_opposite_direction
                    j_counter += 1
                    If j_counter = Number_of_Point_OppositeDirection_current Then
                        j = uvminmax_dict(Opposite_Direction)(1)
                    End If

                Loop
                Dim feature1 As Features.Feature
                feature1 = studioSplineBuilderEx1.CommitFeature()
                Curve_Dict.Add(feature1.Tag, i)
            Catch ex As Exception
            End Try

            i += Increment_uv(direction)
            i_counter += 1
            If i_counter = _Number_of_directions Then
                i = uvminmax_dict(direction)(1)
            End If

        Loop

        Func_Isoparametric_Curve_Create = Curve_Dict
    End Function

    Public Function Func_Isoparametric_Curve_Create_2(ByVal _Surface As Tag, ByVal direction As String, ByVal _Number_of_directions As Integer) As Dictionary(Of Tag, Double)

        Dim Curve_List_zw As New List(Of Tag)
        Dim Curve_dict As New Dictionary(Of Tag, Double)
        Dim opposite_direction As String = "U"
        If direction = "U" Then
            opposite_direction = "V"
        End If
        _Number_of_directions -= 1

        Dim uvminmax(3) As Double
        theUFSession.Modl.AskFaceUvMinmax(_Surface, uvminmax)
        Dim uvminmax_dict As New Dictionary(Of String, Double())
        uvminmax_dict("U") = {uvminmax(0), uvminmax(1)}
        uvminmax_dict("V") = {uvminmax(2), uvminmax(3)}
        Dim increment_uv As New Dictionary(Of String, Double)
        increment_uv("U") = Math.Abs(uvminmax(1) - uvminmax(0)) / _Number_of_directions
        increment_uv("V") = Math.Abs(uvminmax(3) - uvminmax(2)) / _Number_of_directions
        Dim P_Point_0(0 To 2), P_Point_1(0 To 2), u1(0 To 2), u2(0 To 2), v1(0 To 2), v2(0 To 2), P_Norm(0 To 2), radii(0 To 1) As Double

        Dim Number_of_Point_OppositeDirection_StartValue = 5
        Dim Number_of_Point_OppositeDirection_max = 50
        Dim Distance_OppositeDirection_EndValue = 5 '# mm
        Dim i = uvminmax_dict(direction)(0)
        Dim i_counter = 0

        Dim nullNXOpen_Features_IsoparametricCurves As NXOpen.Features.IsoparametricCurves = Nothing

        Dim isoparametricCurvesBuilder1 As NXOpen.Features.IsoparametricCurvesBuilder = Nothing
        isoparametricCurvesBuilder1 = Part_act.Features.CreateIsoparametricCurvesBuilder(nullNXOpen_Features_IsoparametricCurves)

        If direction = "U" Then
            isoparametricCurvesBuilder1.Direction = NXOpen.Features.IsoparametricCurvesBuilder.DirectionTypes.IsoU
        Else
            isoparametricCurvesBuilder1.Direction = NXOpen.Features.IsoparametricCurvesBuilder.DirectionTypes.IsoV
        End If
        isoparametricCurvesBuilder1.Number = _Number_of_directions
        isoparametricCurvesBuilder1.Spacing = 0.0001


        Do While i >= uvminmax_dict(direction)(0) And i <= uvminmax_dict(direction)(1)
            Try
                '# Calculate increment in opposite direction
                Dim increment_in_opposite_direction = Math.Abs(uvminmax_dict(opposite_direction)(0) - uvminmax_dict(opposite_direction)(1)) / Number_of_Point_OppositeDirection_StartValue
                Dim Number_of_Point_OppositeDirection_Currently As Integer = Number_of_Point_OppositeDirection_StartValue
                Dim uv_length_0() As Double = {i, uvminmax_dict(opposite_direction)(0)}
                Dim uv_length_1() As Double = {i, uvminmax_dict(opposite_direction)(0) + increment_in_opposite_direction}
                If direction = "V" Then
                    uv_length_0 = {uvminmax_dict(opposite_direction)(0), i}
                    uv_length_1 = {uvminmax_dict(opposite_direction)(0) + increment_in_opposite_direction, i}
                End If
                theUFSession.Modl.AskFaceProps(_Surface, uv_length_0, P_Point_0, u1, v1, u2, v2, P_Norm, radii)
                theUFSession.Modl.AskFaceProps(_Surface, uv_length_1, P_Point_1, u1, v1, u2, v2, P_Norm, radii)

                Dim Length_opposite_direction As Double = Func_Point_Distance(P_Point_0, P_Point_1)
                If Length_opposite_direction > Distance_OppositeDirection_EndValue Then
                    Dim Multiple_distance_currently = Length_opposite_direction / Distance_OppositeDirection_EndValue
                    increment_in_opposite_direction = increment_in_opposite_direction / Multiple_distance_currently
                    Number_of_Point_OppositeDirection_Currently = Math.Abs(uvminmax_dict(opposite_direction)(0) - uvminmax_dict(opposite_direction)(1)) / increment_in_opposite_direction
                    If Number_of_Point_OppositeDirection_Currently > Number_of_Point_OppositeDirection_max Then
                        increment_in_opposite_direction = Math.Abs(uvminmax_dict(opposite_direction)(0) - uvminmax_dict(opposite_direction)(1)) / Number_of_Point_OppositeDirection_max
                        Number_of_Point_OppositeDirection_Currently = Number_of_Point_OppositeDirection_max
                    End If
                End If

                '# Spline auf Flaeche
                Dim studioSplineBuilderEx1 As NXOpen.Features.StudioSplineBuilderEx
                Dim nullNXOpen_NXObject As NXOpen.NXObject = Nothing
                studioSplineBuilderEx1 = Part_act.Features.CreateStudioSplineBuilderEx(nullNXOpen_NXObject)
                Dim j = uvminmax_dict(opposite_direction)(0)
                Dim j_counter As Integer = 0
                Do While j >= uvminmax_dict(opposite_direction)(0) And j <= uvminmax_dict(opposite_direction)(1) + increment_in_opposite_direction / 3

                    Dim uv() As Double = {i, j}
                    If direction = "V" Then
                        uv = {j, i}
                    End If

                    theUFSession.Modl.AskFaceProps(_Surface, uv, P_Point_0, u1, v1, u2, v2, P_Norm, radii)

                    Dim point1 As NXOpen.Point
                    point1 = Part_act.Points.CreatePoint(Func_Double_to_Point3d(P_Point_0))
                    Dim geometricConstraintData1 As NXOpen.Features.GeometricConstraintData
                    geometricConstraintData1 = studioSplineBuilderEx1.ConstraintManager.CreateGeometricConstraintData()
                    geometricConstraintData1.Point = point1
                    geometricConstraintData1.CanInferConstraintFromAttachmentParent = True
                    geometricConstraintData1.AutomaticConstraintType = NXOpen.Features.GeometricConstraintData.AutoConstraintType.Tangent
                    geometricConstraintData1.AutomaticConstraintDirection = NXOpen.Features.GeometricConstraintData.ParameterDirection.Iso
                    studioSplineBuilderEx1.ConstraintManager.Append(geometricConstraintData1)
                    j += increment_in_opposite_direction
                    j_counter += 1
                    If j_counter = Number_of_Point_OppositeDirection_Currently Then
                        j = uvminmax_dict(opposite_direction)(1)
                    End If

                Loop

                Dim feature1 As Features.Feature
                feature1 = studioSplineBuilderEx1.CommitFeature()
                Curve_dict.Add(feature1.Tag, i)
            Catch ex As Exception
            End Try

            i += increment_uv(direction)
            i_counter += 1
            If i_counter = _Number_of_directions Then
                i = uvminmax_dict(direction)(1)
            End If

        Loop

        Func_Isoparametric_Curve_Create_2 = Curve_dict
    End Function

    Public Function Func_Curve_trim_Edge(ByVal _Curve As Features.StudioSpline, ByVal _Surface As Tag) As Tag

        Dim Curve_Spline As Spline = CType(_Curve.FindObject("CURVE 1"), NXOpen.Spline)
        Dim nullNXOpen_Features_TrimCurve As NXOpen.Features.TrimCurve = Nothing
        Dim trimCurveBuilder1 As NXOpen.Features.TrimCurveBuilder
        trimCurveBuilder1 = Part_act.Features.CreateTrimCurveBuilder(nullNXOpen_Features_TrimCurve)
        trimCurveBuilder1.InteresectionDirectionOption = NXOpen.Features.TrimCurveBuilder.InteresectionDirectionOptions.Shortest3dDistance
        trimCurveBuilder1.CurvesToTrim.SetAllowedEntityTypes(NXOpen.Section.AllowTypes.OnlyCurves)

        Dim curves1(0) As NXOpen.IBaseCurve
        curves1(0) = Curve_Spline
        Dim curveDumbRule1 As NXOpen.CurveDumbRule
        curveDumbRule1 = Part_act.ScRuleFactory.CreateRuleBaseCurveDumb(curves1)
        trimCurveBuilder1.CurvesToTrim.AllowSelfIntersection(True)
        Dim rules1(0) As NXOpen.SelectionIntentRule
        rules1(0) = curveDumbRule1
        Dim nullNXOpen_NXObject As NXOpen.NXObject = Nothing
        Dim helpPoint1 As NXOpen.Point3d = New NXOpen.Point3d(0, 0, 0)
        trimCurveBuilder1.CurvesToTrim.AddToSection(rules1, Curve_Spline, nullNXOpen_NXObject, nullNXOpen_NXObject, helpPoint1, NXOpen.Section.Mode.Create, False)

        Dim Trim_Point As New Dictionary(Of String, Tuple(Of Double, Double(), Tag))
        Trim_Point("min") = New Tuple(Of Double, Double(), Tag)(Double.PositiveInfinity, {0, 0, 0}, 0)
        Trim_Point("max") = New Tuple(Of Double, Double(), Tag)(Double.NegativeInfinity, {0, 0, 0}, 0)
        For Each Edge In Surfaces_NX_Data_Dict.Edge._ValueOutput(_Surface)
            Dim Number_of_Slices As Integer
            Dim Output_Slices() As Double = Nothing
            theUFSession.Modl.IntersectCurveToCurve(Curve_Spline.Tag, Edge, Number_of_Slices, Output_Slices)
            For i = 1 To Number_of_Slices Step 1
                Dim Point_zw() As Double = ({Output_Slices((i - 1) * 5 + 0), Output_Slices((i - 1) * 5 + 1), Output_Slices((i - 1) * 5 + 2)})
                Dim Para_zw As Double = Output_Slices((i - 1) * 5 + 4)
                If Para_zw < Trim_Point("min").Item1 Then
                    Trim_Point("min") = New Tuple(Of Double, Double(), Tag)(Para_zw, Point_zw, Edge)
                End If
                If Para_zw > Trim_Point("max").Item1 Then
                    Trim_Point("max") = New Tuple(Of Double, Double(), Tag)(Para_zw, Point_zw, Edge)
                End If
            Next
        Next
        If Trim_Point("min").Item3 <> 0 And Trim_Point("max").Item3 <> 0 Then
            Dim Edge_1_array(0) As Edge
            Dim Edge_1 As Edge = theUFSession.GetObjectManager.GetTaggedObject(Trim_Point("min").Item3)
            Edge_1_array(0) = Edge_1
            Dim edgeDumbRule1 As NXOpen.EdgeDumbRule
            edgeDumbRule1 = Part_act.ScRuleFactory.CreateRuleEdgeDumb(Edge_1_array)
            Dim section1 As NXOpen.Section
            section1 = Part_act.Sections.CreateSection(0.0095, 0.01, 0.5)
            Dim rules2(0) As NXOpen.SelectionIntentRule
            rules2(0) = edgeDumbRule1
            nullNXOpen_NXObject = Nothing
            section1.AddToSection(rules2, Edge_1, nullNXOpen_NXObject, nullNXOpen_NXObject, helpPoint1, NXOpen.Section.Mode.Create, False)
            trimCurveBuilder1.FirstBoundingObject.Add(section1)
            trimCurveBuilder1.FirstBoundingObjectPickPoint = Func_Double_to_Point3d(Trim_Point("min").Item2)

            Dim Edge_2_array(0) As Edge
            Dim Edge_2 As Edge = theUFSession.GetObjectManager.GetTaggedObject(Trim_Point("max").Item3)
            Edge_2_array(0) = Edge_2
            Dim edgeDumbRule2 As NXOpen.EdgeDumbRule
            edgeDumbRule2 = Part_act.ScRuleFactory.CreateRuleEdgeDumb(Edge_2_array)
            Dim section2 As NXOpen.Section
            section2 = Part_act.Sections.CreateSection(0.0095, 0.01, 0.5)
            Dim rules3(0) As NXOpen.SelectionIntentRule
            rules3(0) = edgeDumbRule2
            nullNXOpen_NXObject = Nothing
            section2.AddToSection(rules3, Edge_2, nullNXOpen_NXObject, nullNXOpen_NXObject, helpPoint1, NXOpen.Section.Mode.Create, False)
            trimCurveBuilder1.SecondBoundingObject.Add(section2)
            trimCurveBuilder1.SecondBoundingObjectPickPoint = Func_Double_to_Point3d(Trim_Point("max").Item2)

            trimCurveBuilder1.CurveTrimRegionOption = NXOpen.Features.TrimCurveBuilder.CurveTrimRegionOptions.Outside
            Try
                Dim nXObject1 As NXOpen.NXObject
                nXObject1 = trimCurveBuilder1.Commit()
                Func_Curve_trim_Edge = nXObject1.Tag
                trimCurveBuilder1.Destroy()
            Catch ex As Exception
                Func_Curve_trim_Edge = _Curve.Tag
                trimCurveBuilder1.Destroy()
                Exit Function
            End Try

            Exit Function
        End If
        Func_Curve_trim_Edge = _Curve.Tag
        trimCurveBuilder1.Destroy()
        Exit Function


    End Function

    Public Function Func_Array_compare(ByVal _Array_1 As Double(), ByVal _Array_2 As Double(), ByVal _Accuracy As Integer) As Boolean
        Dim Equal = True
        Dim Length_1 As Integer = _Array_1.Count
        Dim Length_2 As Integer = _Array_2.Count
        If Length_1 <> Length_2 Then
            Equal = False
        Else
            Dim Entry_point As Integer = 0
            For Entry_point = 0 To Length_1 - 1 Step 1
                If Math.Round(_Array_1(Entry_point), _Accuracy) <> Math.Round(_Array_2(Entry_point), _Accuracy) Then
                    Equal = False
                    Exit For
                End If
                Entry_point += 1
            Next
        End If
        Func_Array_compare = Equal

    End Function

    Public Function Func_Point_Distance(ByVal Punkt_1 As Object, ByVal Punkt_2 As Object) As Double
        Dim Distance As Double
        Dim Point1_() As Double = Punkt_1
        Dim Point2_() As Double = Punkt_2
        Distance = Math.Sqrt((Point1_(0) - Point2_(0)) ^ 2 + (Point1_(1) - Point2_(1)) ^ 2 + (Point1_(2) - Point2_(2)) ^ 2)

        Func_Point_Distance = Distance
    End Function
    Public Function Func_Control_Point_on_Surface(ByVal _Surface As Tag, ByVal _Point As Double()) As Integer
        Dim Status As Integer
        theUFSession.Modl.AskPointContainment(_Point, _Surface, Status)
        Func_Control_Point_on_Surface = Status
    End Function
    ' 02 End 

End Module