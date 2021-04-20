Imports NXOpen
Imports NXOpen.UF
Imports System.Data
Imports System.Collections.Generic
Imports Math_Net = MathNet.Numerics

Public Module Public_Variable
    'CSV
    '# General
    Public theUFSession As UFSession = UFSession.GetUFSession()
    Public theSession As Session = Session.GetSession()
    Public Display_Part As Part = theSession.Parts.Display

    '# Initialization of the variables for calling the files or generating output files
    '# Path and name of the component
    Public Part_Folder_Path As String
    Public Part_Name_org As String
    Public Part_Format As String
    Public Part_ID As String
    Public Output_Path_Part As String
    Public Data_Name As String
    Public Draft_Mode As Boolean = False

    'Start - Added for module 01 
    Public Output_CSV As New Dictionary(Of String, Double)
    'Start - Added for module 02
    Public Output_Subfolder_Curvature As String

    'End - Added for module 02

    'Public Ausgabe_Datei As IO.StreamWriter
    'End - Added for module 01 

    '# List of workparts and dict with details
    '# Liste:(Name,Prototype,Units)
    Public Workpart_Detail_Dict As New Dictionary(Of Tag, List(Of Object))
    Public Workpart_list As New List(Of NXOpen.Tag)
    Public Part_act As Part

    'Start - Added for module 01 
    '# List of bodies in Workpart
    Public Body_List() As Body
    Public nBody As Integer
    Public Body_act As Body

    Public newFacet As NXOpen.Tag

    '# Variables for Minimal Boundingbox
    Public DecimalsData As Integer = 6
    Public DirsSorted As List(Of VectorArithmetic.Vector3)
    Public BoxDir_1 As Vector3d
    Public BoxDir_2 As Vector3d
    Public Coordsys_Min_Box_ACS As CoordinateSystem '# Coordinate system of the minimum box
    Public Deltas(2) As Double '# Delta-x-y-z the minimum box
    Public Minimum_Boundingbox As Body
    Public Percent_volume_abort_criterion As Double = 0.00001 '# Originally 0.00001
    Public Necessary_vol_Min = 3 '# Originally 3


    Public PointsCloud As New Dictionary(Of Tuple(Of Integer, Integer, Integer), Double())
    Public power_accuracy As Integer = 3 '# Stellen
    Public Number_of_R0 As Integer
    Public Number_of_R1 As Integer
    Public Number_of_R2 As Integer
    Public NumberOfPoints As Integer
    Public DiscretizationStep As Double = 2
    Public delta_R0 As Double
    Public delta_R1 As Double
    Public delta_R2 As Double

    Public Matrix_Points_coords As Math_Net.LinearAlgebra.Matrix(Of Double)

    Public Curvature_categories As New List(Of String)(New String() {"k_n_25", "k_n_15", "k_n_10", "k_n_05", "k_00", "k_p_05", "k_p_10", "k_p_15", "k_20", "k_p_25"})
    Public Number_of_krPoints As Integer = 0
    'End - Added for module 01 

    'Start - Added for module 02 
    '# Surface analysis data as Dicts in class

    Public Surfaces_NX_Data_Dict As New Surfacesdict
    Public Surfaces_Merged_Data_Dict As New Surface_density_Own_calculation
    '# Output table for further processing
    Public Table_Output_NX As New CSV_Output_SurfaceData
    Public Table_Output_Neighbour As New CSV_Output_NeighborData
    Public Table_FaceType_Distribution_perNumber As New Table_FaceType_distribution_perNumber
    Public Table_FaceType_Distribution_perArea As New Table_FaceType_distribution_perArea
    'Public Table_Curvature_Surfaces As New Class_Table_Curvature_Distribution_Surface
    Public Neighbour_Dict As New Dictionary(Of Integer, List(Of Tag))
    Public Table_Distributions_body_PointCloud As New Class_Table_Distributions_Body_PointCloud
    Public Curvature_Output_Points As New Table_Curvature_Points
    '# Relationship of adjacent surfaces (edge, (Surface1, Surface2, relationship [concave = 0, convex = 1]))
    Public Neighbouring_Surfaces_relationship As New Dictionary(Of Tuple(Of Integer, Integer, Integer), String)
    Public Related_Neighbor As New Dictionary(Of Tag, HashSet(Of Tag))
    Public List_Correct_SurfacesRelationship As New List(Of Tag)
    Public List_Wrong_SurfacesRelationship As New List(Of Tag)


    Public Classification_of_surface_categories As New List(Of String)(New String() {"mainsurface", "transitionsurface", "featuresurface_concave", "featuresurface_convex"})
    Public NX_Surface_Categories As New List(Of String)(New String() {"nx_16", "nx_17", "nx_18", "nx_19", "nx_20", "nx_22", "nx_23", "nx_43", "nx_65", "nx_66"})

    Public Distribution_curvature_categories_body As New Dictionary(Of String, Double)
    Public Distribution_classification_surfaces_body As New Dictionary(Of String, Double)
    Public Distribution_NX_Surfaces_body As New Dictionary(Of String, Double)
    Public Distribution_Arrangement_Surfaces_Body_based As New Dictionary(Of String, Double)
    Public Distribution_NX_Surfaces_Body_based As New Dictionary(Of String, Double)
    Public Number_of_classification_surfaces As Integer = 0
    Public Number_of_NX_Surfaces As Integer = 0
    Public TotalSurfaces As Double = 0
    'End - Added for module 02 

    '# Definitions for Neighbouring Surfaces
    Public Max_Numbers_Main_Areas As Double = 0.7

    Public Resolution As String

    Public TDP_Path As String


    '# miscellaneous
    Public pi As Double = 3.14159265359
    Dim Year As String = Now.Year.ToString
    Dim Month As String = Now.Month.ToString
    Dim Tag As String = Now.Day.ToString
    Public Date_now As String = String.Format("{0}_{1}_{2}", Year, Month, Tag)


End Module
