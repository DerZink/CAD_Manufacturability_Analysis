' NX 1899
' Journal created by Zink on Mon Jan 27 13:16:31 2020 Mitteleuropäische Zeit

'
Imports System
Imports NXOpen

Imports System.Collections.Generic

Module NXJournal
Sub Main (ByVal args() As String) 

Dim theSession As NXOpen.Session = NXOpen.Session.GetSession()
Dim workPart As NXOpen.Part = theSession.Parts.Work

Dim displayPart As NXOpen.Part = theSession.Parts.Display

Dim origin As NXOpen.Point3d
origin.X = 0
origin.Y = 0
origin.Z = 0

Dim x_0 As NXOpen.Vector3d
x_0.X = 1
x_0.Y = 0
x_0.Z = 0

Dim y_0 As NXOpen.Vector3d
y_0.X = 0
y_0.Y = 1
y_0.Z = 0

Dim translation As NXOpen.Point3d
translation.X = -4.939e+02
translation.Y = 1.435e+02
translation.Z = -6.190e+02

Dim rotation_x As NXOpen.Vector3d
rotation_x.X = 9.240e-01
rotation_x.Y = -3.410e-01
rotation_x.Z = -1.720e-01

Dim rotation_y As NXOpen.Vector3d
rotation_y.X = 1.710e-01
rotation_y.Y = 7.710e-01
rotation_y.Z = -6.130e-01

Dim body As NXOpen.NXObject = CType(workPart.Bodies.FindObject("UNPARAMETERIZED_FEATURE(0)"), NXOpen.NXObject)
' Dim body As NXOpen.NXObject = CType(workPart.Bodies.FindObject("BLOCK(1263)"), NXOpen.Body)

Dim pointObjectsList As New List(Of NXOpen.NXObject)

' For i As Integer = 2 To 1152 Step 2
	' Dim pointFeature_i As NXOpen.Features.PointFeature = CType(workPart.Features.FindObject("POINT(" + i.ToString + ")"), NXOpen.Features.PointFeature)
	' Dim point_i As NXOpen.Point = CType(pointFeature_i.FindObject("POINT 1"), NXOpen.Point)
	' pointObjectsList.add(point_i)
' Next

pointObjectsList.add(body)

Dim moveObject() As NXOpen.NXObject
moveObject = pointObjectsList.ToArray()
' moveObject = {body}


'##################################################################################
Dim nullNXOpen_Features_MoveObject As NXOpen.Features.MoveObject = Nothing
Dim moveObjectBuilder_rot As NXOpen.Features.MoveObjectBuilder = Nothing
moveObjectBuilder_rot = workPart.BaseFeatures.CreateMoveObjectBuilder(nullNXOpen_Features_MoveObject)
moveObjectBuilder_rot.TransformMotion.DeltaEnum = NXOpen.GeometricUtilities.ModlMotion.Delta.ReferenceAcsWorkPart
moveObjectBuilder_rot.TransformMotion.Option = NXOpen.GeometricUtilities.ModlMotion.Options.CsysToCsys
moveObjectBuilder_rot.MoveObjectResult = NXOpen.Features.MoveObjectBuilder.MoveObjectResultOptions.CopyOriginal


Dim added2 As Boolean = Nothing
added2 = moveObjectBuilder_rot.ObjectToMoveObject.Add(moveObject)

Dim unit2 As NXOpen.Unit = Nothing
unit2 = moveObjectBuilder_rot.TransformMotion.RadialOriginDistance.Units

Dim xform1 As NXOpen.Xform = Nothing
xform1 = workPart.Xforms.CreateXform(origin, x_0, y_0, NXOpen.SmartObject.UpdateOption.WithinModeling, 1.0)

Dim cartesianCoordinateSystem1 As NXOpen.CartesianCoordinateSystem = Nothing
cartesianCoordinateSystem1 = workPart.CoordinateSystems.CreateCoordinateSystem(xform1, NXOpen.SmartObject.UpdateOption.WithinModeling)

moveObjectBuilder_rot.TransformMotion.FromCsys = cartesianCoordinateSystem1

Dim xform3 As NXOpen.Xform = Nothing
xform3 = workPart.Xforms.CreateXform(origin, rotation_x, rotation_y, NXOpen.SmartObject.UpdateOption.WithinModeling, 1.0)
Dim cartesianCoordinateSystem3 As NXOpen.CartesianCoordinateSystem = Nothing
cartesianCoordinateSystem3 = workPart.CoordinateSystems.CreateCoordinateSystem(xform3, NXOpen.SmartObject.UpdateOption.WithinModeling)
moveObjectBuilder_rot.TransformMotion.ToCsys = cartesianCoordinateSystem3


Dim nXObject2 As NXOpen.NXObject = Nothing
nXObject2 = moveObjectBuilder_rot.Commit()

Dim objects2() As NXOpen.NXObject
objects2 = moveObjectBuilder_rot.GetCommittedObjects()

moveObjectBuilder_rot.Destroy()


'##################################################################################
' Dim NXObjectRotated() As NXOpen.NXObject  = Utilities.NXObjectManager.Get(objects2(0).tag)

Dim moveObjectBuilder1 As NXOpen.Features.MoveObjectBuilder = Nothing
moveObjectBuilder1 = workPart.BaseFeatures.CreateMoveObjectBuilder(nullNXOpen_Features_MoveObject)
moveObjectBuilder1.TransformMotion.DeltaEnum = NXOpen.GeometricUtilities.ModlMotion.Delta.ReferenceAcsWorkPart
moveObjectBuilder1.TransformMotion.Option = NXOpen.GeometricUtilities.ModlMotion.Options.CsysToCsys
moveObjectBuilder1.MoveObjectResult = NXOpen.Features.MoveObjectBuilder.MoveObjectResultOptions.MoveOriginal


Dim added1 As Boolean = Nothing
added1 = moveObjectBuilder1.ObjectToMoveObject.Add(objects2)

Dim unit1 As NXOpen.Unit = Nothing
unit1 = moveObjectBuilder1.TransformMotion.RadialOriginDistance.Units

moveObjectBuilder1.TransformMotion.FromCsys = cartesianCoordinateSystem1

Dim xform2 As NXOpen.Xform = Nothing
xform2 = workPart.Xforms.CreateXform(translation, x_0, y_0, NXOpen.SmartObject.UpdateOption.WithinModeling, 1.0)
Dim cartesianCoordinateSystem2 As NXOpen.CartesianCoordinateSystem = Nothing
cartesianCoordinateSystem2 = workPart.CoordinateSystems.CreateCoordinateSystem(xform2, NXOpen.SmartObject.UpdateOption.WithinModeling)
moveObjectBuilder1.TransformMotion.ToCsys = cartesianCoordinateSystem2


Dim nXObject1 As NXOpen.NXObject = Nothing
nXObject1 = moveObjectBuilder1.Commit()

Dim objects1() As NXOpen.NXObject
objects1 = moveObjectBuilder1.GetCommittedObjects()

moveObjectBuilder1.Destroy()

End Sub
End Module