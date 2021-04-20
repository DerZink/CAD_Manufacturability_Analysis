Option Strict Off
Imports System
Imports NXOpen
Imports NXOpen.UF
Imports Snap
Imports SharedModule.Public_Variable
Imports SharedModule.File_Management
Imports SharedModule.Capture_Assembly

Module Root

    Public Sub Main(ByVal args As String())

        Dim Part_ID_temp As Integer
        Dim Assembly_ID As String = ""
        Dim Name_Memory_Act As String = ""
        Try
            Sub_Reading_Arguments(args)
            Sub_Assembly_Structure()

            Assembly_ID = Part_ID
            Part_ID_temp = 0 'CInt(Val(Part_ID))
            Dim Body_ID As Integer = 0

            For Each Workpart In Workpart_list
                Dim PartLoadStatus As PartLoadStatus = Nothing
                Part_act = Utilities.NXObjectManager.Get(Workpart)
                Part_act.UnitCollection.SetDefaultDataEntryUnits(UnitCollection.UnitDefaults.KgMmNDegC)

                theSession.Parts.SetDisplay(Part_act, False, False, PartLoadStatus)
                PartLoadStatus.Dispose()

                Dim Part_Backup_Status As PartSaveStatus = Nothing

                '#Thickening of the component
                Dim bodyColl As NXOpen.BodyCollection = Part_act.Bodies
                Dim Body_List As New List(Of Body)

                For Each singleBody As Body In bodyColl
                    Body_List.Add(singleBody)
                Next

                For Each body As Body In Body_List

                    Try

                        If body.IsSheetBody Then
                            Sub_Body_Thicken_And_Extract(body)
                        Else
                            '# join faces 
                            body = Func_joinFaces(body)
                        End If

                        Dim Current_Output_Folder_Path As String
                        Dim Output_Part_Export As String = Nothing
                        Dim Name_Part As String = Body_ID.ToString("D5")
                        Current_Output_Folder_Path = Output_Path_Part + "\" + Name_Part + "\"
                        Output_Part_Export = Current_Output_Folder_Path + Name_Part + ".prt"

                        If Not My.Computer.FileSystem.DirectoryExists(Current_Output_Folder_Path) Then
                            My.Computer.FileSystem.CreateDirectory(Current_Output_Folder_Path)
                        End If

                        Sub_Delete_Existing_Files(Output_Part_Export)

                        Dim myOptions As UFPart.ExportOptions
                        myOptions.params_mode = UFPart.ExportParamsMode.RemoveParams
                        myOptions.new_part = True

                        '# put the tag in array
                        Dim BodyTag(0) As Tag
                        BodyTag(0) = body.Tag()

                        theUFSession.Part.ExportWithOptions(Output_Part_Export, 1, BodyTag, myOptions)
                        Body_ID += 1
                        Part_ID_temp += 1

                    Catch ex As Exception
                        ErrorFile(ex.ToString, Part_ID_temp, Assembly_ID, Name_Memory_Act)
                    End Try
                Next

                'Assembly_ID += 1
            Next


        Catch ex As Exception
            Console.WriteLine(ex.ToString)
            ErrorFile(ex.ToString, Part_ID_temp, Assembly_ID, Name_Memory_Act)
        End Try

    End Sub


    Private Sub ErrorFile(ByVal _ex As String, ByVal _Part_ID_temp As Integer,
                            ByVal _Assembly_ID As String, ByVal _Name_MemoryAct As String)
        Dim Path_Exe_Act = Environment.CurrentDirectory()
        Dim Uhrtime As String = String.Format("{0}{1}", Now.TimeOfDay.Hours, Now.TimeOfDay.Minutes)
        Dim Error_File_Name As String = Date_now + "_Error_Assemblyresolution_" + Part_Name_org + "_" + _Part_ID_temp.ToString + "_" + Uhrtime + ".txt"
        Dim Error_File As IO.StreamWriter
        Error_File = My.Computer.FileSystem.OpenTextFileWriter(Path_Exe_Act + System.IO.Path.DirectorySeparatorChar.ToString + Error_File_Name, False)
        Error_File.WriteLine(_ex)
        Error_File.WriteLine(String.Format("ID:{0}, AssID:{1}, Ordner:{2}", _Part_ID_temp.ToString, _Assembly_ID.ToString, _Name_MemoryAct))
        Error_File.Close()
    End Sub

End Module


