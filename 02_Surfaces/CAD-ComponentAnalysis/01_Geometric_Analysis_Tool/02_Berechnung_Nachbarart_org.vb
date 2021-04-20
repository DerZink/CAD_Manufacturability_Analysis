
Imports NXOpen
Imports NXOpen.UF
Imports System.Math
Imports System.Data


Module Mod_Analyse_Flaechen

    '# Flächentypen bestimmen und Flächen vermessen
    '###########################################################################
    Public Sub Funk_Analyse_Flaechen(ByVal Typ_der_Randbox As String, ByRef Oberflaechen_Ausgabe As Tabelle_Oberflaechen)

        Dim Geflecht_Flaechen(1) As Integer
        Dim Kantenradius(1) As Double
        Dim Flaechentyp As Double
        Dim n As Integer = 176
        Dim obj(0) As DisplayableObject
        Dim RGB(2) As Double
        Dim Farbe As Integer
        Dim Oberflaechen = Oberflaechen_Ausgabe.DataTable_Ausgabe
        If Typ_der_Randbox <> "neutral" Then

            For l = 0 To Koerper_akt.GetFaces.Length - 1
                Flaechentyp = Oberflaechen.Rows(l).Item("Typ")
                '# Flächentyp bestimmen
                Funk_Flaechen_Typ(l, Flaechentyp, Oberflaechen)
            Next

            '# Bestimmen der Anzahlen der verschiedenen Oberflächentypen
            Dim nGrundFlaechen As Integer = Oberflaechen.Select("Oberflaechentyp = 1").Length
            Dim nRandFlaechen As Integer = Oberflaechen.Select("Oberflaechentyp = 2").Length
            Dim nUebergangsFlaechen As Integer = Oberflaechen.Select("Oberflaechentyp = 3").Length
            Dim nFeatureFlaechen As Integer = Oberflaechen.Select("Oberflaechentyp = 4").Length

            '# Falls keine Randfläche gefunden wird ist das Bauteil nicht für die Flaechenanalyse geeignet
            If nRandFlaechen = 0 Then
                MsgBox("Es wurde keine Profilflaeche erkannt. Das Bauteil ist kein extrudiertes Profil und ist damit laut Definition ungeeignet für die Flaechen-, Geflechts- und Pressanalyse!")
                Exit Sub
            End If

            '# Überprüfen, welche Randfläche für Feature-Extraktion benutzt werden soll.
            Dim Profil_ID As Integer = Funk_Erkennung_Profilflaechen(nRandFlaechen, Geflecht_Flaechen, Oberflaechen)
            If Profil_ID = 0 Then
                Txt_Datei.WriteLine("Error in process_Data.vb: Es kann keine Profilseite erkannt werden")
                MsgBox("Error in Analyse_Flaechen.vb: Es kann keine Profilseite erkannt werden")
                Exit Sub
            End If

            '# Flechtprozess-spezifische Analyse
            '# -------------------------------------------------------------------------------------------------------------------
            If Typ_der_Randbox = "lang" Or Typ_der_Randbox = "eben und lang" Then

                '# Flechtbarkeitsanalyse
                '# Wird nur durchgeführt falls eine Randflaeche vorhanden ist da sonst ein Fehler angezeigt wird
                Dim check_Parameter(2) As Double
                check_Parameter = Funk_Analyse_Geflecht(Profil_ID, Geflecht_Flaechen, Oberflaechen)

                Dim kgeflecht As Double = check_Parameter(0)
                Dim ustern As Double = check_Parameter(1)

                Txt_Datei.WriteLine("uStern: " & ustern)
                Txt_Datei.WriteLine("kGeflecht: " & kgeflecht)

                '# Biegewinkel < 180
                If check_Parameter(2) = 1 Then
                    If kgeflecht = 0 Then
                        Txt_Datei.WriteLine("Geometrie ist nicht flechtbar")
                    Else
                        Txt_Datei.WriteLine("Geometrie ist flechtbar")
                    End If

                    '# Biegewinkel >= 180
                Else
                    Txt_Datei.WriteLine("Geometrie ist nicht flechtbar")
                End If
            End If

            '# Pressprozess-spezifische Analyse
            '# -------------------------------------------------------------------------------------------------------------------
            If Typ_der_Randbox = "eben" Or Typ_der_Randbox = "eben und lang" Then

                '# Entformbarkeitsanalyse
                '# --------------------------------------------------subroutine or function---> analyze_PressMoulding.vb
                Dim EntformungsCheck As Boolean = Funk_Analyse_Pressbarkeit(Profil_ID, Oberflaechen)

                If EntformungsCheck = True Then
                    Txt_Datei.WriteLine("Geometrie ist entformbar")
                    RGB(0) = 0
                    RGB(1) = 0.8
                    RGB(2) = 0
                Else
                    Txt_Datei.WriteLine("Geometrie ist nicht entformbar")
                    RGB(0) = 0.8
                    RGB(1) = 0
                    RGB(2) = 0
                End If

            End If

            Dim Objekte(0) As DisplayableObject
            '# Change Color
            'objects(0) = CType(NXOpen.Utilities.NXObjectManager.Get(CType(OberFlaechen.Rows(profileID - 1).Item("Tag"), Tag)), Face)
            Objekte(0) = Koerper_akt
            Dim Darstellung_Modifikation As DisplayModification
            theUFSession.Disp.AskClosestColor(UFConstants.UF_DISP_rgb_model, RGB, UFConstants.UF_DISP_CCM_EUCLIDEAN_DISTANCE, Farbe)
            Darstellung_Modifikation = theSession.DisplayManager.NewDisplayModification()
            Darstellung_Modifikation.ApplyToAllFaces = False
            Darstellung_Modifikation.NewColor = Farbe
            '# Darstellung_Modifikation.Apply(objects)

        End If



    End Sub

    '# Vergleicht erkannte Randflächen anhand ihrer Flächeninhalte und Kantenanzahlen und gibt die Profilfläche zurück
    '###########################################################################################
    Private Function Funk_Erkennung_Profilflaechen(ByVal nRandFlaechen As Integer, ByRef Geflecht_Flaechen() As Integer, ByRef Oberflaechen As DataTable) As Integer

        Dim Reihe() As DataRow = Oberflaechen.Select("Oberflaechentyp = 2")
        Dim Bereich(nRandFlaechen - 1) As Double
        Dim nKanten() As Integer
        Dim GleicheFlaechen() As Integer
        Dim GesamtFlaeche(0) As Integer

        '# Speichern des Flächeninhalts in einem Array
        For i = 0 To nRandFlaechen - 1
            Bereich(i) = Reihe(i).Item("Bereich")
        Next

        '# ID's der Randflächen die mehrmals vorkommen
        GleicheFlaechen = Funk_Erkennung_IdentischeFlaechen(nRandFlaechen, Bereich, GesamtFlaeche, Oberflaechen)

        '# Wenn nur 2 Randflächen vorliegen...
        If GleicheFlaechen.Length = 1 And GleicheFlaechen(0) <> 0 Then

            'returnProfileFace = row(0).Item("ID")
            Funk_Erkennung_Profilflaechen = GleicheFlaechen(0)

            '# Übergabe der Flächen für den Flechtbarkeitsabgleich (Funktion angleCheck in Analyse_des_Geflechts):
            Geflecht_Flaechen(0) = GesamtFlaeche(0)
            Geflecht_Flaechen(1) = GesamtFlaeche(1)


            '# Wenn 4 Randflächen vorliegen...
        ElseIf GleicheFlaechen.Length = 2 Then

            ReDim nKanten(GleicheFlaechen.Length)

            For i = 0 To GleicheFlaechen.Length - 1
                nKanten(i) = Split(Oberflaechen.Rows(GleicheFlaechen(i) - 1).Item("Flaechen"), ",").Length
            Next

            If nKanten(1) > nKanten(0) Then
                Funk_Erkennung_Profilflaechen = GleicheFlaechen(1)
                '# Übergabe der Flächen für den Flechtbarkeitsabgleich (Funktion angleCheck in Analyse_des_Geflechts):
                Geflecht_Flaechen(0) = GesamtFlaeche(2)
                Geflecht_Flaechen(1) = GesamtFlaeche(3)
            ElseIf nKanten(1) < nKanten(0) Then
                Funk_Erkennung_Profilflaechen = GleicheFlaechen(0)
                '# Übergabe der Flächen für den Flechtbarkeitsabgleich (Funktion angleCheck in Analyse_des_Geflechts):
                Geflecht_Flaechen(0) = GesamtFlaeche(0)
                Geflecht_Flaechen(1) = GesamtFlaeche(1)
            ElseIf nKanten(1) = nKanten(0) Then
                '# Flächenvergleich:
                If Oberflaechen.Rows(GleicheFlaechen(0) - 1).Item("Bereich") < Oberflaechen.Rows(GleicheFlaechen(1) - 1).Item("Bereich") Then
                    Funk_Erkennung_Profilflaechen = GleicheFlaechen(0)
                    '# Übergabe der Flächen für den Flechtbarkeitsabgleich (Funktion angleCheck in Analyse_des_Geflechts):
                    Geflecht_Flaechen(0) = GesamtFlaeche(0)
                    Geflecht_Flaechen(1) = GesamtFlaeche(1)
                Else
                    Funk_Erkennung_Profilflaechen = GleicheFlaechen(1)
                    '# Übergabe der Flächen für den Flechtbarkeitsabgleich (Funktion angleCheck in Analyse_des_Geflechts):
                    Geflecht_Flaechen(0) = GesamtFlaeche(2)
                    Geflecht_Flaechen(1) = GesamtFlaeche(3)
                End If

            End If

        Else
            Txt_Datei.WriteLine("Error in process_Data.vb (returnProfileFace). Unbekannte Anzahl an Randflaechen")
        End If

    End Function

    '# Erkennt in einem Array enthaltene Flächenpaare mit gleichem Flächeninhalt.
    '###########################################################################################
    Private Function Funk_Erkennung_IdentischeFlaechen(ByVal nRandFlaechen As Integer, ByVal Bereich() As Double, ByRef GesamtFlaeche() As Integer, ByRef Oberflaechen As DataTable) As Integer()
        Dim Information(nRandFlaechen - 1, 1) As Double
        Dim Reihe() As DataRow = Oberflaechen.Select("Oberflaechentyp = 2")
        Dim Gleiche(1, 0) As Integer
        Dim k As Integer = 0
        Dim l As Integer = 0
        Dim GleicheFlaechen(0) As Integer
        Dim Flaechen_ID As Integer
        Dim Flaechen_IDs(0) As Integer
        Dim Index As Integer = 0
        ReDim GesamtFlaeche(0)


        '# Vergleich der Flächeninhalte der Randflächen
        '# Erstellen eines Arrays, der die ID's der Randflächen gleicher Größe enthält
        For i = 0 To nRandFlaechen - 1
            For j = i + 1 To nRandFlaechen - 1
                If Bereich(i) = Bereich(j) And j <> i Then
                    Flaechen_ID = Reihe(j).Item("ID")
                    ReDim Preserve GesamtFlaeche(GesamtFlaeche.Length + 1)
                    GesamtFlaeche(l) = Reihe(j).Item("ID")
                    GesamtFlaeche(l + 1) = Reihe(i).Item("ID")
                    l = l + 2
                    k = k + 1
                End If
            Next
            If k > 0 Then
                Flaechen_IDs(Index) = Flaechen_ID
                Index = Index + 1
                ReDim Preserve Flaechen_IDs(Index)
            End If
            k = 0
        Next

        If Flaechen_IDs.Length > 1 Then
            ReDim Preserve Flaechen_IDs(Flaechen_IDs.Length - 2)
            '# Übergibt die ID einer Fläche von zwei gleichen Flächen
            Funk_Erkennung_IdentischeFlaechen = Flaechen_IDs
        Else
            '# Wenn keine Randflaechen
            Funk_Erkennung_IdentischeFlaechen = {0}
        End If



    End Function

    '# SurfaceType festlegen
    '###########################################################################
    Private Sub Funk_Flaechen_Typ(ByVal l As Integer, ByVal Typ As Double, ByRef Oberflaechen As DataTable)
        Dim st As Integer = 0
        Dim check As Boolean = Funk_Kontrolle_InnereFlaechen_Zylinder(l, Oberflaechen)
        Dim WinkelBeziehung As String = Funk_WinkelBeziehungen(l, Oberflaechen)
        Dim GroessteAngrenzendeFlaeche As Boolean = Funk_AngrenzendeFlaechen_GroessenCheck(l, Oberflaechen)
        Dim Farbe As Integer = 0
        Dim RGB(2) As Double
        Dim Bereich As Double = Oberflaechen.Rows(l).Item("Bereich")

        '# Zylinderfläche
        If (Typ = 16 Or Typ = 17) And check = True Then
            st = 2
        Else
            '# G R U N D F L Ä C H E
            If l = 0 And WinkelBeziehung = "Konvex" Then
                st = 1
                '# Dunkelgrün
                RGB(0) = 0
                RGB(1) = 1
                RGB(2) = 1
            Else
                If Oberflaechen.Rows(l).Item("Bereich") > 0.7 * Oberflaechen.Rows(0).Item("Bereich") And check = False Then ' And WinkelBeziehung = "convex" Then
                    st = 1
                    '# Dunkelgrün
                    RGB(0) = 0
                    RGB(1) = 1
                    RGB(2) = 1
                    '# R A N D F L Ä C H E
                ElseIf Oberflaechen.Rows(l).Item("Bereich") <= 0.7 * Oberflaechen.Rows(0).Item("Bereich") And check = False And WinkelBeziehung = "Konvex" And GroessteAngrenzendeFlaeche = True And Typ = 22 Then
                    st = 2
                    '# Hellgrün
                    RGB(0) = 0
                    RGB(1) = 1
                    RGB(2) = 0
                    '# Ü B E R G A N G S F L Ä C H E
                ElseIf Oberflaechen.Rows(l).Item("Bereich") <= 0.7 * Oberflaechen.Rows(0).Item("Bereich") And WinkelBeziehung = "Gemischt" And GroessteAngrenzendeFlaeche = True Then
                    st = 3
                    '# Blau
                    RGB(0) = 0
                    RGB(1) = 0
                    RGB(2) = 1
                    '# F E A T U R E F L Ä C H E
                ElseIf Oberflaechen.Rows(l).Item("Bereich") <= 0.7 * Oberflaechen.Rows(0).Item("Bereich") And WinkelBeziehung = "Konkave" Then
                    st = 4
                    '# Gelb
                    RGB(0) = 1
                    RGB(1) = 1
                    RGB(2) = 0
                Else
                    st = 5
                    '# Rot
                    RGB(0) = 1
                    RGB(1) = 0
                    RGB(2) = 0
                End If
            End If
        End If

        Oberflaechen.Rows(l).Item("Oberflaechentyp") = st

        '# Farbmarkierung
        Dim obj(0) As DisplayableObject
        obj(0) = CType(NXOpen.Utilities.NXObjectManager.Get(CType(Oberflaechen.Rows(l).Item("Tag"), Tag)), Face)
        Dim Darstellung_Modifikation As DisplayModification
        theUFSession.Disp.AskClosestColor(UFConstants.UF_DISP_rgb_model, RGB, UFConstants.UF_DISP_CCM_EUCLIDEAN_DISTANCE, Farbe)
        Darstellung_Modifikation = theSession.DisplayManager.NewDisplayModification()
        Darstellung_Modifikation.ApplyToAllFaces = False
        Darstellung_Modifikation.NewColor = Farbe
        Darstellung_Modifikation.Apply(obj)

    End Sub

    '# Größenverhältnisse zu anliegenden Flächen checken
    '###########################################################################
    Private Function Funk_AngrenzendeFlaechen_GroessenCheck(ByVal l As Integer, ByRef Oberflaechen As DataTable) As Boolean
        '# Anzahl der Angrenzenden Flächen
        Dim nAngrenzendeFlaechen As Integer = Split(Oberflaechen.Rows(l).Item("Flaechen"), ",").Length
        Dim Reihen() As DataRow
        Dim id As Integer
        Dim AngrenzendeBereiche(nAngrenzendeFlaechen - 1) As Double
        Dim EigenerBereich As Double = Oberflaechen.Rows(l).Item("Bereich")
        Dim nGroessteAngrenzendeFlaechen As Integer = 0
        For i = 0 To nAngrenzendeFlaechen - 1
            '# Zeile in OberFlaechen- Tabelle mit der in "Flächen" angegebenen Fläche bestimmen
            Reihen = Oberflaechen.Select("Tag = '" & Split(Oberflaechen.Rows(l).Item("Flaechen"), ",")(i) & "'")
            If Reihen.Count > 0 Then
                '# Id der Fläche bestimmen
                id = Reihen(0).Item("ID")
            End If

            '# Zeile mit dieser ID auswählen
            Reihen = Oberflaechen.Select("ID = '" & id & "'")
            '# Normalenvektor der Vergleichsfläche bestimmen
            AngrenzendeBereiche(i) = Reihen(0).Item("Bereich")
        Next

        Funk_sortArray(AngrenzendeBereiche)

        If AngrenzendeBereiche.Length = 1 Then
            If AngrenzendeBereiche(0) > EigenerBereich Then
                Funk_AngrenzendeFlaechen_GroessenCheck = True
            Else
                Funk_AngrenzendeFlaechen_GroessenCheck = False
            End If

        Else
            If AngrenzendeBereiche(0) > EigenerBereich And AngrenzendeBereiche(1) > EigenerBereich Then
                Funk_AngrenzendeFlaechen_GroessenCheck = True
            Else
                Funk_AngrenzendeFlaechen_GroessenCheck = False
            End If
        End If




    End Function

    '# Selectionsort Sortierungsalgorithmus
    Private Sub Funk_sortArray(ByRef Array() As Double)

        Dim Bester_Wert As Double
        Dim Beste_j As Integer
        For i = 0 To Array.Length - 2
            Bester_Wert = Array(i)
            Beste_j = i
            For j = i + 1 To Array.Length - 1
                If Array(j) > Bester_Wert Then
                    Bester_Wert = Array(j)
                    Beste_j = j
                End If
            Next j
            Array(Beste_j) = Array(i)
            Array(i) = Bester_Wert
        Next i

    End Sub

    '# Gibt die WinkelBeziehungen zu angrenzenden Flächen zurück
    '###########################################################################
    Private Function Funk_WinkelBeziehungen(ByVal l As Integer, ByRef Oberflaechen As DataTable) As String
        Dim Reihen() As DataRow
        Dim id As Integer
        Dim NormalenVektor As Snap.Vector = Nothing
        Dim KomponentenVektor As Snap.Vector = Nothing
        Dim HilfsVektor As Snap.Vector = Nothing
        Dim HilfsWinkel As Double
        Dim HilfsPunkt As Point3d = Nothing
        Dim NormalPosition As Snap.Position = Nothing
        Dim Winkel As Double
        Dim StartPunkt, EndPunkt As Point3d
        Dim Konkav As Boolean = False
        Dim Konvex As Boolean = False
        Dim HilfsKurve As Curve
        Dim nUeberschneidungen As Integer
        Dim Daten() As Double = Nothing
        Dim ZuLoeschendeObjekte() As NXObject
        Dim Grund_Tag As Tag = Oberflaechen.Rows(l).Item("Tag")
        Dim Grund_NXID = Funk_NX_ID_Auslesen(Grund_Tag)
        Dim Objekt_Tag As Tag
        Dim Objekt_NXID As Integer

        '# Normalenvektor der Aktuellen Fläche
        NormalenVektor = New Snap.Vector(Oberflaechen.Rows(l).Item("vX"), Oberflaechen.Rows(l).Item("vY"), Oberflaechen.Rows(l).Item("vZ"))
        NormalPosition = New Snap.Position(Oberflaechen.Rows(l).Item("vPunkt1"), Oberflaechen.Rows(l).Item("vPunkt2"), Oberflaechen.Rows(l).Item("vPunkt3"))
        Try
            ' ---- Code that throws exception will go here

            For i = 0 To Split(Oberflaechen.Rows(l).Item("Flaechen"), ",").Length - 1
                ReDim Preserve ZuLoeschendeObjekte(i)

                '#  Zeile in OberFlaechen- Tabelle mit der in "Faces" angegebenen Fläche bestimmen
                Reihen = Oberflaechen.Select("Tag = '" & Split(Oberflaechen.Rows(l).Item("Flaechen"), ",")(i) & "'")
                If Reihen.Count > 0 Then
                    '#  Id der Fläche bestimmen
                    id = Reihen(0).Item("ID")
                End If
                Objekt_Tag = Reihen(0).Item("Tag")
                Objekt_NXID = Funk_NX_ID_Auslesen(Objekt_Tag)

                '# Zeile mit dieser ID auswählen
                Reihen = Oberflaechen.Select("ID = '" & id & "'")
                '# Normalenvektor der Vergleichsfläche bestimmen
                KomponentenVektor = New Snap.Vector(Reihen(0).Item("vX"), Reihen(0).Item("vY"), Reihen(0).Item("vZ"))
                '# Hilfsvektor vom Stützpunkt der Normalenvektoren der Fläche zur Vergleichsfläche bestimmen
                HilfsVektor = New Snap.Vector(Reihen(0).Item("vPunkt1") - Oberflaechen.Rows(l).Item("vPunkt1"), Reihen(0).Item("vPunkt2") - Oberflaechen.Rows(l).Item("vPunkt2"), Reihen(0).Item("vPunkt3") - Oberflaechen.Rows(l).Item("vPunkt3"))

                '# Den selben Vektor als Curve erstellen
                StartPunkt = New Point3d(Oberflaechen.Rows(l).Item("vPunkt1"), Oberflaechen.Rows(l).Item("vPunkt2"), Oberflaechen.Rows(l).Item("vPunkt3"))
                EndPunkt = New Point3d(Reihen(0).Item("vPunkt1"), Reihen(0).Item("vPunkt2"), Reihen(0).Item("vPunkt3"))

                HilfsKurve = theSession.Parts.Display.Curves.CreateInfiniteLine(StartPunkt, EndPunkt)

                '# Überprüfen, ob der Hilfsvektor die Vergleichsfläche schneidet
                theUFSession.Modl.IntersectCurveToFace(HilfsKurve.Tag, Reihen(0).Item("Tag"), nUeberschneidungen, Daten)
                '# Hilfswinkel zwischen Normalenvektor und Hilfsvektor bestimmen
                HilfsWinkel = Snap.Vector.Angle(NormalenVektor, HilfsVektor)

                'ZuLoeschendeObjekte(i) = HilfsKurve
                ''# NormalVector zur löschen-Liste hinzufügen
                'Dim nErrs1 As Integer
                'nErrs1 = theSession.UpdateManager.AddToDeleteList(ZuLoeschendeObjekte)

                '# Sonderfall: Zylinderförmige Flächen. Nicht fertig!
                '# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                Dim Test As Integer = Reihen(0).Item("ID") - 1
                If Reihen(0).Item("Typ") = 19 Then
                    Konvex = True
                    Winkel = Snap.Vector.Angle(NormalenVektor, KomponentenVektor) + 180.1
                    '# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                Else
                    If HilfsWinkel >= 90 Then '# Konvex
                        Winkel = Snap.Vector.Angle(NormalenVektor, KomponentenVektor) + 180
                    ElseIf HilfsWinkel < 90 Then '# Konkav
                        Winkel = Snap.Vector.Angle(NormalenVektor, KomponentenVektor)
                        '# Sonderfall von nicht voll ausgefüllten Flächen (z.B. Ringflächen) ausschließen
                        If nUeberschneidungen = 0 Then '# Konvex
                            Winkel = Snap.Vector.Angle(NormalenVektor, KomponentenVektor) + 180
                        End If
                    End If

                End If

                ''# Sonderfall: Zylinderförmige Flächen
                'Dim test As Integer = rows(0).Item("ID") - 1
                'If Oberflaechen.Rows(l).Item("Type") = 22 And checkInnereFlaechen(Reihen(0).Item("ID") - 1) = False And Reihen(0).Item("Type") = (16 Or 17 Or 19) Then
                '    Konvex = True
                '    Winkel = Snap.Vector.Angle(NormalenVektor, KomponentenVektor) + 180
                'ElseIf OberFlaechen.Rows(l).Item("Type") = 22 And checkInnereFlaechen(Reihen(0).Item("ID") - 1) = True And Reihen Then (0).Item("Typ") = (16 Or 17 Or 19) Then
                '    Konkav = True
                '    Winkel = Snap.Vector.Angle(NormalenVektor, KomponentenVektor)
                'End If

                If Winkel > 180 Then
                    Konvex = True
                ElseIf Winkel <= 180 Then
                    Konkav = True
                End If

            Next

            If Konkav = True And Konvex = True Then
                Funk_WinkelBeziehungen = "Gemischt"
            ElseIf Konkav = True And Konvex = False Then
                Funk_WinkelBeziehungen = "Konkav"
            ElseIf Konkav = False And Konvex = True Then
                Funk_WinkelBeziehungen = "Konvex"
            Else
                Funk_WinkelBeziehungen = "ERROR"
            End If
        Catch ex As NXException
            Dim Ausgabe As String = "Grundfläche:" + vbTab + l.ToString + _
                " NXID:" + vbTab + Grund_NXID.ToString + " TAG:" + vbTab + Grund_Tag.ToString + vbTab + _
                "Objektfläche:" + vbTab + id.ToString + _
                " NXID:" + vbTab + Objekt_NXID.ToString + " TAG:" + vbTab + Objekt_Tag.ToString
            Dim Daten_string As String = "StartPunkt:" + vbTab + StartPunkt.ToString + " EndPunkt:" + vbTab + EndPunkt.ToString + _
                " Vektor:" + vbTab + HilfsVektor.ToString
            theSession.LogFile.WriteLine(Ausgabe)
            theSession.LogFile.Write(Daten_string)
            Funk_WinkelBeziehungen = "ERROR"
        End Try

    End Function

    '# Überpüft, ob Zylinder- oder Konusflächen innen oder außen liegen
    '###########################################################################
    Private Function Funk_Kontrolle_InnereFlaechen_Zylinder(ByVal l As Integer, ByRef Oberflaechen As DataTable) As Boolean

        Dim Rotationsachse, normalVector As Curve
        Dim StartPunkt, endPoint As Point3d
        Dim Punkt(0 To 2) As Double
        Dim nUeberschneidungen As Integer
        Dim Daten() As Double = Nothing
        Dim dx, dy, dz As Double
        Dim Bereich As Double = 0
        Dim Winkel As Double = 0
        Dim ZuLoeschendeObjekte() As NXObject
        ReDim Preserve ZuLoeschendeObjekte(l)


        '# Wird nur durchgeführt, wenn betreffende Fläche einen Zylinder, Konus oder Torus darstellt
        If Oberflaechen.Rows(l).Item("Typ") = 16 Or Oberflaechen.Rows(l).Item("Typ") = 17 Then

            Bereich = Oberflaechen.Rows(l).Item("Bereich") '# Read Area of a Surface

            StartPunkt = New Point3d(Oberflaechen.Rows(l).Item("Punkt1"), Oberflaechen.Rows(l).Item("Punkt2"), Oberflaechen.Rows(l).Item("Punkt3"))
            endPoint = New Point3d(Oberflaechen.Rows(l).Item("Punkt1") + Oberflaechen.Rows(l).Item("X"), Oberflaechen.Rows(l).Item("Punkt2") + Oberflaechen.Rows(l).Item("Y"), Oberflaechen.Rows(l).Item("Punkt3") + Oberflaechen.Rows(l).Item("Z"))
            Rotationsachse = theSession.Parts.Display.Curves.CreateInfiniteLine(StartPunkt, endPoint) '# Function to create a infinet line through 2 points

            StartPunkt = New Point3d(Oberflaechen.Rows(l).Item("vPunkt1"), Oberflaechen.Rows(l).Item("vPunkt2"), Oberflaechen.Rows(l).Item("vPunkt3"))

            '# dx, dy, dz = Schrittweite in jeweilige Richtung. Benutzt Normalenrichtung mit 10*Radius multipliziert.
            dx = Oberflaechen.Rows(l).Item("vX") * 10 * Oberflaechen.Rows(l).Item("Radius")
            dy = Oberflaechen.Rows(l).Item("vY") * 10 * Oberflaechen.Rows(l).Item("Radius")
            dz = Oberflaechen.Rows(l).Item("vZ") * 10 * Oberflaechen.Rows(l).Item("Radius")
            'EndPoint = StartPoint + Schrittweite
            endPoint = New Point3d(Oberflaechen.Rows(l).Item("vPunkt1") + dx, Oberflaechen.Rows(l).Item("vPunkt2") + dy, Oberflaechen.Rows(l).Item("vPunkt3") + dz)
            normalVector = theSession.Parts.Display.Curves.CreateLine(StartPunkt, endPoint)

            theUFSession.Modl.IntersectCurveToCurve(Rotationsachse.Tag, normalVector.Tag, nUeberschneidungen, Daten)
            ZuLoeschendeObjekte(l) = normalVector

            '# NormalVector zur löschen-Liste hinzufügen
            Dim nErrs1 As Integer
            nErrs1 = theSession.UpdateManager.AddToDeleteList(ZuLoeschendeObjekte)

            If nUeberschneidungen > 0 Then
                Funk_Kontrolle_InnereFlaechen_Zylinder = True
                Txt_Datei.WriteLine(Oberflaechen.Rows(l).Item("Tag").ToString & " ist Innenflaeche")
            Else
                Funk_Kontrolle_InnereFlaechen_Zylinder = False
                Txt_Datei.WriteLine(Oberflaechen.Rows(l).Item("Tag").ToString & " ist Außenflaeche")
            End If

        Else
            Funk_Kontrolle_InnereFlaechen_Zylinder = False
        End If

    End Function

End Module
