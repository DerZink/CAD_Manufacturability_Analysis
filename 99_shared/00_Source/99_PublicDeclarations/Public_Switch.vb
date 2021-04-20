Imports NXOpen
Imports NXOpen.UF
Imports System.Data


Public Module Public_Switch
    '00,01,02,03 ------------
    '# Switch for the filtering of small components. 1 = on, 0 = off. Description of the functions depending on the position in the array:
    '# Digit1: Volume analysis, digit2: TBD
    Public Part_Filter = New Integer() {0, 0}
    '00,01,02,03 ------------
    'Public Part_Filter = New Integer() {1, 0} 'for 01,03

    '02 ------------
    '# Output of the surface normals from calculation angle relation neighborsurfaces
    Public Output_of_calculation_normal_in_NX As Boolean = False
    Public Coloring_of_combined_surfaces As Boolean = True
    Public ColorBy_type_of_surface As Boolean = True

    '# Switch for Batch_Processing (1 right away) 
    Public Batch_Processing As Integer = 0
    '02,03 ------------


End Module
