Imports NXOpen
Imports System
Imports NXOpen.UF
Imports NXOpen.UI
Imports NXOpen.Utilities
Imports Math_Net = MathNet.Numerics
Imports SharedModule.Public_Variable
Public Module Typ_Transformations


    Public Sub Sub_Vector_Common_to_Matrix3x3(ByVal Vector_1, ByVal Vector_2, ByVal Vector_3, ByRef Matrix)

        If Vector_1.GetType.ToString = "NXOpen.Vector3d" Then
            Dim Vector3D_1 As Vector3d = Vector_1
            Dim Vector3D_2 As Vector3d = Vector_2
            Dim Vector3D_3 As Vector3d = Vector_3
            Matrix.Xx = Vector3D_1.X
            Matrix.Xy = Vector3D_1.Y
            Matrix.Xz = Vector3D_1.Z
            Matrix.Yx = Vector3D_2.X
            Matrix.Yy = Vector3D_2.Y
            Matrix.Yz = Vector3D_2.Z
            Matrix.Zx = Vector3D_3.X
            Matrix.Zy = Vector3D_3.Y
            Matrix.Zz = Vector3D_3.Z

        ElseIf Vector_1.GetType.ToString = "NXOpen.VectorArithmetic.Vector3" Then
            Dim Vector3_1 As VectorArithmetic.Vector3 = Vector_1
            Dim Vector3_2 As VectorArithmetic.Vector3 = Vector_2
            Dim Vector3_3 As VectorArithmetic.Vector3 = Vector_3
            Matrix.Xx = Vector3_1.x
            Matrix.Xy = Vector3_1.y
            Matrix.Xz = Vector3_1.z
            Matrix.Yx = Vector3_2.x
            Matrix.Yy = Vector3_2.y
            Matrix.Yz = Vector3_2.z
            Matrix.Zx = Vector3_3.x
            Matrix.Zy = Vector3_3.y
            Matrix.Zz = Vector3_3.z

        ElseIf Vector_1.GetType.ToString = "System.Double[]" Then
            Dim VectorD_1() As Double = Vector_1
            Dim VectorD_2() As Double = Vector_2
            Dim VectorD_3() As Double = Vector_3
            Matrix.Xx = VectorD_1(0)
            Matrix.Xy = VectorD_1(1)
            Matrix.Xz = VectorD_1(2)
            Matrix.Yx = VectorD_2(0)
            Matrix.Yy = VectorD_2(1)
            Matrix.Yz = VectorD_2(2)
            Matrix.Zx = VectorD_3(0)
            Matrix.Zy = VectorD_3(1)
            Matrix.Zz = VectorD_3(2)
        End If

    End Sub
    Public Sub Func_Vectortrans_using_ACS(ByVal Origin As Point3d, ByVal Dirs(,) As Double, ByRef Vector() As Double)

        Dim Absolute_Coordinatesystem() As Double = {0, 0, 0, 1, 0, 0, 0, 1, 0}
        Dim Dirs_Coordinatesystem() As Double = {Origin.X, Origin.Y, Origin.Z, Dirs(0, 0), Dirs(0, 1), Dirs(0, 2), Dirs(1, 0), Dirs(1, 1), Dirs(1, 2)}

        Dim Matrix(11) As Double
        Dim Status As Integer = 0

        theUFSession.Trns.CreateCsysMappingMatrix(Absolute_Coordinatesystem, Dirs_Coordinatesystem, Matrix, Status)
        theUFSession.Trns.MapPosition(Vector, Matrix)

    End Sub
    Public Function Func_Vector3_to_Point3d(ByVal Vector_3D As VectorArithmetic.Vector3) As Point3d
        Dim Point_3d As New Point3d(Vector_3D.x, Vector_3D.y, Vector_3D.z)
        Func_Vector3_to_Point3d = Point_3d
    End Function
    Public Function Func_Vector3_to_Vector3d(ByVal Vector_3D As VectorArithmetic.Vector3) As Vector3d
        Dim vector_3d_out As New Vector3d(Vector_3D.x, Vector_3D.y, Vector_3D.z)
        Func_Vector3_to_Vector3d = vector_3d_out
    End Function
    Public Function Func_Vector3_to_Double(ByVal Vector_3D As VectorArithmetic.Vector3) As Double()
        Dim Vector_double() As Double
        Vector_double = {Vector_3D.x, Vector_3D.y, Vector_3D.z}
        Func_Vector3_to_Double = Vector_double
    End Function
    Public Function Func_Vector3List_toDouble2DArray(ByVal VectorList As List(Of VectorArithmetic.Vector3)) As Double(,)
        Dim Double2dArray(2, 2) As Double
        Dim vecCount As Integer = 0
        For Each vector In VectorList
            Double2dArray(vecCount, 0) = vector.x
            Double2dArray(vecCount, 1) = vector.y
            Double2dArray(vecCount, 2) = vector.z
            vecCount += 1
        Next
        Func_Vector3List_toDouble2DArray = Double2dArray
    End Function
    Public Function Func_Vector3d_to_Double(ByVal Vector_3D As Vector3d) As Double()
        Dim Vector_double() As Double
        Vector_double = {Vector_3D.X, Vector_3D.Y, Vector_3D.Z}
        Func_Vector3d_to_Double = Vector_double
    End Function
    Public Function Func_Double_to_Vector3d(ByVal Vector_double() As Double) As Vector3d
        Dim Vector_3d As New Vector3d(Vector_double(0), Vector_double(1), Vector_double(2))
        Func_Double_to_Vector3d = Vector_3d
    End Function
    Public Function Func_Double_to_Vector3(ByVal Vector_double() As Double) As VectorArithmetic.Vector3
        Dim Vector_3 As New VectorArithmetic.Vector3(Vector_double(0), Vector_double(1), Vector_double(2))
        Func_Double_to_Vector3 = Vector_3
    End Function
    Public Function Func_Double2DArray_toVector3List(ByVal Array2d(,) As Double) As List(Of VectorArithmetic.Vector3)
        Dim VectorList As New List(Of VectorArithmetic.Vector3)
        For jj As Integer = 0 To 2
            Dim Double_j(2) As Double
            For kk As Integer = 0 To 2
                Double_j(kk) = Array2d(jj, kk)
            Next
            VectorList.Add(Func_Double_to_Vector3(Double_j))
        Next
        Func_Double2DArray_toVector3List = VectorList
    End Function
    Public Function Func_Double_to_Point3d(ByVal Point_double() As Double) As Point3d
        Dim Point_3d As New Point3d(Point_double(0), Point_double(1), Point_double(2))
        Func_Double_to_Point3d = Point_3d
    End Function
    Public Function Func_Vector3D_to_MathNetMatrix(ByVal Vector3D As Vector3d()) As Math_Net.LinearAlgebra.Matrix(Of Double)

        Dim Matrix_Temp As Math_Net.LinearAlgebra.Matrix(Of Double) = Nothing
        Dim Length = Vector3D.Length
        Matrix_Temp = Math_Net.LinearAlgebra.Double.DenseMatrix.Build.Dense(3, Length)
        Dim Column As Integer = 0
        For Each Vector In Vector3D
            Matrix_Temp.Item(0, Column) = Vector.X
            Matrix_Temp.Item(1, Column) = Vector.Y
            Matrix_Temp.Item(2, Column) = Vector.Z
            Column += 1
        Next
        Func_Vector3D_to_MathNetMatrix = Matrix_Temp
    End Function
    Public Function Func_MathNetMatrix_to_Vector3D(ByVal Matrix As Math_Net.LinearAlgebra.Matrix(Of Double)) As Vector3d()

        Dim Vector_Temp_List As New List(Of Vector3d)
        Dim Column As Integer = 0
        Dim Number_of_Column As Integer = Matrix.ColumnCount
        While Column < Number_of_Column
            Dim Vector_Temp_individually As New Vector3d(Matrix.Item(0, Column), Matrix.Item(1, Column), Matrix.Item(2, Column))
            Vector_Temp_List.Add(Vector_Temp_individually)
            Column += 1
        End While
        Dim Vector_Temp() As Vector3d = {Vector_Temp_List(0), Vector_Temp_List(1), Vector_Temp_List(2)}
        Func_MathNetMatrix_to_Vector3D = Vector_Temp
    End Function

    Public Function Func_Double3D_to_MathNetMatrix(ByVal Double3D As Double()()) As Math_Net.LinearAlgebra.Matrix(Of Double)

        Dim Matrix_Temp As Math_Net.LinearAlgebra.Matrix(Of Double) = Nothing
        Dim Length = Double3D.Length
        Matrix_Temp = Math_Net.LinearAlgebra.Double.DenseMatrix.Build.Dense(3, Length)
        Dim Column As Integer = 0
        For Each Vector In Double3D
            Matrix_Temp.Item(0, Column) = Vector(0)
            Matrix_Temp.Item(1, Column) = Vector(1)
            Matrix_Temp.Item(2, Column) = Vector(2)
            Column += 1
        Next
        Func_Double3D_to_MathNetMatrix = Matrix_Temp
    End Function

End Module