#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
import copy
from scipy.linalg import svd
from scipy.sparse.linalg import eigs
import Global_Variables as GV
from scipy.stats import rankdata as rd

class DD_Procrustes_Commandeur():

    def dataset_bsp1():
        X1=np.full((20,3), np.nan)
        X1[2]=[-1.5,-2,2.4330]
        X1[10]=[-2.0774,-3,0.8]
        X1[14]=[-2.0774,-1,0.8]
        X1[16]=[-0.3453,-2,0.8]

        X2=np.full((20,3), np.nan)
        X2[0]=[1,0,-0.5]
        X2[2]=[1,1,-0.5]
        X2[6]=[1,1,-1.5]
        X2[10]=[0,0,-0.5]
        X2[12]=[0,1,-0.5]
        X2[14]=[0,1,-1.5]
        X2[16]=[1,0,-1.5]
        X2[18]=[0,0,-1.5]

        X3=np.full((20,3), np.nan)
        X3[0]=[2.2705,  -2.5,       4.9098]
        X3[1]=[1.8197,  -1.3197,    4.1803]
        X3[2]=[3,       -0.5902,    3.7295]
        X3[3]=[4.1803,  -1.3197,    4.1803]
        X3[4]=[3.7295,  -2.5,       4.9098]
        X3[5]=[1.0902,  -1.7705,    3]
        X3[6]=[1.8197,  -1.3197,    1.8197]
        X3[7]=[3,       -0.5902,    2.2705]
        X3[8]=[1.8197,  -3.6803,    4.1803]
        X3[9]=[3,       -4.4098,    3.7295]
        X3[10]=[4.1803, -3.6803,    4.1803]
        X3[11]=[4.9098, -3.2295,    3]
        X3[12]=[4.9098, -1.7705,    3]
        X3[13]=[4.1803, -1.3197,    1.8197]
        X3[14]=[3.7295, -2.5,       1.0902]
        X3[15]=[4.1803, -3.6803,    1.8197]
        X3[16]=[1.0902, -3.2295,    3]
        X3[17]=[2.2705, -2.5,       1.0902]
        X3[18]=[3,      -4.4098,    2.2705]
        X3[19]=[1.8197, -3.6803,    1.8197]

        print("X1=")
        print(X1)
        print("X2=")
        print(X2)
        print("X3=")
        print(X3)


        return (X1,X2,X3)
    def dataset_bsp2(self):
        X1=np.full((20,3), np.nan)
        X1[0]=[2.2705,  -2.5,       4.9098]
        X1[1]=[1.8197,  -1.3197,    4.1803]
        X1[2]=[3,       -0.5902,    3.7295]
        X1[3]=[4.1803,  -1.3197,    4.1803]
        X1[4]=[3.7295,  -2.5,       4.9098]
        X1[5]=[1.0902,  -1.7705,    3]
        X1[6]=[1.8197,  -1.3197,    1.8197]
        X1[7]=[3,       -0.5902,    2.2705]
        X1[8]=[1.8197,  -3.6803,    4.1803]
        X1[9]=[3,       -4.4098,    3.7295]
        X1[10]=[4.1803, -3.6803,    4.1803]
        X1[11]=[4.9098, -3.2295,    3]
        X1[12]=[4.9098, -1.7705,    3]
        X1[13]=[4.1803, -1.3197,    1.8197]
        X1[14]=[3.7295, -2.5,       1.0902]
        X1[15]=[4.1803, -3.6803,    1.8197]
        X1[16]=[1.0902, -3.2295,    3]
        X1[17]=[2.2705, -2.5,       1.0902]
        X1[18]=[3,      -4.4098,    2.2705]
        X1[19]=[1.8197, -3.6803,    1.8197]

        X2=np.full((20,3), np.nan)
        X2[0]=[2.2705,  -2.5,       14]
        X2[1]=[1.8197,  -1.3197,    4.1803]
        X2[2]=[3,       -0.5902,    3.7295]
        X2[3]=[4.1803,  -1.3197,    4.1803]
        X2[4]=[3.7295,  -2.5,       4.9098]
        X2[5]=[1.0902,  -1.7705,    3]
        X2[6]=[1.8197,  -1.3197,    1.8197]
        X2[7]=[3,       -0.5902,    2.2705]
        X2[8]=[1.8197,  -3.6803,    4.1803]
        X2[9]=[3,       -4.4098,    3.7295]
        X2[10]=[4.1803, -3.6803,    4.1803]
        X2[11]=[4.9098, -3.2295,    3]
        X2[12]=[4.9098, -1.7705,    3]
        X2[13]=[4.1803, -1.3197,    1.8197]
        X2[14]=[3.7295, -2.5,       1.0902]
        X2[15]=[4.1803, -3.6803,    1.8197]
        X2[16]=[1.0902, -3.2295,    3]
        X2[17]=[2.2705, -2.5,       1.0902]
        X2[18]=[3,      -4.4098,    2.2705]
        X2[19]=[1.8197, -3.6803,    1.8197]


        return (X1,X2)
    def dataset_commandeur_0(self):
    
        X1=np.array([[1,3],
                     [np.nan,np.nan],
                     [4,-1],
                     [np.nan,np.nan],
                     [-3,-3]])
        X2=np.array([[-2,3],
                     [1,5],
                     [np.nan,np.nan],
                     [1,-4],
                     [-5,-4]])
        X3=np.array([[0,6],
                     [5,2],
                     [np.nan,np.nan],
                     [3,-7],
                     [-4.5,-6]])
        X4=np.array([[-3,8],
                     [3,5],
                     [6,-3],
                     [2,-7],
                     [-3.5,-7]])
        Z=np.array([[-1,5],
                     [3,4],
                     [5,-2],
                     [2,-6],
                     [-4,-5]])


        return (X1,X2,X3,X4),Z


    #! Dataprocessing
    def dataset_prepare(_rows,_data,_pos_adjustment):
        amount_data=len(_data)
        dimensions=_data[0].shape[1]
        amount_rows_plus=abs(_rows-_data[_pos_adjustment].shape[0])
        data_rows_plus=np.full((amount_rows_plus,dimensions),np.nan)
        _data[_pos_adjustment]=np.vstack((_data[_pos_adjustment],data_rows_plus))

        return _data
    def dataexport(_part_a, _part_b,_name_variante,
                     _amount_data,_evaluation_final,
                     _s_vektor_stand,_R_Matrices,
                     _maximize_by_rotation,
                     _maximize_by_skaling,
                     _konvergency):
        #! Export:
        path_file=GV.speicher_pathe["Commandeur"]
        file_name="//part_{}_vs_{}_{}.txt".format(_part_a,_part_b,
                                                      _name_variante)
        file=open(path_file+file_name,"w")

        file.write("#"*100+"\n")
        file.write("result:\n")
        file.write("-"*70+"\n")
        file.write("uj=\n")
        for d in range(_amount_data):
            file.write("part {}\n".format(d+1))

            for z in _evaluation_final[2][d]:
                file.write("\t\t{}\n".format(z))
        file.write("-"*70+"\n")
        file.write("Skalierung=\n")
        for d in range(_amount_data):
            file.write("part {}\n".format(d+1))
            file.write("\t\t{}\n".format(_s_vektor_stand[d]))            
        file.write("-"*70+"\n")
        file.write("RotationsMatrices=\n")
        for d in range(_amount_data):
            file.write("part {}\n".format(d+1))
            for j in np.round(_R_Matrices[d],4):
                file.write("\t\t{}\n".format(j))
        file.write("-"*70+"\n")
        file.write("Schwerpunkt=\n")
        for j in np.round(_evaluation_final[0],4):
            file.write("\t\t{}\n".format(j))
        file.write("-"*70+"\n")
        file.write("+"*70+"\n")
        file.write("Iterationsverlauf [Rotation|Skalierung]:\n")
        for i,j in enumerate(_maximize_by_rotation):
            file.write("{}\t\t{:20}\t{:20}\n".format(i,
                                              round(float(_amount_data)-j,
                                                    int(abs(np.log10(_konvergency)))),
                                              round(float(_amount_data)-_maximize_by_skaling[i],
                                                    int(abs(np.log10(_konvergency))))))
        file.write("+"*70+"\n\n")
        file.write("-"*70+"\n")
        file.write("AuswertungsTablen\n")
        file.write("-"*70+"\n")
        file.write("Table A:\n")
        for i,j in enumerate(_evaluation_final[4][0]):
            file.write("{}\t\t{:10}{:10}{:10}\n".format(i,
                                                  round(j,4),
                                                  round(_evaluation_final[4][1][i],4),
                                                  round(_evaluation_final[4][2][i],4)))
        file.write("SumR\t{:10}{:10}{:10}\n".format(round(sum(_evaluation_final[4][0]),4),
                                                       round(sum(_evaluation_final[4][1]),4),
                                                       round(sum(_evaluation_final[4][2]),4)))
        file.write("Sum\t\t{:10}{:10}{:10}\n".format(round(_evaluation_final[4][3],4),
                                               round(_evaluation_final[4][4],4),
                                               _amount_data))
        file.write("-"*70+"\n")
        file.write("Table B:\n")
        for i,j in enumerate(_evaluation_final[5][0]):
            file.write("{}\t\t{:10}{:10}{:10}\n".format(i,
                                                  round(j,4),
                                                  round(_evaluation_final[5][1][i],4),
                                                  round(_evaluation_final[5][2][i],4)))
        file.write("SumR\t{:10}{:10}{:10}\n".format(round(sum(_evaluation_final[5][0]),4),
                                                       round(sum(_evaluation_final[5][1]),4),
                                                       round(sum(_evaluation_final[5][2]),4)))
        file.write("Sum\t\t{:10}{:10}{:10}\n".format(round(_evaluation_final[5][3],4),
                                               round(_evaluation_final[5][4],4),
                                               _amount_data))

        file.write("-"*70+"\n")
        file.write("Table C:\n")
        for i,j in enumerate(_evaluation_final[6][0]):
            file.write("{}\t\t{:10}{:10}{:10}\n".format(i,
                                                  round(j,4),
                                                  round(_evaluation_final[6][1][i],4),
                                                  round(_evaluation_final[6][2][i],4)))
        file.write("SumR\t{:10}{:10}{:10}\n".format(round(sum(_evaluation_final[6][0]),4),
                                                       round(sum(_evaluation_final[6][1]),4),
                                                       round(sum(_evaluation_final[6][2]),4)))
        file.write("Sum\t\t{:10}{:10}{:10}\n".format(round(_evaluation_final[6][3],4),
                                               round(_evaluation_final[6][4],4),
                                               _amount_data))
        file.write("#"*100+"\n")
        file.close()
    ###################################################################
    #! Algorythm
    def Function_C_Matrices(self,_data,
                            pos_adjustment,
                            lenght_short,
                            dimension=None, points_max=None):

        if dimension==None:
            dimension=len(_data[0][0])
        if points_max==None:
            points_max=len(_data[0])
        amount_data=len(_data)

        identity_matrix=np.identity(points_max)
        #identity_matrix_s=sp.sparse.identity(points_max,format="dia")
        ## um einen transponierbaren Vektor zu erzeugen [[]]
        vektor_1=np.array([np.ones(points_max)]).T
        #vektor_1_s=sp.sparse.dok_matrix(vektor_1)
        ## Muss f?r andere data angepasst weren. 99 als Erkennung...
        M_j_list=[0]*amount_data
        C_j_list=[0]*amount_data
        #M_j_list_s=[0]*amount_data
        #C_j_list_s=[0]*amount_data
        C_j_summe=np.zeros((points_max,points_max))
        #C_j_summe_s=sp.sparse.csr_matrix((points_max,points_max))

        for d,column in enumerate(_data):
            #if pos_adjustment==None or d!=pos_adjustment:
            #    M_j_s=identity_matrix_s
            #    #einser_matrix_s=vektor_1_s.dot(vektor_1_s.transpose())
            #    #J_j_zw_0_s=einser_matrix_s.dot(M_j_s).multiply(1.0/float(points_max))
            #    J_j_zw_0_s=sp.sparse.csr_matrix(([1.0/float(points_max)]*points_max*points_max,
            #                                (np.repeat(np.arange(0,points_max),points_max),
            #                                range(0,points_max)*points_max)
            #                                ),
            #                                shape=(points_max, points_max))
            #    J_j_s=identity_matrix_s-J_j_zw_0_s

            #elif d==pos_adjustment:
            #    eintraege_dia=[1.0]*lenght_short
            #    M_j_s=sp.sparse.dia_matrix((points_max, points_max))
            #    M_j_s.setdiag(eintraege_dia)
            #    J_j_zw_0_s=sp.sparse.csr_matrix(([1.0/float(lenght_short)]*lenght_short*points_max,
            #                                (np.repeat(np.arange(0,points_max),lenght_short),
            #                                range(0,lenght_short)*points_max)
            #                                ),
            #                                shape=(points_max, points_max))
            #    J_j_s=identity_matrix_s-J_j_zw_0_s

            #test=J_j_s.toarray()

            #M_j_list_s[d]=M_j_s
            #C_j_s=M_j_s.dot(J_j_s)
            #C_j_list_s[d]=C_j_s
            #test_2=C_j_s.toarray()
            #C_j_summe_s+=C_j_s

            M_j=copy.deepcopy(identity_matrix)
        
            for i,stimulus in enumerate(column):
                if (np.isnan(stimulus).all()):
                    M_j[i,i]=0
        
            M_j_list[d]=M_j
            J_j_zw_0a=np.dot(vektor_1,vektor_1.T)
            J_j_zw_0=np.dot(J_j_zw_0a,M_j)
            J_j_zw_1=np.dot(np.dot(vektor_1.T,M_j),vektor_1)
            J_j_zw_2=J_j_zw_0/J_j_zw_1
            J_j=identity_matrix-J_j_zw_2
            C_j=np.dot(M_j,J_j)
            C_j_list[d]=C_j
            C_j_summe+=C_j

        #    print M_j
        #    print C_j
        #    print "-"*10
        #print C_j_summe

        return C_j_summe, C_j_list, M_j_list
        #return C_j_summe_s, C_j_list_s, M_j_list_s
    def Funktion_W_m05_Matrix(self,_data,_C_Matrices):
        amount_data=len(_data)
        norm_export=[0]*amount_data
        W_Matrix=np.zeros((amount_data,amount_data))
        for d,column in enumerate(_data):
            column_nan_0=np.nan_to_num(column)
            matrix_curr=column_nan_0.T.dot(_C_Matrices[d]).dot(column_nan_0)
            matrix_curr_track=np.trace(matrix_curr)
            column_norm=column/np.sqrt(matrix_curr_track)
            column_norm_nan_0=np.nan_to_num(column_norm)
            entry_w_j=1.0/np.sqrt(np.trace(column_norm_nan_0.T.dot(_C_Matrices[d]).dot(column_norm_nan_0)))
            W_Matrix[d,d]=entry_w_j
            norm_export[d]=column_norm

        return W_Matrix,norm_export
    def Convergence_Control(self,_data,_s_vektor,_C_Matrices,_R_Matrices,_C_Matrix_invers,
                             _kon_curr,_i_kon_range,_i_kon_max,_konvergency_range):
        data=np.nan_to_num(_data)
        amount_data=len(data)
        m=len(data[0][0])
        p=len(data[0])

        error=False
        loop=True
        summe_sCXR=np.zeros((p,m))
        for j in range(amount_data):
            summe_sCXR_j=_s_vektor[j]*_C_Matrices[j].dot(data[j]).dot(_R_Matrices[j])
            summe_sCXR+=summe_sCXR_j
        calculation_zw=summe_sCXR.T.dot(_C_Matrix_invers).dot(summe_sCXR)
        track_curr=np.trace(calculation_zw)
        diff_curr=abs(_kon_curr-track_curr)
        if diff_curr<=_konvergency_range:
            _i_kon_range+=1
            if _i_kon_range>=_i_kon_max:
                loop=False
        elif track_curr<_kon_curr:# and _kon_curr<=float(amount_data):
            #print "error, keine Konvergenz"
            error=True
        #print track_curr,diff_curr
        return track_curr,diff_curr,_i_kon_range,loop, error
    def evaluation(_data,_C_Matrix_invers,_C_Matrix,_C_Matrices,_M_Matrices,_R_Matrices,_s_vektor):
    
        data=np.nan_to_num(_data)

        amount_data=len(data)
        m=len(data[0][0])
        p=len(data[0])

        vektor_1=np.array([np.ones(p)]).T
        summe_sCXR=np.zeros((p,m))
        for j in range(amount_data):
            summe_sCXR_j=_s_vektor[j]*_C_Matrices[j].dot(data[j]).dot(_R_Matrices[j])
            summe_sCXR+=summe_sCXR_j

        Z=_C_Matrix_invers.dot(summe_sCXR)
        ZtCZ=Z.T.dot(_C_Matrix).dot(Z)
        K, Lambda, K_T=svd(ZtCZ)
        ZK=Z.dot(K)
    
        list_u_j=[0]*amount_data
        list_erg_j=[0]*amount_data
        #! Table 2.3
        a_pp=np.zeros((p,p))
        b_pp=np.zeros((p,p))
        ECE=0.0
        d_pp=np.zeros((p,p))

        fit_j=0.0
        #! Table 2.4
        list_sZCXR=[0]*amount_data
        list_ECE=[0]*amount_data
        list_sXCX_ZCE=[0]*amount_data
        #! Table 2.5
        f_pp=np.zeros((m,m))
        g_pp=np.zeros((m,m))

        for j in range(amount_data):
            u_j_0a=_s_vektor[j]*data[j]-Z.dot(_R_Matrices[j].T)
            u_j_0=u_j_0a.T.dot(_M_Matrices[j]).dot(vektor_1)
            u_j_1=_s_vektor[j]*vektor_1.T.dot(_M_Matrices[j]).dot(vektor_1)
            u_j=u_j_0/u_j_1
            list_u_j[j]=u_j

            erg_j_0=data[j]-vektor_1.dot(u_j.T)
            E_j=_s_vektor[j]*_M_Matrices[j].dot(erg_j_0).dot(_R_Matrices[j])
            erg_j=E_j.dot(K)
            list_erg_j[j]=erg_j

            #! Table 2.3
            a_jj_zw=_M_Matrices[j].dot(Z)
            a_pp+=a_jj_zw.dot(a_jj_zw.T)

            E_j_Z=_s_vektor[j]*data[j].dot(_R_Matrices[j])-Z
            b_jj_zw=_C_Matrices[j].dot(E_j_Z)
            b_pp+=b_jj_zw.dot(b_jj_zw.T)
            ECE+=np.trace(E_j_Z.T.dot(_C_Matrices[j]).dot(E_j_Z))

            d_jj_zw=E_j.dot(E_j.T)
            d_pp+=d_jj_zw

            fit_0aa=(_s_vektor[j]**2)
            fit_0ab=np.trace(data[j].T.dot(_C_Matrices[j]).dot(data[j]))
            fit_0a=fit_0aa*fit_0ab
            fit_0b=np.trace(Z.T.dot(_C_Matrices[j]).dot(Z))
            fit_j+=fit_0a/fit_0b

            #! Table 2.4
            list_sZCXR[j]=_s_vektor[j]*np.trace(Z.T.dot(_C_Matrices[j]).dot(data[j]).dot(_R_Matrices[j]))
            list_ECE[j]=np.trace(E_j_Z.T.dot(_C_Matrices[j]).dot(E_j_Z))
            list_sXCX_ZCE[j]=((_s_vektor[j]**2)*np.trace(data[j].T.dot(_C_Matrices[j]).dot(data[j]))-
                               np.trace(Z.T.dot(_C_Matrices[j]).dot(E_j_Z)))

            #! Table 2.5
            f_jj_zw=_s_vektor[j]*data[j].dot(_R_Matrices[j]).dot(K)-Z.dot(K)
            f_pp+=f_jj_zw.T.dot(_C_Matrices[j]).dot(f_jj_zw)
            g_pp_zw=_s_vektor[j]*_C_Matrices[j].dot(data[j]).dot(_R_Matrices[j]).dot(K)
            g_pp+=g_pp_zw.T.dot(g_pp_zw)

        #! Table 2.3
        fit_a=1.0/float(amount_data)*((1.0/float(amount_data)*np.trace(Z.T.dot(_C_Matrix).dot(Z)))**2)*fit_j
        #! Nur fuer vollstaendige datasaetze geeignet
        #nZZ=float(amount_data)*np.trace(Z.T.dot(Z))

        #! Table 2.4 und 2.5
        track_ZCZ=np.trace(ZtCZ)
        track_EtCE=sum(list_ECE)


        return (Z, ZK, list_u_j, list_erg_j,
                (a_pp.diagonal(),b_pp.diagonal(),d_pp.diagonal(),fit_a,ECE),
                (list_sZCXR,list_ECE,list_sXCX_ZCE,track_ZCZ,track_EtCE),
                (Lambda,f_pp.diagonal(),g_pp.diagonal(),track_ZCZ,track_EtCE))
    def Funktion_Orthonomal_Transformation(self,_Normalisations_WM,
                                           _C_Matrix,
                                           _C_Matrices,
                                           _M_Matrices,
                                           _C_Matrix_invers,
                                           _R_Matrices,
                                           _A_Matrices,
                                           _s_vektor,
                                           _konvergency_range):

        amount_data=len(_Normalisations_WM)
        list_A_j=copy.deepcopy(_A_Matrices)
        list_R_j=copy.deepcopy(_R_Matrices)
        m=len(_Normalisations_WM[0][0])
        p=len(_Normalisations_WM[0])

        #! nan wird als 0 berechnet:
        data=np.nan_to_num(_Normalisations_WM)

        g_r_curr,dummy_a, dummy_b, dummy_c, dummy_d=Convergence_Control(data,_s_vektor,_C_Matrices,
                                                                        list_R_j,_C_Matrix_invers,
                                                                        0.0,0.0,0.0,0.0)
        i_kon_range=0
        i_kon_max=4
        loop=True
        i_opt=0
        error_stand_max=2
        i_error=0
        while loop==True:
            i_opt+=1
            #print "Ortho {}".format(i_opt)
            for d,data_column in enumerate(data):

                Xt_C_j=data_column.T.dot(_C_Matrices[d])
                Xt_C_j_Cm=Xt_C_j.dot(_C_Matrix_invers)

                list_data=range(0,amount_data)
                del list_data[d]
                summe_sCXR=np.zeros((p,m))
                for i in list_data:
                    C_i_X_i=_C_Matrices[i].dot(data[i])
                    C_i_X_i_R_i=_s_vektor[i]*C_i_X_i.dot(list_R_j[i])
                    summe_sCXR+=C_i_X_i_R_i

                A_j=Xt_C_j_Cm.dot(summe_sCXR)
            
                P_j, Phi_j, Q_j_T=svd(A_j)
                list_R_j[d]=P_j.dot(Q_j_T)
                A_j_export=_C_Matrices[d].dot(data_column).dot(list_R_j[d])
                list_A_j[d]=A_j_export
                g_r_j, diff_curr, i_kon_range, loop, error=Convergence_Control(data,
                                                                                      _s_vektor,
                                                                                      _C_Matrices,
                                                                                      list_R_j,
                                                                                      _C_Matrix_invers,
                                                                                      g_r_curr,
                                                                                      i_kon_range,
                                                                                      i_kon_max,
                                                                                      _konvergency_range)
                if error==True:
                    list_R_j=copy.deepcopy(_R_Matrices)
                    evaluation_old=evaluation(data,_C_Matrix_invers,_C_Matrix,
                                            _C_Matrices,_M_Matrices,_R_Matrices,_s_vektor)[5][3]
                    evaluation_new=evaluation(data,_C_Matrix_invers,_C_Matrix,
                                            _C_Matrices,_M_Matrices,list_R_j,_s_vektor)[5][3]
                    if evaluation_new>evaluation_old:
                        list_R_j=copy.deepcopy(list_R_j)
                    else:
                        i_error+=1
                    list_A_j=[0]*amount_data
                    for i,R_j in enumerate(list_R_j):
                        list_A_j[i]=_C_Matrices[i].dot(data[i]).dot(R_j)
                
                    if i_error>=error_stand_max:
                        loop=False
                        _A_Matrices=copy.deepcopy(list_A_j)
                        _R_Matrices=copy.deepcopy(list_R_j)
                        break
                else:
                    _A_Matrices=copy.deepcopy(list_A_j)
                    _R_Matrices=copy.deepcopy(list_R_j)
                    g_r_curr=g_r_j

        return _R_Matrices, _A_Matrices, g_r_curr, error
    def Function_Scaling(self,_A_Matrices,_C_Matrix_invers,_W_m05_Matrix):
        amount_data=len(_A_Matrices)
        Y=np.zeros((amount_data,amount_data))
        for x in range(amount_data):
            #test=np.trace(_A_Matrices[x].T.dot(_A_Matrices[x]))
            for y in range(amount_data):
                matrix_curr=_A_Matrices[y].T.dot(_C_Matrix_invers).dot(_A_Matrices[x])
                track_curr=np.trace(matrix_curr)
                Y[y][x]=track_curr
        #! calculation obligatorisch, da W_m05=I aber der Regel nach:
        WYW=_W_m05_Matrix.dot(Y).dot(_W_m05_Matrix)
        #! Nur 1. Eigenvektor mit Scipy Sparse-Matrix Methode
        try:
            eigw, eigv = eigs(WYW,1)
            eigw_r=eigw.real
            eigv_r=eigv.real
        except:
            P_j, Phi_j, Q_j_T=svd(WYW)
            eigw_r=Phi_j[0]
            eigv_r=Q_j_T[0]
            #print "SVD"
        s=np.sqrt(amount_data)*_W_m05_Matrix.dot(eigv_r)
        return s             
    def matrix_rang_myself(self,_matrix):

        S=sp.linalg.svd(_matrix,compute_uv=False,check_finite=False)
        return sum(S>0)


    def _start(self,_part_a, _parte_b, _data_input, _category):

        print(_part_a, _parte_b)
        for ii,data in enumerate(_data_input):
            _data_0=data[0][np.lexsort(np.fliplr(data[0]).T)]
            _data_1=data[1][np.lexsort(np.fliplr(data[1]).T)]

            _data=[_data_0,_data_1]
            category=_category[ii]
            print(category)
            #data, zentrum=dataset_commandeur_0()
            #! Max(Zeilen) data bestimmen. data gleiche Anzahl an Zeilen
            pos_adjustment=None
            lenght_short=None
            data_max=15000
            if len(_data[0])>len(_data[1]):
                number_rows=len(_data[0])
                if number_rows>data_max:
                    #_data[0]= np.delete(_data[0],range(data_max,number_rows),0)
                    data_keys=range(number_rows)
                    data_selection=np.random.choice(data_keys,number_rows-data_max,False)
                    _data[0]= np.delete(_data[0],data_selection,0)
                    number_rows=data_max
                    print("Datenkuerzung part A um {} Eintraege".format(len(data_selection)))
                pos_adjustment=1
                lenght_short=len(_data[1])
                if lenght_short>data_max:
                    #_data[1]= np.delete(_data[1],range(data_max,lenght_short),0)
                    data_keys=range(lenght_short)
                    data_selection=np.random.choice(data_keys,lenght_short-data_max,False)
                    _data[1]= np.delete(_data[1],data_selection,0)
                    lenght_short=data_max
                    data=_data
                    print("Datenkuerzung part B um {} Eintraege".format(len(data_selection)))
                else:
                    data=dataset_prepare(number_rows,_data,pos_adjustment)
            elif len(_data[0])<len(_data[1]):
                number_rows=len(_data[1])
                if number_rows>data_max:
                    #_data[1]= np.delete(_data[1],range(data_max,number_rows),0)
                    data_keys=range(number_rows)
                    data_selection=np.random.choice(data_keys,number_rows-data_max,False)
                    _data[1]= np.delete(_data[1],data_selection,0)
                    number_rows=data_max
                    print("Datenkuerzung part B um {} Eintraege".format(len(data_selection)))
                pos_adjustment=0
                lenght_short=len(_data[0])
                if lenght_short>data_max:
                    #_data[0]= np.delete(_data[0],range(data_max,lenght_short),0)
                    data_keys=range(lenght_short)
                    data_selection=np.random.choice(data_keys,lenght_short-data_max,False)
                    _data[0]= np.delete(_data[0],data_selection,0)
                    lenght_short=data_max
                    data=_data
                    print("Datenkuerzung part A um {} Eintraege".format(len(data_selection)))
                else:
                    data=dataset_prepare(number_rows,_data,pos_adjustment)
            else:
                lenght_short=len(_data[0])
                if lenght_short<data_max:
                    pass
                else:
                    #_data[0]= np.delete(_data[0],range(data_max,lenght_short),0)
                    #_data[1]= np.delete(_data[1],range(data_max,lenght_short),0)
                    data_keys=range(lenght_short)
                    data_selection=np.random.choice(data_keys,lenght_short-data_max,False)
                    _data[0]= np.delete(_data[0],data_selection,0)
                    data_selection=np.random.choice(data_keys,lenght_short-data_max,False)
                    _data[1]= np.delete(_data[1],data_selection,0)
                    lenght_short=data_max
                    print("Datenkuerzung part A&B um {} Eintraege".format(len(data_selection)))
                data=_data
    
            amount_data=len(data) # Sollte immer 2 sein

            #if _flaeche_a.part==0 and _flaeche_b.part==2:
            #    print "stop"

            #! Mit und ohne Positionsangabe
            #name_varianten=("_mit_postion","_ohne_postion")
            #data_red_0=np.delete(_data[0],[0,1],1)
            #data_red_1=np.delete(_data[1],[0,1],1)
            #varianten=(data,(data_red_0,data_red_1))
            varianten=[data]
            result=[]
            #for v,v_data in enumerate(varianten):
            v_data=data
            v=0
            infinity_num=50000000 #1.79769e+50
            v_data[0][np.nan_to_num(v_data[0])>infinity_num]=infinity_num
            v_data[1][np.nan_to_num(v_data[1])>infinity_num]=infinity_num
            #rang_data_0=np.linalg.matrix_rank(np.round(np.nan_to_num(v_data[0]),4))
            #rang_data_1=np.linalg.matrix_rank(np.round(np.nan_to_num(v_data[1]),4))
            rang_data_0=matrix_rang_myself(np.round(np.nan_to_num(v_data[0]),4))
            rang_data_1=matrix_rang_myself(np.round(np.nan_to_num(v_data[1]),4))
            #print name_varianten[v]
            if rang_data_0>1 and rang_data_1>1:
                dimension=len(v_data[0][0])
                #! Vorcalculationen ohne Optimierung
                C_Matrix, C_Matrices, M_Matrices=Function_C_Matrices(v_data,
                                                                        pos_adjustment,
                                                                        lenght_short)
                #C_Matrix_invers=np.linalg.pinv(C_Matrix)
                #C_Matrix_invers=sp.linalg.pinv(C_Matrix,check_finite=False)
                C_Matrix_invers=sp.linalg.pinv2(C_Matrix,check_finite=False)
                W_m05_Matrix, Normalisations_WM=Funktion_W_m05_Matrix(v_data,C_Matrices)

                s_vektor_stand=[1.0]*amount_data
                R_Matrices=[0]*amount_data
                for i in range(amount_data):
                    R_Matrices[i]=np.identity(dimension)
                A_Matrices=[0]*amount_data

                #! Konvergenzeinstellungen
                konvergenz=1e-10
                i_kon_range=0
                i_kon_max=4

                maximisation_by_rotation=[]
                maxisation_by_scaling=[]

                #! Optimierung:
                loop=True
                i_iteration=0
                i_iteration_max=100
                wert_curr=None
                while loop==True and i_iteration<i_iteration_max:# and wert_curr!=float(amount_data):
                    i_iteration+=1

                    #! Optimierte RotationsMatrices
                    (R_Matrices, A_Matrices,
                    wert_curr, error)=Funktion_Orthonomal_Transformation(Normalisations_WM,
                                                                            C_Matrix,
                                                                            C_Matrices,
                                                                            M_Matrices,
                                                                            C_Matrix_invers,
                                                                            R_Matrices,
                                                                            A_Matrices,
                                                                            s_vektor_stand,
                                                                            konvergenz)
                    #! Abspeichern 1. Rotationsoptimierung
                    if i_iteration==1:
                        evaluation_orth=evaluation(Normalisations_WM,C_Matrix_invers,C_Matrix,
                                                    C_Matrices,M_Matrices,R_Matrices,s_vektor_stand)
                        stand_orth=(R_Matrices,s_vektor_stand)
                    maximisation_by_rotation.append(wert_curr)
                    maxisation_by_scaling.append(0)
                    loop=False

                    ##! Optimierte Skalierung
                    #s_vektor=Function_Scaling(A_Matrices,C_Matrix_invers,W_m05_Matrix)
                    #wert_i, diff_ber, i_kon_range, loop, error=Convergence_Control(Normalisations_WM,
                    #                                                                        s_vektor,
                    #                                                                        C_Matrices,
                    #                                                                        R_Matrices,
                    #                                                                        C_Matrix_invers,
                    #                                                                        wert_curr,
                    #                                                                        i_kon_range,
                    #                                                                        i_kon_max,
                    #                                                                        konvergenz)

                    #if error==False: #! error=false=kein error=newer Wert_i>older Wert_curr :)
                    #    s_vektor_stand=s_vektor
                    #    wert_curr=wert_i
                    #    maxisation_by_scaling.append(wert_curr)
                    #else:
                    #    evaluation_old=evaluation(Normalisations_WM,C_Matrix_invers,C_Matrix,
                    #                            C_Matrices,M_Matrices,R_Matrices,s_vektor_stand)[5][3]
                    #    evaluation_new=evaluation(Normalisations_WM,C_Matrix_invers,C_Matrix,
                    #                            C_Matrices,M_Matrices,R_Matrices,s_vektor)[5][3]
                    #    if evaluation_new>evaluation_old:
                    #        s_vektor_stand=s_vektor
                    #        wert_curr=wert_i
                    #        maxisation_by_scaling.append(wert_curr)
                    #    else:
                    #        maxisation_by_scaling.append(wert_curr)
                    #        loop=False

                evaluation_final=evaluation(Normalisations_WM,C_Matrix_invers,C_Matrix,
                                            C_Matrices,M_Matrices,R_Matrices,s_vektor_stand)

                dataexport(_part_a,_parte_b,category,
                                amount_data,evaluation_final,
                                s_vektor_stand,R_Matrices,
                                maximisation_by_rotation,
                                maxisation_by_scaling,
                                konvergenz)
                erg_orth=(round(sum(evaluation_orth[4][0]),4)/float(amount_data),
                            round(evaluation_orth[4][3],4)/float(amount_data),
                            round(evaluation_orth[5][3],4)/float(amount_data),
                            round(evaluation_orth[5][4],4)/float(amount_data))
                erg_sk=(round(sum(evaluation_final[4][0]),4)/float(amount_data),
                            round(evaluation_final[4][3],4)/float(amount_data),
                            round(evaluation_final[5][3],4)/float(amount_data),
                            round(evaluation_final[5][4],4)/float(amount_data))
                result.append((erg_orth,erg_sk))
            else:
                id_flaeche=None
                if rang_data_0==1:
                    id_flaeche=0
                    #print "Rang=1 Flaeche {}".format(id_flaeche)
                else:
                    id_flaeche=1
                    #print "Rang=1 Flaeche {}".format(id_flaeche)
                erg_orth=("Rang von Flaeche{}=1/0".format((_part_a, _parte_b)[id_flaeche]),
                            "Rang von Flaeche{}=1/0".format((_part_a, _parte_b)[id_flaeche]),
                            "Rang von Flaeche{}=1/0".format((_part_a, _parte_b)[id_flaeche]),
                            "Rang von Flaeche{}=1/0".format((_part_a, _parte_b)[id_flaeche]))
                erg_sk=("Rang von Flaeche{}=1/0".format((_part_a, _parte_b)[id_flaeche]),
                            "Rang von Flaeche{}=1/0".format((_part_a, _parte_b)[id_flaeche]),
                            "Rang von Flaeche{}=1/0".format((_part_a, _parte_b)[id_flaeche]),
                            "Rang von Flaeche{}=1/0".format((_part_a, _parte_b)[id_flaeche]))
                result.append((erg_orth,erg_sk))
        return result