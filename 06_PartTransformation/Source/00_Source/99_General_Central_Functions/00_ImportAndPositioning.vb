Imports NXOpen
Imports SharedModule.Public_Variable
Module _00_ImportAndPositioning

    Dim partIDs As Dictionary(Of String, String) = New Dictionary(Of String, String) From {{"a", Part_ID_a}, {"b", Part_ID_b}}
    Dim translations As Dictionary(Of String, Vector3d) = New Dictionary(Of String, Vector3d) From {{"a", Translation_a}, {"b", Translation_b}}
    Dim rotations As Dictionary(Of String, Matrix3x3) = New Dictionary(Of String, Matrix3x3) From {{"a", Rotation_a}, {"b", Rotation_b}}

    Public Sub start()

        For Each name As String In {"a", "b"}
            import(name)
        Next

    End Sub

    Sub import(ByVal NameOfPart As String)

        Dim addComponentBuilder As NXOpen.Assemblies.AddComponentBuilder = Nothing
        addComponentBuilder = Part_act.AssemblyManager.CreateAddComponentBuilder()
        addComponentBuilder.SetInitialLocationType(NXOpen.Assemblies.AddComponentBuilder.LocationType.WorkPartAbsolute)

        '# load part
        Dim basePart As NXOpen.BasePart = Nothing
        Dim partLoadStatus As NXOpen.PartLoadStatus = Nothing
        Dim FilePath As String = Path_Output + partIDs(NameOfPart) + Part_Ending
        basePart = theSession.Parts.OpenBase(FilePath, partLoadStatus)
        partLoadStatus.Dispose()
        addComponentBuilder.ReferenceSet = "Use Model"

        Dim partstouse(0) As NXOpen.BasePart
        Dim part As NXOpen.Part = CType(basePart, NXOpen.Part)

        partstouse(0) = part
        addComponentBuilder.SetPartsToAdd(partstouse)

        '# build assembly component of part
        Dim nXObject(0) As NXOpen.NXObject
        nXObject(0) = addComponentBuilder.Commit()
        addComponentBuilder.Destroy()

        '# positioning of body
        position(nXObject, NameOfPart)

        '# Show points of point cloud on surface and delete other points
        'clearPoints(nXObject(0))



    End Sub

    Sub position(ByVal partComponent() As NXOpen.NXObject, ByVal NameOfPart As String)

        Dim componentPositioner As NXOpen.Positioning.ComponentPositioner = Nothing
        componentPositioner = Part_act.ComponentAssembly.Positioner
        componentPositioner.ClearNetwork()
        'componentPositioner.BeginAssemblyConstraints()
        componentPositioner.BeginMoveComponent()

        Dim network As NXOpen.Positioning.Network = Nothing
        network = componentPositioner.EstablishNetwork()

        Dim componentNetwork As NXOpen.Positioning.ComponentNetwork = CType(network, NXOpen.Positioning.ComponentNetwork)
        componentNetwork.MoveObjectsState = True

        componentNetwork.NetworkArrangementsMode = NXOpen.Positioning.ComponentNetwork.ArrangementsMode.Existing
        componentNetwork.RemoveAllConstraints()

        componentNetwork.NetworkSolveInWorksetMode = False
        componentNetwork.SetMovingGroup(partComponent)

        componentNetwork.DragByTransform(translations(NameOfPart), rotations(NameOfPart))
        componentNetwork.Solve()

        componentPositioner.ClearNetwork()

    End Sub

    Sub clearPoints(ByVal partComponent As NXOpen.NXObject)
        Dim component As NXOpen.Assemblies.Component = CType(partComponent, NXOpen.Assemblies.Component)

        '# activate part
        Dim partLoadStatus1 As NXOpen.PartLoadStatus = Nothing
        theSession.Parts.SetWorkComponent(component, partLoadStatus1)
        Dim workPart = theSession.Parts.Work
        partLoadStatus1.Dispose()

        Dim theMarkId As Session.UndoMarkId =
                theSession.SetUndoMark(Session.MarkVisibility.Visible,
                                       "Delete Features")

        '# get points of feature group Grid_Askmin
        Dim FeatureGroupTag As Tag = Nothing
        theUFSession.Modl.AskSetFromName("Grid_Askmin", FeatureGroupTag)
        Dim FeatureGroup As Features.FeatureGroup = Utilities.NXObjectManager.Get(FeatureGroupTag)

        Dim points As Features.Feature() = Nothing
        FeatureGroup.GetMembers(points)

        '# delete points
        Dim poinObjs As NXObject() = CType(points, NXObject())
        theSession.UpdateManager.AddObjectsToDeleteList(poinObjs)
        theSession.UpdateManager.DoUpdate(theMarkId)

        '# go back to assembly
        Dim nullNXOpen_Assemblies_Component As NXOpen.Assemblies.Component = Nothing
        Dim partLoadStatus2 As NXOpen.PartLoadStatus = Nothing
        theSession.Parts.SetWorkComponent(nullNXOpen_Assemblies_Component, NXOpen.PartCollection.RefsetOption.Entire, NXOpen.PartCollection.WorkComponentOption.Visible, partLoadStatus2)

        '# change reference set of part to Entire Part
        Part_act = theSession.Parts.Work
        Dim components(0) As NXOpen.Assemblies.Component
        components(0) = component
        Part_act.ComponentAssembly.ReplaceReferenceSetInOwners("Entire Part", components)

    End Sub

End Module
