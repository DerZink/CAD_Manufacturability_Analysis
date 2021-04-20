Imports NXOpen
Imports System
Imports NXOpen.UF
Imports NXOpen.UI
Imports NXOpen.Utilities
Imports NXOpen.VectorArithmetic
Imports Math_Net = MathNet.Numerics

Public Module _01_PointsCloud
    Public Sub _start()

        PointsCloud = Points_in_cubes()
        'Draw_Points(PointsCloud)

    End Sub


    Private Function Points_in_cubes() As Dictionary(Of Tuple(Of Integer, Integer, Integer), Double())
        Dim Vertex_1 As Vector3 = Func_Double_to_Vector3({Output_CSV("Coordinate_P1_x"), Output_CSV("Coordinate_P1_y"), Output_CSV("Coordinate_P1_z")})
        'Dim Vertex_2() As Double = {Output_CSV("Coordinate_P2_x"), Output_CSV("Coordinate_P2_y"), Output_CSV("Coordinate_P2_z")}
        Dim Dir_0 As Vector3 = DirsSorted(0) 'Func_Double_to_Vector3({Output_CSV("Orientation_1_x"), Output_CSV("Orientation_1_y"), Output_CSV("Orientation_1_z")})
        Dim Dir_1 As Vector3 = DirsSorted(1) 'Func_Double_to_Vector3({Output_CSV("Orientation_2_x"), Output_CSV("Orientation_2_y"), Output_CSV("Orientation_2_z")})
        Dim Dir_2 As Vector3 = DirsSorted(2) 'Func_Double_to_Vector3({Output_CSV("Orientation_3_x"), Output_CSV("Orientation_3_y"), Output_CSV("Orientation_3_z")})

        Dim deltaBoxProduct_0 = Deltas(0) * Deltas(1) * Deltas(2)
        Dim DeltasCopy As Double() = Deltas.Clone()
        ' adjust delta for small deltas in one or two directions
        Dim deltaPerc_min = 4 * (NumberOfPoints) ^ (-1 / 3) ' solving min step == 2 to minimum delta
        Dim delta_min_0 = deltaPerc_min * deltaBoxProduct_0 ^ (1 / 3)

        Dim deltaBoxProduct = deltaBoxProduct_0
        Dim minDeltaPos As New List(Of Integer)
        For pos As Integer = 0 To DeltasCopy.Count() - 1
            If DeltasCopy(pos) < delta_min_0 Then
                minDeltaPos.Add(pos)
            End If
        Next

        If minDeltaPos.Count() = 1 Then
            Dim posRest As New List(Of Double)({0, 1, 2})
            posRest.RemoveAt(minDeltaPos(0))
            Dim product = DeltasCopy(posRest(0)) * DeltasCopy(posRest(1))
            Dim minObjective = (deltaPerc_min * product ^ (1 / 3)) ^ (3 / 2)
            DeltasCopy(minDeltaPos(0)) = minObjective
            deltaBoxProduct = DeltasCopy(0) * DeltasCopy(1) * DeltasCopy(2)
        End If

        If minDeltaPos.Count() = 2 Then
            Dim posRest As New List(Of Double)({0, 1, 2})
            posRest.RemoveAt(minDeltaPos(0))
            posRest.RemoveAt(minDeltaPos(1 - 1))
            Dim product = DeltasCopy(posRest(0))
            Dim minObjective = (deltaPerc_min * product ^ (1 / 3)) ^ (3)
            DeltasCopy(minDeltaPos(0)) = minObjective
            DeltasCopy(minDeltaPos(1)) = minObjective
            deltaBoxProduct = DeltasCopy(0) * DeltasCopy(1) * DeltasCopy(2)
        End If


        ' calc point distribution
        Dim deltaPerc_0 = DeltasCopy(0) / deltaBoxProduct ^ (1 / 3)
        Dim deltaPerc_1 = DeltasCopy(1) / deltaBoxProduct ^ (1 / 3)
        Dim deltaPerc_2 = DeltasCopy(2) / deltaBoxProduct ^ (1 / 3)

        ' optimization number of points
        Dim pointDev = NumberOfPoints
        Dim pointDevMin = NumberOfPoints
        Dim NumberOfPointsOpt = NumberOfPoints
        Dim NumberOfPointsMin = NumberOfPoints

        Dim optCount = 0

        While pointDev > NumberOfPoints / 10 And optCount <= 20

            Dim stepR0 = NumberOfPointsOpt ^ (1 / 3) * deltaPerc_0 - 2
            If stepR0 <= 1 Then
                stepR0 = 2
            End If
            Dim stepR1 = NumberOfPointsOpt ^ (1 / 3) * deltaPerc_1 - 2
            If stepR1 <= 1 Then
                stepR1 = 2
            End If
            Dim stepR2 = NumberOfPointsOpt ^ (1 / 3) * deltaPerc_2 - 2
            If stepR2 <= 1 Then
                stepR2 = 2
            End If

            Dim delta_R0_i = Deltas(0) / stepR0
            Dim delta_R1_i = Deltas(1) / stepR1
            Dim delta_R2_i = Deltas(2) / stepR2

            delta_R0 = discreteDistances(delta_R0_i)
            delta_R1 = discreteDistances(delta_R1_i)
            delta_R2 = discreteDistances(delta_R2_i)

            Dim pointCheck = Deltas(0) / delta_R0 * Deltas(1) / delta_R1 * Deltas(2) / delta_R2
            pointDev = Math.Abs(NumberOfPoints - pointCheck)
            If pointDev < pointDevMin Then
                pointDevMin = pointDev
                NumberOfPointsMin = NumberOfPointsOpt
            End If
            NumberOfPointsOpt = Int(Math.Round(Math.Max(NumberOfPointsOpt * (1 + (NumberOfPoints - pointCheck) / NumberOfPoints), NumberOfPoints * 2 / 3), 0))
            optCount += 1

        End While

        If optCount = 20 + 1 Then
            Dim stepR0 = NumberOfPointsMin ^ (1 / 3) * deltaPerc_0 - 2
            If stepR0 <= 1 Then
                stepR0 = 2
            End If
            Dim stepR1 = NumberOfPointsMin ^ (1 / 3) * deltaPerc_1 - 2
            If stepR1 <= 1 Then
                stepR1 = 2
            End If
            Dim stepR2 = NumberOfPointsMin ^ (1 / 3) * deltaPerc_2 - 2
            If stepR2 <= 1 Then
                stepR2 = 2
            End If

            Dim delta_R0_i = Deltas(0) / stepR0
            Dim delta_R1_i = Deltas(1) / stepR1
            Dim delta_R2_i = Deltas(2) / stepR2

            delta_R0 = discreteDistances(delta_R0_i)
            delta_R1 = discreteDistances(delta_R1_i)
            delta_R2 = discreteDistances(delta_R2_i)
        End If

        Dim Points_L0 As New Dictionary(Of Tuple(Of Integer, Integer, Integer), Double())
        Dim Points_Box As New Dictionary(Of Tuple(Of Integer, Integer, Integer), Double())

        '# distribute points equaly over box by translation of startpoint. stepwidth remains constant
        Dim trans_1 As Double = Math.Abs(Deltas(0) - Math.Ceiling(Deltas(0) / delta_R0) * delta_R0) / 2.0
        Dim trans_2 As Double = Math.Abs(Deltas(1) - Math.Ceiling(Deltas(1) / delta_R1) * delta_R1) / 2.0
        Dim trans_3 As Double = Math.Abs(Deltas(2) - Math.Ceiling(Deltas(2) / delta_R2) * delta_R2) / 2.0

        Dim Vertex_start = Vertex_1 - trans_1 * Dir_0 - trans_2 * Dir_1 - trans_3 * Dir_2

        Dim dist0 As Double = 0.0
        Dim i_0 As Integer = 0
        While dist0 <= Deltas(0) + 1 * delta_R0
            Dim Point_act As Vector3 = Vertex_start + Dir_0 * dist0
            Dim Point_array = Func_Vector3_to_Double(Point_act)
            Dim Coordinate_act = Tuple.Create(Of Integer, Integer, Integer)(i_0, 0, 0)
            Points_Box(Coordinate_act) = Point_array
            Points_L0(Coordinate_act) = Point_array
            dist0 += delta_R0
            i_0 += 1
        End While
        Number_of_R0 = i_0

        Dim Points_E0 As New Dictionary(Of Tuple(Of Integer, Integer, Integer), Double())(Points_L0)
        Dim dist1 As Double = delta_R1
        Dim i_1 As Integer = 1
        While dist1 <= Deltas(1) + 1 * delta_R1
            For Each Data_L0 In Points_L0
                Dim Coordinate_L0 = Data_L0.Key
                Dim Point_act_L0 = Func_Double_to_Vector3(Data_L0.Value)
                Dim Point_act = Point_act_L0 + Dir_1 * dist1
                Dim Point_array = Func_Vector3_to_Double(Point_act)
                Dim Coordinate_akt = Tuple.Create(Of Integer, Integer, Integer)(Coordinate_L0.Item1, i_1, 0)
                Points_Box(Coordinate_akt) = Point_array
                Points_E0(Coordinate_akt) = Point_array
            Next
            dist1 += delta_R1
            i_1 += 1
        End While
        Number_of_R1 = i_1

        Dim dist2 As Double = delta_R2
        Dim i_2 As Integer = 1
        While dist2 <= Deltas(2) + 1 * delta_R2
            For Each Data_E0 In Points_E0
                Dim Coordinate_E0 = Data_E0.Key
                Dim Point_act_E0 = Func_Double_to_Vector3(Data_E0.Value)
                Dim Point_act = Point_act_E0 + Dir_2 * dist2
                Dim Point_array = Func_Vector3_to_Double(Point_act)
                Dim Coordinate_akt = Tuple.Create(Of Integer, Integer, Integer)(Coordinate_E0.Item1, Coordinate_E0.Item2, i_2)
                Points_Box(Coordinate_akt) = Point_array
            Next
            dist2 += delta_R2
            i_2 += 1
        End While
        Number_of_R2 = i_2

        'If Draft_Mode = True Then
        '    Draw_Points(Points_Box)
        'End If

        Points_in_cubes = Points_Box

    End Function

    Private Function discreteDistances(ByVal _Delta As Double)

        Dim discreteResult = _Delta

        If DiscretizationStep <= 1 Then
            discreteResult = Math.Round(_Delta, 0)

        Else
            Dim deltaLog As Double = Math.Log(_Delta, DiscretizationStep)
            Dim deltaLogRound As Double = Math.Round(deltaLog, 0)

            discreteResult = DiscretizationStep ^ deltaLogRound

        End If

        discreteDistances = discreteResult

    End Function
    Private Sub Draw_Points(ByVal _Points As Dictionary(Of Tuple(Of Integer, Integer, Integer), Double()))
        Dim Cloud As New List(Of Tag)
        For Each Point_tuple In _Points
            Dim Point As Double() = {Point_tuple.Value(0), Point_tuple.Value(1), Point_tuple.Value(2)}
            Cloud.Add(Func_Point_To_Draw(Point))
        Next
        Sub_Create_FeatureGroup(Cloud.ToArray(), "GridPoints")
    End Sub

End Module
