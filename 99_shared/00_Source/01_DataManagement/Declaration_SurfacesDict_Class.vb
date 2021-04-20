Imports NXOpen
Imports NXOpen.UF


Public Class Surfacesdict

    '# Declarations of the properties
    Public Property Surfacecontents As New Property_Zink
    Public Property NXID As New Property_Zink
    Public Property NeighbourSurfaces As New Property_Zink
    Public Property Type As New Property_Zink
    Public Property Point As New Property_Zink
    Public Property Dir As New Property_Zink
    Public Property Radius As New Property_Zink
    Public Property Raidus_data As New Property_Zink
    Public Property Norm_Dir As New Property_Zink
    Public Property uv As New Property_Zink
    Public Property P_Point As New Property_Zink
    Public Property u1 As New Property_Zink
    Public Property v1 As New Property_Zink
    Public Property u2 As New Property_Zink
    Public Property v2 As New Property_Zink
    Public Property P_Norm As New Property_Zink
    Public Property P_Radius As New Property_Zink
    '# additionally
    Public Property Edge As New Property_Zink

    Public Property Number_Of_Convex As New Property_Zink
    Public Property number_of_Concave As New Property_Zink
    Public Property NumberOf_Plane As New Property_Zink

    Public Property Orientation As New Property_Zink

    Public Class Property_Zink

        Private _Dict As New Dictionary(Of Tag, Object)

        Public Sub _Entry(ByVal Tag As Tag, ByVal Value As Object)
            _Dict(Tag) = Value
        End Sub

        Public Function _DictOutput() As Dictionary(Of Tag, Object)
            _DictOutput = _Dict
        End Function

        Public Function _ValueOutput(ByVal Tag As Tag) As Object
            If _Dict.ContainsKey(Tag) Then
                _ValueOutput = _Dict(Tag)
            Else
                _ValueOutput = Nothing
            End If
        End Function
    End Class

End Class
Public Class Surface_density_Own_calculation

    '# Declarations of the properties
    Public Max_ID As Integer
    Public Property Surfacecontents As New Property_Zink
    Public Property Neighbours As New Property_Zink
    Public Property Number_Of_Convex As New Property_Zink
    Public Property number_of_Concave As New Property_Zink
    Public Property Neighbour_Tags As New Property_Zink


    Public Class Property_Zink

        Private _Dict As New Dictionary(Of Integer, Object)

        Public Sub _Entry(ByVal ID As Integer, ByVal Value As Object)
            _Dict(ID) = Value
        End Sub

        Public Function _DictOutput() As Dictionary(Of Integer, Object)
            _DictOutput = _Dict
        End Function

        Public Function _ValueOutput(ByVal ID As Integer) As Object
            If _Dict.ContainsKey(ID) Then
                _ValueOutput = _Dict(ID)
            Else
                _ValueOutput = Nothing
            End If
        End Function
    End Class

End Class


