Imports NXOpen
Imports Snap


Public Module Capture_Assembly

    Public Sub Sub_Assembly_Structure()


        '# Prt.File will be opened
        Dim Status_Start As New UF.UFPart.LoadStatus()
        Dim Tag_Start As New Tag '= Nothing
        Dim File = Part_Folder_Path + Part_Name_org + Part_Format
        theUFSession.Part.Open(File, Tag_Start, Status_Start)
        Dim Start_Part As Part = Utilities.NXObjectManager.Get(Tag_Start)
        Dim Root_Part As Assemblies.Component = Start_Part.ComponentAssembly.RootComponent

        '# Locate the children when RootPart exists and save in Dictionary Parts_Dict[Tag, (Name,Units)]
        '# or the individual parts in Workpart_list[Tag]
        If Utilities.NXObjectManager.Equals(Root_Part, Nothing) <> True Then
            '# Subassemblies "children" = components are searched
            Part_Finder(Root_Part)
        Else
            '# Routine for item
            Dim Child_List As New List(Of Object)
            If Start_Part.Name = "" Then
                Child_List.Add(Start_Part.JournalIdentifier)
            Else
                Child_List.Add(Start_Part.Name)
            End If
            Dim Unit_System As Integer
            Unit_Check(Unit_System, Start_Part)
            Child_List.Add(Unit_System)
            Workpart_Detail_Dict.Add(Start_Part.Tag, Child_List)
            Workpart_list.Add(Start_Part.Tag)

        End If

    End Sub

    Private Sub Part_Finder(ByVal Part As Assemblies.Component)

        '# List of children from RootPart is createdt
        Dim Children As Assemblies.Component() = Part.GetChildren
        For Each Child In Children
            If TypeOf Child.Prototype Is Part = True Then
                '# Error in NRW object can not be converted to Part
                Dim Workpart As Part = Child.Prototype
                '# Check whether Workpart has already been recorded (for example, about another component group)
                If Workpart_Detail_Dict.ContainsKey(Workpart.Tag) = False Then
                    Dim Workpart_Detail_List As New List(Of Object)
                    If Workpart.Name = "" Then
                        Workpart_Detail_List.Add(Workpart.JournalIdentifier)
                    Else
                        Workpart_Detail_List.Add(Workpart.Name)
                    End If
                    Dim UnitSystem As Integer
                    Unit_Check(UnitSystem, Workpart)
                    Workpart_Detail_List.Add(UnitSystem)
                    Workpart_Detail_Dict.Add(Workpart.Tag, Workpart_Detail_List)

                    '# Pre-filter of components based on different criteria
                    Dim Switch_Part As Integer = 1
                    '# Volume filter: control of the component volume compared to minimum component volume (see Public_Variable)
                    If Part_Filter(0) = 1 Then
                        VolumeAnalysis(Workpart, Switch_Part)
                    End If
                    '# Other filters (material etc, TBD)
                    If Switch_Part = 1 Then
                        Workpart_list.Add(Workpart.Tag)
                    End If
                End If
            End If

            '# Recursive : Function calls itself up again to find more children! 
            Part_Finder(Child)
        Next
    End Sub

    Private Sub VolumeAnalysis(ByRef Workpart As Part, ByRef Schalter_Part As Integer)

        Dim mm As MeasureManager = Workpart.MeasureManager()
        Dim mb As MeasureBodies

        Dim massUnits(4) As Unit
        massUnits(0) = CType(Workpart.UnitCollection.FindObject("SquareMilliMeter"), Unit)
        massUnits(1) = CType(Workpart.UnitCollection.FindObject("CubicMilliMeter"), Unit)
        massUnits(2) = CType(Workpart.UnitCollection.FindObject("Kilogram"), Unit)
        massUnits(3) = CType(Workpart.UnitCollection.FindObject("MilliMeter"), Unit)

        Dim iBody(0) As IBody
        Dim Body_number As Integer = 0
        Dim TotalVolume As Double = 0

        Dim bodyColl As NXOpen.BodyCollection = Workpart.Bodies
        For Each body As Body In bodyColl
            If body.IsSheetBody Then
                Dim test As Integer
                test = 1
            End If
            iBody(0) = body
            mb = mm.NewMassProperties(massUnits, 0.99, iBody)
            'Fenster_NX.WriteLine("Tag: " & body.Tag & "Name_Part: " & Workpart.Name & "Name_Body: " & body.Name & " Volume: " & mb.Volume.ToString() & massUnits(1).Abbreviation())
            TotalVolume += mb.Volume
            Body_number += 1
        Next
        'Fenster_NX.WriteLine("Total volume: " & TotalVolume.ToString & " Number : " & Body_number.ToString)
    End Sub

    Private Sub Unit_Check(ByRef Units As Integer, ByVal Bauteil As Part)

        '# Controls the unit system
        Dim partUnits As Integer
        theUFSession.Part.AskUnits(Bauteil.Tag, partUnits)
        If partUnits = UF.UFConstants.UF_PART_ENGLISH Then
            Units = 1       '#  Pounds
        ElseIf partUnits = UF.UFConstants.UF_PART_METRIC Then
            Units = 4       '# Kilograms
        End If
    End Sub

End Module