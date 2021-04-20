Imports NXOpen
Imports System
Imports NXOpen.UF
Imports NXOpen.UI
Imports NXOpen.Utilities
Imports Math_Net = MathNet.Numerics
Public Module _00_Min_Box

    Public Sub _start(Optional ByVal X_Axis_in As Vector3d = Nothing,
                      Optional ByVal Y_Axis_in As Vector3d = Nothing)

        Dim NullVector As New Vector3d(0, 0, 0)
        If X_Axis_in.Equals(NullVector) Then
            X_Axis_in = New Vector3d(1, 0, 0)
        End If
        If Y_Axis_in.Equals(NullVector) Then
            Y_Axis_in = New Vector3d(0, 1, 0)
        End If

        Sub_Box_Boundingpoints_Create(X_Axis_in, Y_Axis_in, False)

    End Sub

End Module
