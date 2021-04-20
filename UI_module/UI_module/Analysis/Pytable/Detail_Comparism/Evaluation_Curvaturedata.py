# -*- coding: utf-8 -*-
import Global_Variables, AA_Data_creation, BB_HDF5_Table_create
import CC_Evaluation_of_Data

def def_parts():
    import random
    part_list=[]
    ## part_1
    part_path="Grober Unsinn"#r"C:\Users\Robin\Desktop\01_Hiwi\03_Detailvergleich\Auto_Tunnel\Output_Ordner_Debugging\Bauteil_Karte" #r"D:\Bauteil_Karte"
    part_name="Freiform"
    part_format="prt"
    part_box_x_0=(1,0,0)
    part_box_y_0=(0,1,0)
    #part_list.append(Globale_Variablen.part(0,
    #                                    (part_path,part_name,part_format),
    #                                    (part_box_x_0,part_box_y_0)))
    #part_name_1="Freiform_versetzt"
    ##part_box_x_1=(0.500865775,0.352040721,0.790696406)
    ##part_box_y_1=(-0.866098322,0.203425976,0.456608769)
    #part_list.append(Globale_Variablen.part(1,
    #                                    (part_path,part_name_1,part_format),
    #                                    (part_box_x_0,part_box_y_0)))

    #part_box_x_1=(0.500865775,0.352040721,0.790696406)
    #part_box_y_1=(-0.866098322,0.203425976,0.456608769)
    #part_list.append(Globale_Variablen.part(2,
    #                                    (part_path,part_name_1,part_format),
    #                                    (part_box_x_1,part_box_y_1)))


    #part_box_x_2=(random.random(),random.random(),random.random())
    #part_box_y_2=(random.random(),random.random(),random.random())
    #part_list.append(Globale_Variablen.part(3,
    #                                    (part_path,part_name,part_format),
    #                                    (part_box_x_2,part_box_y_2)))

    #part_name_3="Freiform_konturversetzt"
    #part_list.append(Globale_Variablen.part(4,
    #                                    (part_path,part_name_3,part_format),
    #                                    (part_box_x_0,part_box_y_0)))
    #part_name_4="Freiform_konturmanipuliert"
    #part_list.append(Globale_Variablen.part(5,
    #                                    (part_path,part_name_4,part_format),
    #                                    (part_box_x_0,part_box_y_0)))

    #part_name_5="V222_Gesamtfahrzeug_1432_V222 Heckwagen_stp_Koerper_255"
    #part_list.append(Globale_Variablen.part(5,
    #                                    (part_path,part_name_5,part_format),
    #                                    (part_box_x_0,part_box_y_0)))
    #part_name_6="V222 Itraeger_Montageteile_Front_stp_d_Koerper_42"
    #part_list.append(Globale_Variablen.part(6,
    #                                    (part_path,part_name_6,part_format),
    #                                    (part_box_x_0,part_box_y_0)))
    #part_name_7="V222_Gesamtfahrzeug_255_A2226302016_3_Koerper_0"
    #part_list.append(Globale_Variablen.part(7,
    #                                    (part_path,part_name_7,part_format),
    #                                    (part_box_x_0,part_box_y_0)))
    part_name_8="V222_Gesamtfahrzeug_1430_V222 Hauptboden_stp_Koerper_3"
    part_list.append(Global_Variables.part(0,
                                        (part_path,part_name_8,part_format),
                                        (part_box_x_0,part_box_y_0)))
    part_name_9="V222_Gesamtfahrzeug_1430_V222 Hauptboden_stp_Koerper_3_Beule"
    part_list.append(Global_Variables.part(1,
                                        (part_path,part_name_9,part_format),
                                        (part_box_x_0,part_box_y_0)))
    part_name_10="V222_Gesamtfahrzeug_1430_V222 Hauptboden_stp_Koerper_3_Moved"
    part_list.append(Global_Variables.part(2,
                                        (part_path,part_name_10,part_format),
                                        (part_box_x_0,part_box_y_0)))


    return part_list


if __name__ == '__main__':

    parts=def_parts()
    #BB_HDF5_Tabelle_erstellen.HDF5_erstellen()
    #for part in parte:
    #    AA_Daten_erstellen._start(part)
    #    BB_HDF5_Tabelle_erstellen.tabellen_fuellen(part)
    CC_Evaluation_of_Data.Evaluation_of_Data()._start()