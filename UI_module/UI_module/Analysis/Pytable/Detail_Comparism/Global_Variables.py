# -*- coding: utf-8 -*-
import os,time,math,sys
import numpy as np

Algorithmus_Version="0.0"
Date="{}_{}_{}".format(time.localtime()[0:3][0],time.localtime()[0:3][1],time.localtime()[0:3][2])
separatori_sign_path=os.path.sep
delta_gitter=5 ## mm
## Pfade
save_paths={}
save_paths["Hauptdateipfade_NX"]=r"C:\Program Files\Siemens\NX 11.0"
save_paths["Hauptdateipfade_Datenbank"]=r"X:\03_Detailvergleich\Auto_Tunnel" #rD:\Bauteil_Karte"
## Hauptdateipfade_Datenbank werden im Code definiert
save_paths["Bauteile"]=os.path.normpath(u"/01_Daten-Bauteil")
## save_paths["parte_Pfad"] im Code definiert
save_paths["HDF5"]=os.path.normpath(u"/02_HDF5-Datenblaetter")
save_paths["Datenblaetter"]=os.path.normpath(u"/00_Datenblaetter")
save_paths["Info_Blatt"]=os.path.normpath(u"X:\03_Detailvergleich\Auto_Tunnel\Output_Ordner_Debugging") #u"/00_Info_allgemein")
## save_paths["Info_Blatt_Pfad"] im Code definiert
save_paths["Randbox"]=os.path.normpath(u"X:\03_Detailvergleich\Auto_Tunnel\Output_Ordner_Debugging") #u"/01_Minimale_Randbox")
## save_paths["Randbox_Pfad"] im Code definiert
save_paths["Flaechen_HDF5"]=os.path.normpath(u"X:\03_Detailvergleich\Auto_Tunnel\Output_Ordner_Debugging") #u"/02_Flaechenanalyse")
save_paths["Kruemmungen_HDF5"]=os.path.normpath(u"/xx_Kruemmung")
## Hauptdateipfade_NX werden im Code definiert
save_paths["NX_exe"]=os.path.normpath(u"/UGII/ugraf.exe")
save_paths["NX_run_managed"]=os.path.normpath(u"/NXBIN/run_managed.exe")
## Tools
save_paths["Hauptdateipfade_Tools"]=os.path.dirname(r"X:\03_Detailvergleich\Auto_Tunnel\Auswertung_Kruemmungsdaten\01_Tools") #os.path.abspath(unicode(__file__, sys.getfilesystemencoding( ))))+os.path.normpath(u"/01_Tools") 
save_paths["Assembly"]=os.path.normpath(u"/00_Assemblyzerlegung")
save_paths["Box"]=os.path.normpath(u"/01_Analysiere_Box.exe")
save_paths["Flaechen"]=os.path.normpath(u"/02_Analysiere_Flaechen.exe")
save_paths["Bilder"]=os.path.normpath(u"/03_Erstelle_Bilder.exe")
save_paths["Kruemmung"]=os.path.normpath(u"/xx_Curvaturedata")
## Zwischenspeicher

save_paths["Ergebnisse"]=save_paths["Hauptdateipfade_Datenbank"]+os.path.normpath(u"/Ergebnisse")
save_paths["Speicher"]=save_paths["Ergebnisse"]+os.path.normpath(u"/00_Speicher")
save_paths["Commandeur"]=save_paths["Ergebnisse"]+os.path.normpath(r"/Commandeur") ### ur flag deprecated (u means unicode / r means raw (bc of backslash))
if os.path.isdir(save_paths["Ergebnisse"])==False:
    os.mkdir(save_paths["Ergebnisse"])
if os.path.isdir(save_paths["Speicher"])==False:
    os.mkdir(save_paths["Speicher"])
if os.path.isdir(save_paths["Commandeur"])==False:
    os.mkdir(save_paths["Commandeur"])

save_paths["Datenbasis_Pickle"]=os.path.normpath(u"/00_Datenbasis.txt")


######################################################################################################################
## HDF5 Eintraege

# Format: speicher_HDF5_def[Name]=(Name,
                                  #HDF5-Root,
                                  #[Node1,Beschreibung],
                                  #[Node2, Beschreibung]...) 
HDF5_def={}

HDF5_def["Kruemmung"]=["Daten_Kruemmungsanalyse.h5",
                                "/",
                                ["Verteilung_Kruemmung","Kruemmungsverteilung auf gesamten part, nach ID sortiert"],
                                ["Datenpunkte_Kruemmung","Kruemmungen an diskreten Punkten auf NX-Flaechen"]]


## Kuremmungen
comparism_curvature_dict={}
comparism_curvature_dict["k_n_25"]=1
comparism_curvature_dict["k_n_15"]=2
comparism_curvature_dict["k_n_10"]=3
comparism_curvature_dict["k_n_05"]=4
comparism_curvature_dict["k_00"]=5
comparism_curvature_dict["k_p_05"]=6
comparism_curvature_dict["k_p_10"]=7
comparism_curvature_dict["k_p_15"]=8
comparism_curvature_dict["k_20"]=9
comparism_curvature_dict["k_p_25"]=10

list_parts=[]

class part():
    separator=os.path.sep
    
    def __init__(self,_ID,_part_dict_item, _box_achsen, parent=None):
        self.part_ID= _ID
        self.part_ID_str=str(self.part_ID)
        self.part_pfad=_part_dict_item[0]
        self.part_name=_part_dict_item[1]
        self.part_format=_part_dict_item[2]
        self.box_x=_box_achsen[0]
        self.box_y=_box_achsen[1]

## Klassen-Definitionen fuer Kruemmungsauswertung
class curvature_part():

    def __init__(self,_ID):
        self.ID=_ID

    def _read_HDF5_Table(self, _table):
        column_s=_table.colnames
        del column_s[0],column_s[-1]
        self.Curvaturedata_column_s=column_s
        for column in column_s:
            data_column=np.array(_table.cols._f_col(column))
            setattr(self,column,data_column)