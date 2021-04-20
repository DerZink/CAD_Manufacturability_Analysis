Imports NXOpen
Imports System
Imports NXOpen.UF
Imports NXOpen.UI
Imports NXOpen.Utilities
Imports Math_Net = MathNet.Numerics
Imports SharedModule.Public_Variable
Imports SharedModule.Typ_Transformations

Public Module Mod_Boundingbox_General_Func

    Public Function Func_Calculate_Box_Volume(ByVal Length() As Double) As Double
        Func_Calculate_Box_Volume = Length(0) * Length(1) * Length(2)
    End Function
    Public Sub Sub_Box_Boundingpoints_Create(ByVal X_Axis As Vector3d, ByVal Y_Axis As Vector3d,
                                            ByVal create As Boolean)
        Dim Vertex_1(2) As Double
        Dim Vertex_2(2) As Double
        Dim Dirs(2, 2) As Double
        Dim Body_Tag(0) As NXOpen.Tag
        Body_Tag(0) = Body_act.Tag
        Dim Focuspoint_ACS As New Point3d(0.0, 0.0, 0.0)
        Dim Gen_coordsys_ACS As NXOpen.CartesianCoordinateSystem
        Gen_coordsys_ACS = Part_act.CoordinateSystems.CreateCoordinateSystem(Focuspoint_ACS, X_Axis, Y_Axis)
        theUFSession.Modl.AskBoundingBoxExact(Body_Tag(0), Gen_coordsys_ACS.Tag, Vertex_1, Dirs, Deltas)

        RoundArrays_oneDim(Deltas)

        '# sorting box axes by length
        Dim DeltasTuple As List(Of Tuple(Of Integer, Double)) = New List(Of Tuple(Of Integer, Double)) From {Tuple.Create(0, Deltas(0)), Tuple.Create(1, Deltas(1)), Tuple.Create(2, Deltas(2))}
        Dim DeltasTupleSorted = DeltasTuple.OrderByDescending(Function(x) x.Item2)
        Dim DeltasSorted() As Double = {DeltasTupleSorted(0).Item2, DeltasTupleSorted(1).Item2, DeltasTupleSorted(2).Item2}

        '# Transform to sorted Vector3 list 
        Dim DirsList As List(Of VectorArithmetic.Vector3) = Func_Double2DArray_toVector3List(Dirs)
        DirsSorted = New List(Of VectorArithmetic.Vector3) From {DirsList(DeltasTupleSorted(0).Item1), DirsList(DeltasTupleSorted(1).Item1), DirsList(DeltasTupleSorted(2).Item1)}

        '# First corner of the box is created (ACS)
        Dim Vertex_1_vec = Func_Double_to_Vector3(Vertex_1)
        RoundVector3(Vertex_1_vec)

        '# Calculate all corner points of the box
        Dim CornerPointList = Func_CalcBoxPoints(Vertex_1_vec, DirsSorted, DeltasSorted)

        '# Edit box orientations. Only highest value must be positive
        DirsSorted(0).Normalize()
        OrientVector(DirsSorted(0))
        RoundVector3(DirsSorted(0))
        DirsSorted(1).Normalize()
        OrientVector(DirsSorted(1))
        RoundVector3(DirsSorted(1))

        '# build 3rd axis with cross product
        Dim Dir3_new As VectorArithmetic.Vector3 = DirsSorted(0).Cross(DirsSorted(1))
        Dir3_new.Normalize()
        RoundVector3(Dir3_new)
        DirsSorted(2) = Dir3_new

        '# Search the one combination
        Dim Vert2Found As Boolean = False
        While Vert2Found = False
            For Each Point In CornerPointList

                '# calculated second point
                Dim Vert2_check = Func_VectorAddition(Point, DirsSorted, DeltasSorted)
                RoundVector3(Vert2_check)

                For Each Point2 In CornerPointList
                    Dim distancePoints As Double = (Vert2_check - Point2).LengthSqr()
                    '# check if point is identical to second point in this combination
                    If distancePoints <= 0.5 Then
                        Vert2Found = True
                        Vertex_1 = Func_Vector3_to_Double(Point)
                        Dirs = Func_Vector3List_toDouble2DArray(DirsSorted)
                        Deltas = DeltasSorted
                        Vertex_2 = Func_Vector3_to_Double(Point2)
                        Exit For
                    End If
                Next

                If Vert2Found = True Then
                    Exit For
                End If

            Next
        End While

        Output_CSV("Coordinate_P1_x") = Vertex_1(0)
        Output_CSV("Coordinate_P1_y") = Vertex_1(1)
        Output_CSV("Coordinate_P1_z") = Vertex_1(2)
        Output_CSV("Orientation_1_x") = Dirs(0, 0)
        Output_CSV("Orientation_1_y") = Dirs(0, 1)
        Output_CSV("Orientation_1_z") = Dirs(0, 2)
        Output_CSV("Orientation_2_x") = Dirs(1, 0)
        Output_CSV("Orientation_2_y") = Dirs(1, 1)
        Output_CSV("Orientation_2_z") = Dirs(1, 2)
        Output_CSV("Orientation_3_x") = Dirs(2, 0)
        Output_CSV("Orientation_3_y") = Dirs(2, 1)
        Output_CSV("Orientation_3_z") = Dirs(2, 2)
        If create = True Then
            Output_CSV("Coordinate_P2_x") = Vertex_2(0)
            Output_CSV("Coordinate_P2_y") = Vertex_2(1)
            Output_CSV("Coordinate_P2_z") = Vertex_2(2)
            Minimum_Boundingbox = Func_Create_propertybox(Func_Double_to_Point3d(Vertex_1),
                                                          Func_Vector3_to_Vector3d(DirsSorted(0)), Func_Vector3_to_Vector3d(DirsSorted(1)),
                                                          DeltasSorted)
            Output_CSV("Dim_1") = Deltas(0)
            Output_CSV("Dim_2") = Deltas(1)
            Output_CSV("Dim_3") = Deltas(2)
        End If
    End Sub
    Public Function Func_Create_propertybox(ByVal Vertex_1 As Point3d, ByVal xAxis As Vector3d, ByVal yAxis As Vector3d, ByVal lengths() As Double) As NXOpen.Body
        Try

            Dim Work_part As Part = theSession.Parts.Work
            Dim Null_Body As Body = Nothing

            Dim Block_analytic_BodyFeature As NXOpen.Features.BodyFeature = Nothing
            Dim Null_property_feature As NXOpen.Features.Feature = Nothing
            Dim BlockProperty As NXOpen.Features.BlockFeatureBuilder

            BlockProperty = Work_part.Features.CreateBlockFeatureBuilder(Null_property_feature)
            BlockProperty.SetOrientation(xAxis, yAxis)
            BlockProperty.SetOriginAndLengths(Vertex_1, Str(lengths(0)), Str(lengths(1)), Str(lengths(2)))
            BlockProperty.SetBooleanOperationAndTarget(NXOpen.Features.Feature.BooleanType.Create, Null_Body)
            Block_analytic_BodyFeature = BlockProperty.CommitFeature()
            Block_analytic_BodyFeature.SetName("Box_analysis_Zink")
            Dim Block_analytic_body As Body
            Block_analytic_body = Block_analytic_BodyFeature.GetBodies(0)
            theUFSession.Obj.SetColor(Block_analytic_body.Tag, 108)
            theUFSession.Obj.SetTranslucency(Block_analytic_body.Tag, 90)


            BlockProperty.Destroy()

            Func_Create_propertybox = Block_analytic_body

        Catch ex As Exception
            Console.WriteLine(ex.ToString)
            Dim Path_Exe_Act = Environment.CurrentDirectory()
            Dim UhrTime As String = String.Format("{0}{1}", Now.TimeOfDay.Hours, Now.TimeOfDay.Minutes)
            Dim Error_File_Name As String = Date_now + "_Fail_To_Build_Box_" + Part_Name_org + "_" + UhrTime + ".txt"
            Dim Error_File As IO.StreamWriter
            Error_File = My.Computer.FileSystem.OpenTextFileWriter(Path_Exe_Act + System.IO.Path.DirectorySeparatorChar.ToString + Error_File_Name, False)
            Error_File.WriteLine(ex.ToString)
            Error_File.Close()

            Dim Null_Body As Body = Nothing
            Func_Create_propertybox = Null_Body

        End Try

    End Function

    Private Sub Func_sortDimensionen(ByRef Dimensions() As Double)

        Dim Best_Value As Double
        Dim Best_j As Integer
        For i = 0 To 1
            Best_Value = Dimensions(i)
            Best_j = i
            For j = i + 1 To 2
                If Dimensions(j) > Best_Value Then
                    Best_Value = Dimensions(j)
                    Best_j = j
                End If
            Next j
            Dimensions(Best_j) = Dimensions(i)
            Dimensions(i) = Best_Value
        Next i

    End Sub

    Private Sub RoundArrays_oneDim(ByRef DoubleArray() As Double)
        For index0 = 0 To DoubleArray.GetUpperBound(0)
            Dim value As Double = DoubleArray(index0)
            DoubleArray(index0) = Math.Round(value, DecimalsData)
        Next
    End Sub

    Private Sub RoundArrays_twoDim(ByRef DoubleArray(,) As Double)
        For index0 = 0 To DoubleArray.GetUpperBound(0)
            For index1 = 0 To DoubleArray.GetUpperBound(1)
                Dim value As Double = DoubleArray(index0, index1)
                DoubleArray(index0, index1) = Math.Round(value, DecimalsData)
            Next
        Next
    End Sub

    Private Sub RoundVector3(ByRef Vector As VectorArithmetic.Vector3)
        Vector.x = Math.Round(Vector.x, DecimalsData)
        Vector.y = Math.Round(Vector.y, DecimalsData)
        Vector.z = Math.Round(Vector.z, DecimalsData)
    End Sub

    Private Sub OrientVector(ByRef Vector As VectorArithmetic.Vector3)

        Dim vectorValues() As Double = Func_Vector3_to_Double(Vector)
        For pos As Integer = 0 To vectorValues.Count() - 1
            vectorValues(pos) = Math.Abs(vectorValues(pos))
        Next
        Dim maxValue = vectorValues.Max()

        If Math.Abs(Vector.x) = maxValue Then
            If Vector.x < 0 Then
                Vector *= -1.0
            End If
        ElseIf Math.Abs(Vector.y) = maxValue Then
            If Vector.y < 0 Then
                Vector *= -1.0
            End If
        Else
            If Vector.z < 0 Then
                Vector *= -1.0
            End If
        End If
    End Sub

    Private Function Func_CalcBoxPoints(ByVal StartPoint As VectorArithmetic.Vector3, ByVal Directions As List(Of VectorArithmetic.Vector3), ByVal Deltas() As Double) As List(Of VectorArithmetic.Vector3)

        Dim PointX0 = Func_VectorAddition(StartPoint, Directions, {Deltas(0), 0, 0})
        Dim PointY0 = Func_VectorAddition(StartPoint, Directions, {0, Deltas(1), 0})
        Dim PointXY0 = Func_VectorAddition(StartPoint, Directions, {Deltas(0), Deltas(1), 0})
        Dim PointZ1 = Func_VectorAddition(StartPoint, Directions, {0, 0, Deltas(2)})
        Dim PointX1 = Func_VectorAddition(StartPoint, Directions, {Deltas(0), 0, Deltas(2)})
        Dim PointY1 = Func_VectorAddition(StartPoint, Directions, {0, Deltas(1), Deltas(2)})
        Dim PointXY1 = Func_VectorAddition(StartPoint, Directions, {Deltas(0), Deltas(1), Deltas(2)})

        Return New List(Of VectorArithmetic.Vector3)({StartPoint, PointX0, PointY0, PointXY0, PointZ1, PointX1, PointY1, PointXY1})

    End Function
    Private Function Func_VectorAddition(ByVal StartPoint As VectorArithmetic.Vector3, ByVal Directions As List(Of VectorArithmetic.Vector3), ByVal Deltas() As Double) As VectorArithmetic.Vector3
        Dim EndPoint As VectorArithmetic.Vector3
        EndPoint = StartPoint + Directions(0) * Deltas(0) + Directions(1) * Deltas(1) + Directions(2) * Deltas(2)
        Func_VectorAddition = EndPoint
    End Function



End Module