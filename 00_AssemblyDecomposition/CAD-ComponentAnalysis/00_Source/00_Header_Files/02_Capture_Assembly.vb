Imports NXOpen
Imports Snap
Imports SharedModule.Public_Variable


Public Module Mod_Capture_Assembly

    Public Sub Sub_Body_Thicken_And_Extract(ByRef body As Body)

        'Dim workPart As NXOpen.Part = theSession.Parts.Work
        Dim workBasePart As NXOpen.BasePart = theSession.Parts.Work

        Dim nullNXOpen_Features_Feature As NXOpen.Features.Feature = Nothing

        Dim thickenBuilder1 As NXOpen.Features.ThickenBuilder
        thickenBuilder1 = workBasePart.Features.CreateThickenBuilder(nullNXOpen_Features_Feature)
        'thickenBuilder1 = workPart.Features.CreateThickenBuilder(nullNXOpen_Features_Feature)
        thickenBuilder1.Tolerance = 0.01
        thickenBuilder1.FirstOffset.RightHandSide = "0.1"
        thickenBuilder1.SecondOffset.RightHandSide = "0"
        thickenBuilder1.BooleanOperation.Type = NXOpen.GeometricUtilities.BooleanOperation.BooleanType.Create

        Dim targetBodies1(0) As NXOpen.Body
        Dim nullNXOpen_Body As NXOpen.Body = Nothing

        targetBodies1(0) = nullNXOpen_Body
        thickenBuilder1.BooleanOperation.SetTargetBodies(targetBodies1)
        thickenBuilder1.RegionToPierce.DistanceTolerance = 0.01
        thickenBuilder1.RegionToPierce.ChainingTolerance = 0.0095

        Dim body1 As NXOpen.Body = body

        Dim faceBodyRule1 As NXOpen.FaceBodyRule
        faceBodyRule1 = workBasePart.ScRuleFactory.CreateRuleFaceBody(body1)
        'faceBodyRule1 = workPart.ScRuleFactory.CreateRuleFaceBody(body1)

        Dim rules1(0) As NXOpen.SelectionIntentRule
        rules1(0) = faceBodyRule1
        thickenBuilder1.FaceCollector.ReplaceRules(rules1, False)
        thickenBuilder1.RemoveGashes = True

        Dim nXObject1 As NXOpen.NXObject
        nXObject1 = thickenBuilder1.Commit()

        Dim thicken_object As NXOpen.Features.Thicken = Nothing
        thicken_object = CType(nXObject1, Features.Thicken)

        thickenBuilder1.Destroy()

        Dim wavePointBuilder1 As NXOpen.Features.WavePointBuilder
        wavePointBuilder1 = workBasePart.Features.CreateWavePointBuilder(nullNXOpen_Features_Feature)
        'wavePointBuilder1 = workPart.Features.CreateWavePointBuilder(nullNXOpen_Features_Feature)

        Dim waveDatumBuilder1 As NXOpen.Features.WaveDatumBuilder
        waveDatumBuilder1 = workBasePart.Features.CreateWaveDatumBuilder(nullNXOpen_Features_Feature)
        'waveDatumBuilder1 = workPart.Features.CreateWaveDatumBuilder(nullNXOpen_Features_Feature)

        Dim compositeCurveBuilder1 As NXOpen.Features.CompositeCurveBuilder
        compositeCurveBuilder1 = workBasePart.Features.CreateCompositeCurveBuilder(nullNXOpen_Features_Feature)
        'compositeCurveBuilder1 = workPart.Features.CreateCompositeCurveBuilder(nullNXOpen_Features_Feature)

        Dim extractFaceBuilder1 As NXOpen.Features.ExtractFaceBuilder
        extractFaceBuilder1 = workBasePart.Features.CreateExtractFaceBuilder(nullNXOpen_Features_Feature)
        'extractFaceBuilder1 = workPart.Features.CreateExtractFaceBuilder(nullNXOpen_Features_Feature)

        Dim mirrorBodyBuilder1 As NXOpen.Features.MirrorBodyBuilder
        mirrorBodyBuilder1 = workBasePart.Features.CreateMirrorBodyBuilder(nullNXOpen_Features_Feature)
        'mirrorBodyBuilder1 = workPart.Features.CreateMirrorBodyBuilder(nullNXOpen_Features_Feature)

        waveDatumBuilder1.ParentPart = NXOpen.Features.WaveDatumBuilder.ParentPartType.WorkPart
        wavePointBuilder1.ParentPart = NXOpen.Features.WavePointBuilder.ParentPartType.WorkPart
        extractFaceBuilder1.ParentPart = NXOpen.Features.ExtractFaceBuilder.ParentPartType.WorkPart
        mirrorBodyBuilder1.ParentPartType = NXOpen.Features.MirrorBodyBuilder.ParentPart.WorkPart
        compositeCurveBuilder1.ParentPart = NXOpen.Features.CompositeCurveBuilder.PartType.WorkPart

        compositeCurveBuilder1.Associative = False
        compositeCurveBuilder1.Section.DistanceTolerance = 0.01
        compositeCurveBuilder1.Section.ChainingTolerance = 0.0095

        extractFaceBuilder1.Associative = False
        extractFaceBuilder1.FixAtCurrentTimestamp = True
        extractFaceBuilder1.HideOriginal = False
        extractFaceBuilder1.InheritDisplayProperties = False
        extractFaceBuilder1.Type = NXOpen.Features.ExtractFaceBuilder.ExtractType.Body
        extractFaceBuilder1.CopyThreads = False
        extractFaceBuilder1.FeatureOption = NXOpen.Features.ExtractFaceBuilder.FeatureOptionType.OneFeatureForAllBodies

        Dim features1(0) As NXOpen.Features.Feature

        features1(0) = thicken_object
        Dim bodyFeatureRule1 As NXOpen.BodyFeatureRule
        bodyFeatureRule1 = workBasePart.ScRuleFactory.CreateRuleBodyFeature(features1, True)
        'bodyFeatureRule1 = workPart.ScRuleFactory.CreateRuleBodyFeature(features1, True)

        Dim rules2(0) As NXOpen.SelectionIntentRule
        rules2(0) = bodyFeatureRule1
        extractFaceBuilder1.ExtractBodyCollector.ReplaceRules(rules2, False)

        Dim nXObject2 As NXOpen.NXObject
        nXObject2 = extractFaceBuilder1.Commit()

        Dim Extract_Surface As NXOpen.Features.ExtractFace = Nothing

        Extract_Surface = CType(nXObject2, Features.ExtractFace)

        Dim Extrahierte_Flaeche_als_Body = Extract_Surface.GetBodies()

        body = Extrahierte_Flaeche_als_Body(0)

        compositeCurveBuilder1.Destroy()
        waveDatumBuilder1.Destroy()
        wavePointBuilder1.Destroy()
        extractFaceBuilder1.Destroy()
        mirrorBodyBuilder1.Destroy()

    End Sub

    Public Sub Sub_extract_Body(ByRef body As Body)

        'Dim workPart As NXOpen.Part = theSession.Parts.Work
        Dim workBasePart As NXOpen.BasePart = theSession.Parts.Work
        Dim nullNXOpen_Features_Feature As NXOpen.Features.Feature = Nothing

        Dim wavePointBuilder1 As NXOpen.Features.WavePointBuilder
        wavePointBuilder1 = workBasePart.Features.CreateWavePointBuilder(nullNXOpen_Features_Feature)
        'wavePointBuilder1 = workPart.Features.CreateWavePointBuilder(nullNXOpen_Features_Feature)

        Dim waveDatumBuilder1 As NXOpen.Features.WaveDatumBuilder
        waveDatumBuilder1 = workBasePart.Features.CreateWaveDatumBuilder(nullNXOpen_Features_Feature)
        'waveDatumBuilder1 = workPart.Features.CreateWaveDatumBuilder(nullNXOpen_Features_Feature)

        Dim compositeCurveBuilder1 As NXOpen.Features.CompositeCurveBuilder
        compositeCurveBuilder1 = workBasePart.Features.CreateCompositeCurveBuilder(nullNXOpen_Features_Feature)
        'compositeCurveBuilder1 = workPart.Features.CreateCompositeCurveBuilder(nullNXOpen_Features_Feature)

        Dim extractFaceBuilder1 As NXOpen.Features.ExtractFaceBuilder
        extractFaceBuilder1 = workBasePart.Features.CreateExtractFaceBuilder(nullNXOpen_Features_Feature)
        'extractFaceBuilder1 = workPart.Features.CreateExtractFaceBuilder(nullNXOpen_Features_Feature)

        Dim mirrorBodyBuilder1 As NXOpen.Features.MirrorBodyBuilder
        mirrorBodyBuilder1 = workBasePart.Features.CreateMirrorBodyBuilder(nullNXOpen_Features_Feature)
        'mirrorBodyBuilder1 = workPart.Features.CreateMirrorBodyBuilder(nullNXOpen_Features_Feature)

        compositeCurveBuilder1.Tolerance = 0.01

        compositeCurveBuilder1.Associative = False

        compositeCurveBuilder1.FixAtCurrentTimestamp = True

        waveDatumBuilder1.ParentPart = NXOpen.Features.WaveDatumBuilder.ParentPartType.WorkPart
        wavePointBuilder1.ParentPart = NXOpen.Features.WavePointBuilder.ParentPartType.WorkPart
        extractFaceBuilder1.ParentPart = NXOpen.Features.ExtractFaceBuilder.ParentPartType.WorkPart
        mirrorBodyBuilder1.ParentPartType = NXOpen.Features.MirrorBodyBuilder.ParentPart.WorkPart
        compositeCurveBuilder1.ParentPart = NXOpen.Features.CompositeCurveBuilder.PartType.WorkPart

        compositeCurveBuilder1.Associative = False
        compositeCurveBuilder1.Section.DistanceTolerance = 0.01
        compositeCurveBuilder1.Section.ChainingTolerance = 0.0095
        extractFaceBuilder1.Associative = False
        extractFaceBuilder1.FixAtCurrentTimestamp = True
        extractFaceBuilder1.HideOriginal = False
        extractFaceBuilder1.InheritDisplayProperties = False
        extractFaceBuilder1.Type = NXOpen.Features.ExtractFaceBuilder.ExtractType.Body
        extractFaceBuilder1.CopyThreads = False
        extractFaceBuilder1.FeatureOption = NXOpen.Features.ExtractFaceBuilder.FeatureOptionType.OneFeatureForAllBodies

        Dim bodies1(0) As NXOpen.Body

        bodies1(0) = body
        Dim bodyDumbRule1 As NXOpen.BodyDumbRule
        bodyDumbRule1 = workBasePart.ScRuleFactory.CreateRuleBodyDumb(bodies1, True)
        'bodyDumbRule1 = workPart.ScRuleFactory.CreateRuleBodyDumb(bodies1, True)

        Dim rules1(0) As NXOpen.SelectionIntentRule
        rules1(0) = bodyDumbRule1
        extractFaceBuilder1.ExtractBodyCollector.ReplaceRules(rules1, False)

        Dim nXObject1 As NXOpen.NXObject
        nXObject1 = extractFaceBuilder1.Commit()

        Dim Extrahierte_Flaeche As NXOpen.Features.ExtractFace = Nothing

        Extrahierte_Flaeche = CType(nXObject1, Features.ExtractFace)

        Dim Extrahierte_Flaeche_als_Body = Extrahierte_Flaeche.GetBodies()

        body = Extrahierte_Flaeche_als_Body(0)

        compositeCurveBuilder1.Destroy()
        waveDatumBuilder1.Destroy()
        wavePointBuilder1.Destroy()
        extractFaceBuilder1.Destroy()
        mirrorBodyBuilder1.Destroy()

    End Sub

    Public Function Func_joinFaces(ByVal body As Body) As Body
        '# see https://docs.plm.automation.siemens.com/data_services/resources/nx/1899/nx_api/custom/en_US/ugopen_doc/uf_modl/global.html#UF_MODL_edit_face_join
        Dim joinedBody As Tag = Nothing
        Dim faces(1) As Tag
        Dim outputBody As Body = Nothing
        Try
            theUFSession.Modl.EditFaceJoin(1, body.Tag, faces, joinedBody)
            Dim joinedBodyFeature As Features.BodyFeature = Utilities.NXObjectManager.Get(joinedBody)
            Dim joinedBodies As Body() = joinedBodyFeature.GetBodies()
            outputBody = joinedBodies(0)
        Catch ex As Exception
            outputBody = body
        End Try

        Return outputBody

    End Function
End Module