Imports NXOpen
Imports System
Imports NXOpen.UF
Imports NXOpen.UI
Imports NXOpen.Utilities
Imports Math_Net = MathNet.Numerics
Imports SharedModule.Public_Variable
Imports SharedModule.Typ_Transformations
Imports SharedModule.Mod_Boundingbox_General_Func
Module Mod_Randbox_genetic

    Public Function Func_Zink_Boundingbox_genetic(ByRef Min_Box() As Vector3d) As Double
        '# Genetic Optimization of the Minimal Box According to Chang et al 'Fast Oriented Bounding Box Optimization on the Rotation Group SO (3, R)'

        '# Boundary values of the optimization
        Dim Number_of_Population As Integer = 20
        Dim Number_of_Mutations As Integer = 40
        Dim Number_of_Iterations As Integer = 30

        '# optimization
        Dim Matrix_Box() As Vector3d = Min_Box
        Dim Volume_Box_Min_Cloud As Double = Nothing
        Sub_Genetic_Algorithm_Header(Number_of_Population, Number_of_Mutations, Number_of_Iterations, Matrix_Box, Volume_Box_Min_Cloud)

        '# Creation of the smallest possible box based on the genetic min box
        Dim Edge_1(2) As Double
        Dim Dirs(2, 2) As Double
        Dim Delta(2) As Double
        Dim Focuspoint_ACS As New Point3d(0.0, 0.0, 0.0)
        Dim Gen_axis_ACS As Vector3d = Matrix_Box(0)
        Dim Gen_yaxis_ACS As Vector3d = Matrix_Box(1)
        Dim Gen_coordsys_ACS As NXOpen.CartesianCoordinateSystem
        Dim Body_Tag(0) As NXOpen.Tag
        Body_Tag(0) = Body_act.Tag
        Gen_coordsys_ACS = Part_act.CoordinateSystems.CreateCoordinateSystem(Focuspoint_ACS, Gen_axis_ACS, Gen_yaxis_ACS)
        theUFSession.Modl.AskBoundingBoxExact(Body_Tag(0), Gen_coordsys_ACS.Tag, Edge_1, Dirs, Delta)

        '# Calculation and transfer of the box volume
        Dim Volume_Box_Min As Double = Func_Calculate_Box_Volume(Delta)

        Min_Box = Matrix_Box
        Func_Zink_Boundingbox_genetic = Volume_Box_Min
    End Function
    Private Sub Sub_Genetic_Algorithm_Header(ByVal Number_of_Population As Integer, ByVal Number_of_Mutations As Integer,
                                                   ByVal Number_of_Iterations As Integer, ByRef Matrix_Box() As Vector3d, ByRef Volume_Box_Min As Double)

        Dim Dimensions As Integer = 3

        '# Generation of Number_of_Population random simplexes with (points_) dimensions + 1 rotation matrices
        Dim Population_Matrix As New Dictionary(Of Integer, Dictionary(Of Integer, Vector3d()))
        Dim Matrix_coincidence As Math_Net.LinearAlgebra.Matrix(Of Double)
        Dim Q_Matrix As Math_Net.LinearAlgebra.Double.Matrix
        Dim Q_Vector_List As New Dictionary(Of Integer, Vector3d)
        Dim Number_of_Columns_Q As Integer
        Dim Population_Fitness As New Dictionary(Of Integer, List(Of Double))
        Dim Act_Min_fitness As Double = 1 / 0
        Dim Entry_Min_Fitness As Integer = Dimensions + 1
        Dim Min_Simplex As Integer
        Dim Min_Simplex_Matrix As Integer
        Dim Fitness_List As New List(Of KeyValuePair(Of Integer, Double))

        For i = 0 To Number_of_Population Step 1
            Dim Rot_matrices As New Dictionary(Of Integer, Vector3d())
            For j = 0 To Dimensions Step 1
                '# Add Min_Box from HTAS as a Rot_Matrix, Code Acceleration
                If i = 0 And j = 0 Then
                    Rot_matrices(j) = {Matrix_Box(0), Matrix_Box(1), Matrix_Box(2)}
                Else
                    '# Generation of the matrices
                    Matrix_coincidence = Math_Net.LinearAlgebra.Double.DenseMatrix.Build.Random(3, 3) '# Zufalls 3-auf-3 Matrix
                    Q_Matrix = Matrix_coincidence.QR(Math_Net.LinearAlgebra.Factorization.QRMethod.Full).Q '# QR-Zerlegung (schnell) fuer lin. unabhaengige/orthogonale Matrix
                    Number_of_Columns_Q = Q_Matrix.ColumnCount
                    Q_Vector_List.Clear()
                    '# Transfer to Dict Q_Vector_List (Int, Vector3D)
                    For z = 0 To Number_of_Columns_Q - 1 Step 1
                        Dim Q_temp As New Vector3d(Q_Matrix.ToColumnArrays()(z)(0), Q_Matrix.ToColumnArrays()(z)(1), Q_Matrix.ToColumnArrays()(z)(2))
                        Q_Vector_List(z) = Q_temp
                    Next
                    Rot_matrices(j) = {Q_Vector_List(0), Q_Vector_List(1), Q_Vector_List(2)}
                    Matrix_coincidence.Clear()
                End If
            Next
            Population_Matrix.Add(i, Rot_matrices)
            '# Fitness of all population or all rotation matrices in a simplex
            Population_Fitness(i) = Func_Fitness(Population_Matrix(i))
            Fitness_List.Add(New KeyValuePair(Of Integer, Double)(i, Population_Fitness(i)(Dimensions + 1)))
            '# Find the smallest box volume of the population
            If Population_Fitness(i)(Dimensions + 1) < Act_Min_fitness Then
                Min_Simplex = i
                Min_Simplex_Matrix = Population_Fitness(i)(Dimensions + 2)
                Act_Min_fitness = Population_Fitness(i)(Entry_Min_Fitness)
            End If
        Next

        '# Pass the best 50% of the populations
        Dim Fitness_List_sorted = Fitness_List.OrderBy(Function(x) x.Value).ToList
        Dim Population_Matrix_bestHalf As New Dictionary(Of Integer, Dictionary(Of Integer, Vector3d()))
        Dim Population_Fitness_bestHalf As New Dictionary(Of Integer, List(Of Double))
        Dim Simplex_Index As Integer = 0
        Dim M_Half As Integer = Math.Ceiling((Number_of_Population) / 2) '# rounded up
        Dim Fitness_Mut_Start As Double = 1 / 0
        Dim Simplex_min As Integer = -1
        Dim Matrix_min As Integer = -1
        While Simplex_Index < M_Half
            Dim Index_List_Sorted = Fitness_List_sorted(Simplex_Index).Key
            Population_Matrix_bestHalf(Simplex_Index) = Population_Matrix(Index_List_Sorted)
            Population_Fitness_bestHalf(Simplex_Index) = Population_Fitness(Index_List_Sorted)
            Dim Fitness_act = Population_Fitness_bestHalf(Simplex_Index)
            If Fitness_act(Dimensions + 1) < Fitness_Mut_Start Then
                Fitness_Mut_Start = Fitness_act(Dimensions + 1)
                Simplex_min = Simplex_Index
                Matrix_min = Fitness_act(Dimensions + 2)
            End If
            Simplex_Index += 1
        End While

        '# Mutation of the better half of the populations
        Sub_Mutation(Population_Matrix_bestHalf, Population_Fitness_bestHalf, Fitness_Mut_Start, Number_of_Mutations, Number_of_Iterations, Matrix_Box, Volume_Box_Min)

    End Sub
    Private Sub Sub_Mutation(ByVal Population As Dictionary(Of Integer, Dictionary(Of Integer, Vector3d())),
                                   ByVal Population_Fitness As Dictionary(Of Integer, List(Of Double)),
                                   ByVal Fitness_Mut_Start As Double, ByVal Number_of_Mutations As Integer,
                                   ByVal Number_of_Iterations As Integer,
                                   ByRef Matrix_Box() As Vector3d, ByRef Volume_Box_Min As Double)

        Dim Population_Calculation = Population
        Dim Number_of_Matrixes = Population_Calculation(0).Count
        Dim Simplex_min As Integer = -1
        Dim Matrix_min As Integer = -1
        Dim Number_of_Convergence_Crit As Integer = 0

        Dim Fitness_Nelder_Mead_min As Double = 1 / 0
        Dim Simplex_Nelder_Mead_min As Integer = -1
        Dim Matrix_Nelder_Mead_min As Integer = -1
        Dim Fitness_i_minus_1 As Double = 1 / 0

        '# Tag limit is reached on some components -> abort and take over last value
        Dim tag_stand_0 As Integer = Nothing
        theUFSession.Ps.AskTagsRemaining(tag_stand_0)
        Dim Tag_consumption As Integer = Nothing

        For Mutations = 0 To Number_of_Mutations Step 1

            If Fitness_Mut_Start > Fitness_Nelder_Mead_min Then
                Fitness_Mut_Start = Fitness_Nelder_Mead_min
            End If
            '# Create new population from (initially) 50% of the best starting populations
            Dim New_Population_Matrix = Func_Evolution(Population_Calculation, Population_Fitness)

            '# Nelder-Mead Mutation
            For Each Simplex_key In New_Population_Matrix.Keys
                Population_Calculation(Simplex_key) = Func_Nelder_Mead_Mutation(New_Population_Matrix(Simplex_key), Number_of_Iterations)
                Dim Fitness_Nelder_Mead_akt = Func_Fitness(Population_Calculation(Simplex_key))
                If Fitness_Nelder_Mead_akt(Number_of_Matrixes) < Fitness_Nelder_Mead_min Then
                    Fitness_Nelder_Mead_min = Fitness_Nelder_Mead_akt(Number_of_Matrixes)
                    Simplex_Nelder_Mead_min = Simplex_key
                    Matrix_Nelder_Mead_min = Fitness_Nelder_Mead_akt(Number_of_Matrixes + 1)
                End If
            Next
            '# Tag-Stand Control
            Dim tag_stand_1 As Integer = Nothing
            theUFSession.Ps.AskTagsRemaining(tag_stand_1)
            Tag_consumption = tag_stand_0 - tag_stand_1
            If tag_stand_1 <= Tag_consumption * 1.1 Then Exit For
            tag_stand_0 = tag_stand_1

            '# Zufalls-Mutations...later if necessary
            Dim Mutation_Switch = 0
            If Mutation_Switch = 1 Then
            End If

            '# convergence criterion
            If Fitness_Nelder_Mead_min < Fitness_Mut_Start Then
                Dim status_fitness = Math.Abs(Fitness_Nelder_Mead_min - Fitness_Mut_Start)
                If (status_fitness < (Percent_volume_abort_criterion * Fitness_Mut_Start)) Then
                    If status_fitness <= Fitness_i_minus_1 Then
                        Number_of_Convergence_Crit += 1
                    Else
                        Number_of_Convergence_Crit = 0
                    End If
                    Fitness_i_minus_1 = status_fitness

                    If Number_of_Convergence_Crit = Necessary_vol_Min Then Exit For
                End If
            End If
        Next
        Matrix_Box = Population_Calculation(Simplex_Nelder_Mead_min)(Matrix_Nelder_Mead_min)
        Volume_Box_Min = Fitness_Nelder_Mead_min

    End Sub

    Private Function Func_Fitness(ByVal Simplex As Dictionary(Of Integer, Vector3d())) As List(Of Double)
        '# Traversing the matrices in a simplex
        '# List of volumes to dimensions + 1 = min of volume + 1 = matrix with min volume 
        Func_Fitness = Nothing
        Dim Volume_List As New List(Of Double)
        Dim Volume_List_Index As New List(Of KeyValuePair(Of Integer, Double))
        Dim Number_of_Matrixes As Integer = Simplex.Count - 1
        For M = 0 To Number_of_Matrixes Step 1
            Dim Volume_Temp = Func_Vol_Box(Simplex(M))
            Volume_List.Add(Volume_Temp)
            Volume_List_Index.Add(New KeyValuePair(Of Integer, Double)(M, Volume_Temp))
        Next
        Dim Volume_List_sorted As List(Of Double) = Volume_List_Index.OrderBy(Function(x) x.Value).Select(Function(x) x.Key).ToList.ConvertAll(Function(int) Double.Parse(int))
        Volume_List.Add(Volume_List.Min)
        Volume_List.AddRange(Volume_List_sorted)
        Func_Fitness = Volume_List

    End Function
    Private Function Func_Vol_Box(ByVal Rot_Matrix As Vector3d()) As Double
        '# Calculation of the min box of a Rot_Matrix from a simplex
        Dim Delta(2) As Double

        Sub_Bounding_Box_Cloud(Rot_Matrix, Delta)
        '# Berechnung des Volumens
        Func_Vol_Box = Func_Calculate_Box_Volume(Delta)

    End Function
    Private Function Func_Evolution(ByVal Population_Matrixes As Dictionary(Of Integer, Dictionary(Of Integer, Vector3d())),
                                          ByVal Population_Fitness As Dictionary(Of Integer, List(Of Double))) As Dictionary(Of Integer, Dictionary(Of Integer, Vector3d()))

        Dim Number_of_Populations = Population_Matrixes.Count
        Dim Number_of_Populations_Half_on As Integer = Math.Ceiling(Number_of_Populations / 2)
        Dim Number_of_Populations_Half_off As Integer = Math.Floor(Number_of_Populations / 2)
        Dim Dimensions_Simplex = Population_Matrixes.Item(0).Count
        Dim Entry_Min_Fitness As Integer = Dimensions_Simplex
        Dim Pop_Index As Integer = 0
        Dim Pop_1 As New Dictionary(Of Integer, Dictionary(Of Integer, Vector3d()))
        Dim Pop_2 As New Dictionary(Of Integer, Dictionary(Of Integer, Vector3d()))
        Dim Pop_3 As New Dictionary(Of Integer, Dictionary(Of Integer, Vector3d()))
        Dim Pop_4 As New Dictionary(Of Integer, Dictionary(Of Integer, Vector3d()))
        Dim Fit_1 As New Dictionary(Of Integer, List(Of Double))
        Dim Fit_2 As New Dictionary(Of Integer, List(Of Double))
        Dim Fit_3 As New Dictionary(Of Integer, List(Of Double))
        Dim Fit_4 As New Dictionary(Of Integer, List(Of Double))

        '# Generation of the 4 population groups
        While Pop_Index < Number_of_Populations_Half_on
            Randomize()
            Dim Rand As Double = Rnd()
            Dim Random_1 = CInt(Int((Number_of_Populations * Rand) + 0))
            Pop_1(Pop_Index) = Population_Matrixes(Random_1)
            Fit_1(Pop_Index) = Population_Fitness(Random_1)
            Randomize()
            Rand = Rnd()
            Dim Random_2 = CInt(Int((Number_of_Populations * Rand) + 0))
            Pop_2(Pop_Index) = Population_Matrixes(Random_2)
            Fit_2(Pop_Index) = Population_Fitness(Random_2)
            Randomize()
            Rand = Rnd()
            Dim Random_3 = CInt(Int((Number_of_Populations * Rand) + 0))
            Pop_3(Pop_Index) = Population_Matrixes(Random_3)
            Fit_3(Pop_Index) = Population_Fitness(Random_3)
            Randomize()
            Rand = Rnd()
            Dim Random_4 = CInt(Int((Number_of_Populations * Rand) + 0))
            Pop_4(Pop_Index) = Population_Matrixes(Random_4)
            Fit_4(Pop_Index) = Population_Fitness(Random_4)
            Pop_Index += 1
        End While

        Dim New_Pop As New Dictionary(Of Integer, Dictionary(Of Integer, Vector3d()))
        '# Generation of new population groups I new_Pop_1
        Dim new_Pop_1 As New Dictionary(Of Integer, Dictionary(Of Integer, Vector3d()))
        For Each Entry_1 In Pop_1.Keys
            '# Compare if Min_Vol greater-smaller -> 1 or 0
            Dim Temp_1 As Integer = (Fit_1(Entry_1)(Entry_Min_Fitness) <= Fit_2(Entry_1)(Entry_Min_Fitness))
            Dim Compare_1 As Integer = Math.Abs(Temp_1)
            Dim Temp_2 As Integer = (Fit_1(Entry_1)(Entry_Min_Fitness) >= Fit_2(Entry_1)(Entry_Min_Fitness))
            Dim Compare_2 As Integer = Math.Abs(Temp_2)
            Dim MixingRule_Pop1 As Double
            MixingRule_Pop1 = 0.5 + 0.1 * (Compare_1) - 0.1 * (Compare_2)
            '# Randomization in new_Pop_1 of Pop_1 and Pop_2
            Dim Matrix_temp_1 As New Dictionary(Of Integer, Vector3d())
            For Each Matrix In Pop_1(Entry_1).Keys
                Randomize()
                If (Rnd() < MixingRule_Pop1) Then
                    Matrix_temp_1.Add(Matrix, Pop_1(Entry_1)(Matrix))
                Else
                    Matrix_temp_1.Add(Matrix, Pop_2(Entry_1)(Matrix))
                End If
            Next
            New_Pop.Add(Entry_1, Matrix_temp_1)
            new_Pop_1.Add(Entry_1, Matrix_temp_1)
        Next

        '# Generation of new population groups II new_Pop_2
        Dim New_pop_keys = New_Pop.Keys.Count
        Dim new_Pop_2 As New Dictionary(Of Integer, Dictionary(Of Integer, Vector3d()))
        Dim Entry_2 As Integer = 0
        While Entry_2 < Number_of_Populations_Half_off
            '# Compare if Min_Vol greater-smaller -> 1 or 0
            Dim Temp_1 As Integer = (Fit_3(Entry_2)(Entry_Min_Fitness) <= Fit_4(Entry_2)(Entry_Min_Fitness))
            Dim Compare_1 As Integer = Math.Abs(Temp_1)
            Dim Temp_2 As Integer = (Fit_3(Entry_2)(Entry_Min_Fitness) >= Fit_4(Entry_2)(Entry_Min_Fitness))
            Dim Compare_2 As Integer = Math.Abs(Temp_2)
            Dim MixingRule_Pop2 As Double
            MixingRule_Pop2 = 0.5 + 0.1 * (Compare_1) - 0.1 * (Compare_2)
            '# Randomization in new_Pop_1 of Pop_1 and Pop_2
            Dim Matrix_Temp_2 As New Dictionary(Of Integer, Vector3d())
            For Each Matrix In Pop_3(Entry_2).Keys
                Dim Matrix_affin = Func_Affine_Transformation(Pop_3(Entry_2)(Matrix), Pop_4(Entry_2)(Matrix), MixingRule_Pop2, 1.0 - MixingRule_Pop2, )
                Matrix_Temp_2.Add(Matrix, Matrix_affin)
            Next
            New_Pop.Add(New_pop_keys + Entry_2, Matrix_Temp_2)
            new_Pop_2.Add(Entry_2, Matrix_Temp_2)
            Entry_2 += 1
        End While

        Func_Evolution = New_Pop

    End Function
    Private Function Func_Nelder_Mead_Mutation(ByVal Simplex As Dictionary(Of Integer, Vector3d()), ByVal Number_of_Iterations As Integer) As Dictionary(Of Integer, Vector3d())

        Dim Number_of_Matrixes As Integer = Simplex.Count
        Dim Number_of_Matrixes_Calculation As Integer = Number_of_Matrixes - 1
        '#Standard Werte fuer Nelder-Mead Simplex Algorithmus
        Dim rho As Double = 1 / 2
        Dim sigma As Double = 1 / 2

        Dim Simplex_Calculation = Simplex

        For iteration = 0 To Number_of_Iterations Step 1
            '# Step 1 : Reordering to Min_Volume
            Dim Fit_Temp = Func_Fitness(Simplex_Calculation)
            '# Step 2 : Center of gravity of all simplexes after Karcher
            Dim Mean_Matrix = Func_Karcher(Simplex_Calculation, Fit_Temp)
            Dim Location_Matrix_Max As Integer = Fit_Temp(Number_of_Matrixes * 2)
            Dim Matrix_vol_Max = Func_Vector3D_to_MathNetMatrix(Simplex_Calculation(Location_Matrix_Max))
            Dim Reflections_Matrix = Mean_Matrix * Matrix_vol_Max.Transpose * Mean_Matrix
            Dim Reflections_Matrix_Fitness = Func_Vol_Box(Func_MathNetMatrix_to_Vector3D(Reflections_Matrix))
            Dim Index_before_worst_matrix As Integer = Fit_Temp(Number_of_Matrixes + Number_of_Matrixes_Calculation)
            If Reflections_Matrix_Fitness < Fit_Temp(Index_before_worst_matrix) Then
                If Reflections_Matrix_Fitness >= Fit_Temp(Number_of_Matrixes) Then
                    '# Step 3 : Reflection
                    Simplex_Calculation(Location_Matrix_Max) = Func_MathNetMatrix_to_Vector3D(Reflections_Matrix)
                Else
                    '# Step 4 : Expansion
                    Dim Expansions_Matrix = Mean_Matrix * Matrix_vol_Max.Transpose * Reflections_Matrix
                    Dim Expansions_Matrix_Fitness = Func_Vol_Box(Func_MathNetMatrix_to_Vector3D(Expansions_Matrix))
                    If Expansions_Matrix_Fitness < Reflections_Matrix_Fitness Then
                        Simplex_Calculation(Location_Matrix_Max) = Func_MathNetMatrix_to_Vector3D(Expansions_Matrix)
                    Else
                        Simplex_Calculation(Location_Matrix_Max) = Func_MathNetMatrix_to_Vector3D(Reflections_Matrix)
                    End If
                End If
            Else
                '# Step 5 : Contraction
                Dim Contractions_Matrix = Func_Affine_Transformation(Func_MathNetMatrix_to_Vector3D(Mean_Matrix), Simplex_Calculation(Location_Matrix_Max), rho, -rho, Simplex_Calculation(Location_Matrix_Max))
                Dim Contractions_Matrix_Fitness = Func_Vol_Box(Contractions_Matrix)
                If Contractions_Matrix_Fitness <= Fit_Temp(Location_Matrix_Max) Then
                    Simplex_Calculation(Location_Matrix_Max) = Contractions_Matrix
                Else
                    '# Step 6 : Reduction
                    For Matrix = 2 To Number_of_Matrixes
                        Dim Location_Matrix_act As Integer = Fit_Temp(Number_of_Matrixes + Matrix)
                        Dim Location_Matrix_min As Integer = Fit_Temp(Number_of_Matrixes + 1)
                        Dim Affine_Matrix = Func_Affine_Transformation(Simplex_Calculation(Location_Matrix_act), Simplex_Calculation(Location_Matrix_min), sigma, -sigma, Simplex_Calculation(Location_Matrix_min))
                        Simplex_Calculation(Location_Matrix_act) = Affine_Matrix
                    Next
                End If
            End If
        Next

        Func_Nelder_Mead_Mutation = Simplex_Calculation

    End Function
    Private Function Func_Affine_Transformation(ByVal Matrix_1 As Vector3d(),
                                           ByVal Matrix_2 As Vector3d(),
                                           ByVal MixingRule_1 As Double,
                                           ByVal MixingRule_2 As Double,
                                           Optional ByVal Matrix_0 As Object = Nothing) As Vector3d()
        '# Affine transformation of the two matrix

        Dim Matrix_Affin As Math_Net.LinearAlgebra.Matrix(Of Double)
        Matrix_Affin = Math_Net.LinearAlgebra.Double.Matrix.Build.Dense(3, 3)
        Dim Matrix1_MathNet As Math_Net.LinearAlgebra.Matrix(Of Double)
        Dim Matrix2_MathNet As Math_Net.LinearAlgebra.Matrix(Of Double)

        If Not IsNothing(Matrix_0) Then
            Dim Matrix0_MathNet As Math_Net.LinearAlgebra.Matrix(Of Double)
            Matrix0_MathNet = Func_Vector3D_to_MathNetMatrix(Matrix_0)
            Matrix_Affin = Matrix_Affin + Matrix0_MathNet
        End If
        Matrix1_MathNet = Func_Vector3D_to_MathNetMatrix(Matrix_1)
        Matrix2_MathNet = Func_Vector3D_to_MathNetMatrix(Matrix_2)

        Matrix_Affin = Matrix_Affin + Matrix1_MathNet * MixingRule_1
        Matrix_Affin = Matrix_Affin + (MixingRule_2) * Matrix2_MathNet
        Matrix_Affin = Matrix_Affin.QR(Math_Net.LinearAlgebra.Factorization.QRMethod.Full).Q()
        Dim Matrix_Affin_det = Matrix_Affin.Determinant
        Matrix_Affin = Matrix_Affin / Matrix_Affin_det

        Func_Affine_Transformation = Func_MathNetMatrix_to_Vector3D(Matrix_Affin)

    End Function
    Private Function Func_Karcher(ByVal Simplex As Dictionary(Of Integer, Vector3d()), ByVal Fitness_List As List(Of Double)) As Math_Net.LinearAlgebra.Matrix(Of Double)

        Dim Middle_Matrix As Math_Net.LinearAlgebra.Matrix(Of Double)
        Middle_Matrix = Math_Net.LinearAlgebra.Double.Matrix.Build.Dense(3, 3)
        Dim Number_of_Matrixes = Simplex.Count

        For Matrix_key = 1 To Number_of_Matrixes - 1 Step 1
            Dim Matrix_key_mins As Integer = Fitness_List(Number_of_Matrixes + Matrix_key)
            Dim Matrix_MathNet = Func_Vector3D_to_MathNetMatrix(Simplex(Matrix_key_mins))
            Middle_Matrix = Middle_Matrix + Matrix_MathNet
        Next
        Middle_Matrix = Middle_Matrix / (Number_of_Matrixes - 1)
        Dim Mittel_Matrix_q = Middle_Matrix.QR(MathNet.Numerics.LinearAlgebra.Factorization.QRMethod.Full).Q()
        Middle_Matrix = Mittel_Matrix_q / Mittel_Matrix_q.Determinant

        Func_Karcher = Middle_Matrix
    End Function

    Private Sub Sub_Bounding_Box_Cloud(ByVal Rot_Matrix As Vector3d(),
                                       ByRef Delta As Double())

        Dim Points_act = Matrix_Points_coords
        Dim Rot_Matrix_math = Func_Vector3D_to_MathNetMatrix(Rot_Matrix)

        Dim Points_act_trans = Rot_Matrix_math.Transpose * Points_act

        Dim Points_act_trans_x_max = Points_act_trans.Row(0).Maximum()
        Dim Points_act_trans_x_min = Points_act_trans.Row(0).Minimum()
        Dim Points_act_trans_y_max = Points_act_trans.Row(1).Maximum()
        Dim Points_act_trans_y_min = Points_act_trans.Row(1).Minimum()
        Dim Points_act_trans_z_max = Points_act_trans.Row(2).Maximum()
        Dim Points_act_trans_z_min = Points_act_trans.Row(2).Minimum()

        Delta(0) = System.Math.Abs(Points_act_trans_x_max - Points_act_trans_x_min)
        Delta(1) = System.Math.Abs(Points_act_trans_y_max - Points_act_trans_y_min)
        Delta(2) = System.Math.Abs(Points_act_trans_z_max - Points_act_trans_z_min)

    End Sub
End Module