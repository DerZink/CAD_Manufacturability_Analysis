Option Strict Off
Imports System
Imports System.Drawing
Imports NXOpen
Imports System.Collections.Generic
Imports System.ComponentModel
Imports System.Data
Imports System.Text
Imports NXOpen.UF
Imports Snap
Imports System.Windows.Forms
Imports SharedModule.Public_Variable

Module Source

    Public Sub Main(ByVal args As String())

        Try
            Console.WriteLine("## NX overlay assembly creation")
            Sub_Reading_Arguments(args)
            Dim Status_Start As New UFPart.LoadStatus
            Dim Tag_Start As New Tag '= Nothing
            Dim AssemblyFileName = Path_Output + Part_ID_a + "_vs_" + Part_ID_b + ".prt"
            '# Build the new Assembly file. Can be used with variable Part_act
            Sub_BuildFile(AssemblyFileName)

            theSession.Preferences.Assemblies.InterpartPositioning = True

            '# get parts and orient them
            _00_ImportAndPositioning.start()

            '# save assembly
            Dim partSaveStatus As NXOpen.PartSaveStatus = Nothing
            partSaveStatus = Part_act.Save(NXOpen.BasePart.SaveComponents.True, NXOpen.BasePart.CloseAfterSave.True)
            partSaveStatus.Dispose()

        Catch ex As Exception
            Console.WriteLine(ex.ToString)
            Dim Path_Exe_Act = Environment.CurrentDirectory()
            Dim timeOfDay As String = String.Format("{0}{1}", Now.TimeOfDay.Hours, Now.TimeOfDay.Minutes)
            Dim Error_File_Name As String = Date_now + "_Error_PartRotation_" + Part_ID_a + "_vs_" + Part_ID_b + "_" + timeOfDay + ".txt"
            Dim Error_File As IO.StreamWriter
            Error_File = My.Computer.FileSystem.OpenTextFileWriter(Path_Exe_Act + System.IO.Path.DirectorySeparatorChar.ToString + Error_File_Name, False)
            Error_File.WriteLine(ex.ToString)
            Error_File.WriteLine(Path_Output + Part_ID_a + "_vs_" + Part_ID_b)
            Error_File.Close()
        End Try

    End Sub

    Sub Sub_BuildFile(ByVal FilePath)
        '# check if file exists -> delete it

        Dim StatusFile As Boolean = My.Computer.FileSystem.FileExists(FilePath)
        If StatusFile = True Then
            My.Computer.FileSystem.DeleteFile(FilePath)
        End If

        Dim fileNew As NXOpen.FileNew = Nothing
        fileNew = theSession.Parts.FileNew()

        fileNew.TemplateFileName = "assembly-mm-template.prt"
        fileNew.UseBlankTemplate = False
        fileNew.ApplicationName = "AssemblyTemplate"
        fileNew.Units = NXOpen.Part.Units.Millimeters
        fileNew.RelationType = ""
        fileNew.UsesMasterModel = "No"
        fileNew.TemplateType = NXOpen.FileNewTemplateType.Item
        fileNew.TemplatePresentationName = "Assembly"
        fileNew.ItemType = ""
        fileNew.Specialization = ""
        fileNew.SetCanCreateAltrep(False)
        fileNew.NewFileName = FilePath
        fileNew.MasterFileName = ""
        fileNew.MakeDisplayedPart = True
        fileNew.DisplayPartOption = NXOpen.DisplayPartOption.AllowAdditional

        Dim nXObject1 As NXOpen.NXObject = Nothing
        nXObject1 = fileNew.Commit()

        Part_act = theSession.Parts.Work
        fileNew.Destroy()
    End Sub
End Module


