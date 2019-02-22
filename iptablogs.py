#!/usr/bin/python3.7
# -*-coding:Utf-8 -*

from tkinter import *
from tkinter import ttk
from re import search
from os import getuid

# dico_colonnes is a dictionary containing for each "variable-style name", the corresponding "full name". It is used to
# display column names but also to browse attributes of the lines :

dico_colonnes = {
    "numero_ligne": "N° ligne",
    "chaine": "Chaine",
    "date": "Date",
    "heure": "Heure",
    "timestamp": "Timestamp",
    "interface_in": "Interface entrée",
    "interface_out": "Interface sortie",
    "adresse_mac": "MAC",
    "ip_source": "IP source",
    "ip_destination": "IP destination",
    "longueur_trame": "Longueur trame",
    "type_service": "TOS",
    "priorite_tos": "PREC",
    "time_to_live": "TTL",
    "id_paquet": "ID",
    "flag_fragment": "Frag",
    "protocole": "Protocole",
    "port_source": "Port source",
    "port_destination": "Port destination",
    "icmp_type": "Type ICMP",
    "icmp_code": "Code ICMP",
    "icmp_id": "ID ICMP",
    "icmp_n_sequence": "N° seq ICMP",
    "longueur_datagramme": "Longueur datagramme",
    "fenetre_tcp": "Taille fenêtre TCP",
    "bits_reserves": "Bits réservés",
    "paquet_urgent": "Paquet urgent",
    "tcp_flag": "Flag TCP"
}


def verif_sudo():
    if getuid() != 0:
        print("Ce programme nécessite d'être exécuté avec les droits root.")
    else:
        interface = Interface()
        interface.fenetre.mainloop()


def appeler_fenetre_erreur(err, msg="Erreur inconnue"):
    """This function is called when an error is raised.

    It creates a simple error window which takes as arguments the raised error and an optional message.

    """
    fenetre_erreur = Toplevel()
    fenetre_erreur.title("Erreur")
    label_erreur = Label(fenetre_erreur, text="{}\n{}".format(msg, err))
    label_erreur.pack()
    fenetre_erreur.mainloop()


def appeler_fenetre_stdout(msg_stdout):
    """This function is called when we want to display messages returned by the standard output.

    It creates a simple window which takes as argument the standard output.

    """
    fenetre_stdout = Toplevel()
    fenetre_stdout.title("stdout")
    label_stdout = Label(fenetre_stdout, text=msg_stdout)
    label_stdout.pack()
    fenetre_stdout.mainloop()


class Interface(object):
    try:
        def __init__(self):
            # This list will hold the lines read from the log file. Because it's going to used in a method of this
            # class and also because we don't want to use a global variable, it's registered here as an attribute of the
            # Interface class object :
            self.liste_lignes_log_initiale = []

            # Instancing the window :
            self.fenetre = Tk()
            self.fenetre.title("iptablogs")
            self.fenetre.geometry("1280x800")

            # Instancing the table :
            self.tableau = ttk.Treeview(self.fenetre, height=23, selectmode="browse")

            # Hiding the first column (it's a treeview control, but we don't use it as is) :
            self.tableau["show"] = "headings"

            # Defining columns we want to display :
            self.tableau["columns"] = dico_colonnes.keys()

            # Setting up the columns names :
            i = 0
            for cle_colonne_tab, valeur_colonne_tab in dico_colonnes.items():
                self.tableau.column(i, width=120, minwidth=40, stretch=0)
                self.tableau.heading(i, text=valeur_colonne_tab, anchor="w")
                i += 1

            # Scrollbars to adjust the table view :
            self.defil_hori = ttk.Scrollbar(self.fenetre, orient="horizontal", command=self.tableau.xview)
            self.defil_hori.place(x=1, y=485, height=20, width=1278)
            self.defil_verti = ttk.Scrollbar(self.fenetre, orient="vertical", command=self.tableau.yview)
            self.defil_verti.place(x=1260, y=0, height=485, width=20)
            self.tableau.configure(xscrollcommand=self.defil_hori.set)
            self.tableau.configure(yscrollcommand=self.defil_verti.set)
            self.tableau.pack(side=TOP, fill=X)

            # Second part of the interface :
            # Frame containing the sorting/filtering options :
            self.trame_options = ttk.Frame(self.fenetre, borderwidth=1, relief="groove")
            self.trame_options.place(height=295, width=1278, x=1, y=505)

            # Options to select the columns to display :
            self.label_colonnes_a_afficher = ttk.Label(self.trame_options, text="Colonnes à afficher :")
            self.label_colonnes_a_afficher.place(relx=0.0001, rely=0.001)
            self.liste_colonnes_a_afficher = Listbox(self.trame_options, width=18, height=13, selectmode="extended")
            self.liste_colonnes_a_afficher.place(relx=0.0001, rely=0.09)
            for valeur_colonne_a_afficher in dico_colonnes.values():
                self.liste_colonnes_a_afficher.insert("end", valeur_colonne_a_afficher)
            self.bouton_filtre_colonnes_a_afficher = Button(self.trame_options, text="Appliquer",
                                                            command=self.filtrer_colonnes)
            self.bouton_filtre_colonnes_a_afficher.place(relx=0.0008, rely=0.85)

            # Options to limit the number of lines to be displayed :
            self.label_nb_lignes_a_afficher = ttk.Label(self.trame_options, text="Afficher :")
            self.label_nb_lignes_a_afficher.place(relx=0.12, rely=0.001)
            self.label_nb_lignes_a_afficher2 = ttk.Label(self.trame_options, text="lignes.")
            self.label_nb_lignes_a_afficher2.place(relx=0.17, rely=0.09)
            self.inpbox_nb_lignes_a_afficher = ttk.Entry(self.trame_options, width=7)
            self.inpbox_nb_lignes_a_afficher.place(relx=0.12, rely=0.09)
            self.checkbox_dernier = IntVar()
            self.checkbox_dernieres_nb_lignes_a_afficher = ttk.Checkbutton(self.trame_options,
                                                                           text="Dernières lignes ?",
                                                                           variable=self.checkbox_dernier)
            self.checkbox_dernieres_nb_lignes_a_afficher.place(relx=0.12, rely=0.2)

            # Sorting options :
            self.label_tri = ttk.Label(self.trame_options, text="Trier par :")
            self.label_tri.place(relx=0.12, rely=0.43)
            self.combobox_tri_valeur_selectionnee = StringVar()
            self.liste_attributs_tri = [x for x in list(dico_colonnes.values()) if x != "Date"]
            self.combobox_tri = ttk.Combobox(self.trame_options, values=self.liste_attributs_tri, state="readonly",
                                             textvariable=self.combobox_tri_valeur_selectionnee, width=20)
            self.combobox_tri.current(0)
            self.combobox_tri.place(relx=0.12, rely=0.5)
            self.checkbox_var_tri = IntVar()
            self.checkbox_inverser_tri = ttk.Checkbutton(self.trame_options, text="Inverser le tri",
                                                         variable=self.checkbox_var_tri)
            self.checkbox_inverser_tri.place(relx=0.12, rely=0.6)
            self.bouton_tri = Button(self.trame_options, text="Filtrer et trier", command=self.remplir_tableau)
            self.bouton_tri.place(relx=0.15, rely=0.85)

            # Button to launch the first read of the log and display the list.
            self.bouton_initialiser = Button(self.trame_options, text="Initialiser", command=self.initialiser)
            self.bouton_initialiser.place(relx=0.08, rely=0.85)

            # Options to filter the list :
            self.label_filtres = ttk.Label(self.trame_options, text="Filtres :")
            self.label_filtres.place(relx=0.27, rely=0)
            self.trame_filtres = ttk.Frame(self.trame_options, borderwidth=1, relief="groove")
            self.trame_filtres.place(height=240, width=510, relx=0.27, rely=0.07)
            self.label_filtre_chaine = ttk.Label(self.trame_filtres, text="Chaine(s):")
            self.label_filtre_chaine.place(relx=0.001, rely=0.005)
            self.inpbox_filtre_chaine = ttk.Entry(self.trame_filtres, width=48, name="chaine")
            self.inpbox_filtre_chaine.place(relx=0.23, rely=0.005)
            self.label_filtre_date = ttk.Label(self.trame_filtres, text="Date(s):")
            self.label_filtre_date.place(relx=0, rely=0.1)
            self.inpbox_filtre_date = ttk.Entry(self.trame_filtres, width=48, name="date")
            self.inpbox_filtre_date.place(relx=0.23, rely=0.1)
            self.label_filtre_interface_in = ttk.Label(self.trame_filtres, text="Interface(s) IN:")
            self.label_filtre_interface_in.place(relx=0, rely=0.2)
            self.inpbox_filtre_interface_in = ttk.Entry(self.trame_filtres, width=48, name="interface_in")
            self.inpbox_filtre_interface_in.place(relx=0.23, rely=0.2)
            self.label_filtre_interface_out = ttk.Label(self.trame_filtres, text="Interface(s) OUT:")
            self.label_filtre_interface_out.place(relx=0, rely=0.3)
            self.inpbox_filtre_interface_out = ttk.Entry(self.trame_filtres, width=48, name="interface_out")
            self.inpbox_filtre_interface_out.place(relx=0.23, rely=0.3)
            self.label_filtre_adresse_mac = ttk.Label(self.trame_filtres, text="Adresse(s) MAC:")
            self.label_filtre_adresse_mac.place(relx=0, rely=0.4)
            self.inpbox_filtre_adresse_mac = ttk.Entry(self.trame_filtres, width=48, name="adresse_mac")
            self.inpbox_filtre_adresse_mac.place(relx=0.23, rely=0.4)
            self.label_filtre_ip_source = ttk.Label(self.trame_filtres, text="IP(s) source:")
            self.label_filtre_ip_source.place(relx=0, rely=0.5)
            self.inpbox_filtre_ip_source = ttk.Entry(self.trame_filtres, width=48, name="ip_source")
            self.inpbox_filtre_ip_source.place(relx=0.23, rely=0.5)
            self.label_filtre_ip_destination = ttk.Label(self.trame_filtres, text="IP(s) destination:")
            self.label_filtre_ip_destination.place(relx=0, rely=0.6)
            self.inpbox_filtre_ip_destination = ttk.Entry(self.trame_filtres, width=48, name="ip_destination")
            self.inpbox_filtre_ip_destination.place(relx=0.23, rely=0.6)
            self.label_filtre_protocole = ttk.Label(self.trame_filtres, text="Protocole(s):")
            self.label_filtre_protocole.place(relx=0, rely=0.7)
            self.inpbox_filtre_protocole = ttk.Entry(self.trame_filtres, width=48, name="protocole")
            self.inpbox_filtre_protocole.place(relx=0.23, rely=0.7)
            self.label_filtre_port_source = ttk.Label(self.trame_filtres, text="Port(s) source:")
            self.label_filtre_port_source.place(relx=0, rely=0.8)
            self.inpbox_filtre_port_source = ttk.Entry(self.trame_filtres, width=48, name="port_source")
            self.inpbox_filtre_port_source.place(relx=0.23, rely=0.8)
            self.label_filtre_port_destination = ttk.Label(self.trame_filtres, text="Port(s) destination:")
            self.label_filtre_port_destination.place(relx=0, rely=0.9)
            self.inpbox_filtre_port_destination = ttk.Entry(self.trame_filtres, width=48, name="port_destination")
            self.inpbox_filtre_port_destination.place(relx=0.23, rely=0.9)

            # Controls of the "experimental" functions :
            self.label_actions_experimentales = ttk.Label(self.trame_options,
                                                          text="EXPERIMENTAL : (LIRE LE README !!!)")
            self.label_actions_experimentales.place(relx=0.68, rely=0)
            self.trame_actions_experimentales = ttk.Frame(self.trame_options, borderwidth=1, relief="groove")
            self.trame_actions_experimentales.place(height=240, width=400, relx=0.68, rely=0.07)
            self.bouton_effacer_log = Button(self.trame_actions_experimentales, text="Effacer le fichier de logs",
                                             command=self.initialiser)
            self.bouton_effacer_log.place(relx=0.08, rely=0.1)
            self.bouton_rediriger_logs = Button(self.trame_actions_experimentales,
                                                text="Rediriger les logs dans /var/logs/iptables.logs",
                                                command=self.initialiser)

            self.bouton_rediriger_logs.place(relx=0.08, rely=0.4)
            self.bouton_ajouter_regles_iptables = Button(self.trame_actions_experimentales,
                                                         text="Ajouter les règles de logs iptables",
                                                         command=appeler_fenetre_erreur)
            self.bouton_ajouter_regles_iptables.place(relx=0.08, rely=0.7)
            self.dico_filtre = None

        class Lignelog:
            """Classe representing a line in the logs."""

            def __init__(self, ligne_a_decouper, n_ligne):
                """Initialization of an object Lignelog.

                It takes as arguments the line itself (str) and the line number (int).
                It makes use of regular expressions to extract the data we're looking for in each string.

             """
                numero_ligne = n_ligne
                try:
                    date = search("^([A-Z][a-z]+\\s((\\s\\d)|(\\d{2})))(?= )", ligne_a_decouper).groups()[0]
                except (AttributeError, IndexError):
                    date = ""
                try:
                    chaine = search("(?<= \\[netfilter-)(OUTPUT|INPUT|FORWARD)(?=\\] )", ligne_a_decouper).groups()[0]
                except (AttributeError, IndexError):
                    chaine = ""
                try:
                    heure = search("(?<= )(\\d{2}:\\d{2}:\\d{2})(?= )", ligne_a_decouper).groups()[0]
                except (AttributeError, IndexError):
                    heure = ""
                try:
                    timestamp = search("(?<= )(\\[\\s*\\d*\\.\\d*\\])(?= )", ligne_a_decouper).groups()[0]
                except (AttributeError, IndexError):
                    timestamp = ""
                try:
                    interface_in = search("(?<= IN=)(\\S*)(?= )", ligne_a_decouper).groups()[0]
                except (AttributeError, IndexError):
                    interface_in = ""
                try:
                    interface_out = search("(?<= OUT=)(\\S*)(?= )", ligne_a_decouper).groups()[0]
                except (AttributeError, IndexError):
                    interface_out = ""
                try:
                    adresse_mac = search("(?<= MAC=)((([a-z]|[0-9]){0,2}:){5,13}([a-z]|[0-9]){0,2})(?= )",
                                         ligne_a_decouper).groups()[0]
                except (AttributeError, IndexError):
                    adresse_mac = ""
                try:
                    ip_source = search("(?<= SRC=)((([0-9]{0,3}.){4}([0-9]{0,3}))?)(?= )", ligne_a_decouper).groups()[0]
                except (AttributeError, IndexError):
                    ip_source = ""
                try:
                    ip_destination = search("(?<= DST=)((([0-9]{0,3}.){4}([0-9]{0,3}))?)(?= )",
                                            ligne_a_decouper).groups()[0]
                except (AttributeError, IndexError):
                    ip_destination = ""
                try:
                    longueur_trame = int(search("(?<= LEN=)(\\d*)(?= )", ligne_a_decouper).groups()[0])
                except (AttributeError, IndexError):
                    longueur_trame = ""
                try:
                    type_service = search("(?<= TOS=)(\\S*)(?= )", ligne_a_decouper).groups()[0]
                except (AttributeError, IndexError):
                    type_service = ""
                try:
                    priorite_tos = search("(?<= PREC=)(\\S*)(?= )", ligne_a_decouper).groups()[0]
                except (AttributeError, IndexError):
                    priorite_tos = ""
                try:
                    time_to_live = int(search("(?<= TTL=)(\\d*)(?= )", ligne_a_decouper).groups()[0])
                except (AttributeError, IndexError):
                    time_to_live = ""
                try:
                    id_paquet = int(search("(?<= ID=)(\\d*)(?= )", ligne_a_decouper).groups()[0])
                except (AttributeError, IndexError):
                    id_paquet = ""
                try:
                    flag_fragment = search("(?<= )(DF|CE|MF)(?= )", ligne_a_decouper).groups()[0]
                except (AttributeError, IndexError):
                    flag_fragment = ""
                try:
                    protocole = search("(?<= PROTO=)(\\S*)(?= )", ligne_a_decouper).groups()[0]
                except (AttributeError, IndexError):
                    protocole = ""
                try:
                    port_source = int(search("(?<= SPT=)(\\d*)(?= )", ligne_a_decouper).groups()[0])
                except (AttributeError, IndexError):
                    port_source = int()
                try:
                    port_destination = int(search("(?<= DPT=)(\\d*)(?= )", ligne_a_decouper).groups()[0])
                except (AttributeError, IndexError):
                    port_destination = int()
                try:
                    icmp_type = int(search("(?<= TYPE=)(\\d{0,2})(?= )", ligne_a_decouper).groups()[0])
                except (AttributeError, IndexError):
                    icmp_type = int()
                try:
                    icmp_code = int(search("(?<= CODE=)(\\d{0,2})(?= )", ligne_a_decouper).groups()[0])
                except (AttributeError, IndexError):
                    icmp_code = int()
                try:
                    icmp_id = int(search("(?: PROTO=ICMP.*)(?<= ID=)(\\d*)(?= )", ligne_a_decouper).groups()[0])
                except (AttributeError, IndexError):
                    icmp_id = int()
                try:
                    icmp_n_sequence = int(search("(?<= SEQ=)(\\d*)(?= )", ligne_a_decouper).groups()[0])
                except (AttributeError, IndexError):
                    icmp_n_sequence = int()
                try:
                    longueur_datagramme = int(search("(?: PROTO=UDP.*)(?<= LEN=)(\\d*)(?= )",
                                                     ligne_a_decouper).groups()[0])
                except (AttributeError, IndexError):
                    longueur_datagramme = int()
                try:
                    fenetre_tcp = int(search("(?<= WINDOW=)(\\d*)(?= )", ligne_a_decouper).groups()[0])
                except (AttributeError, IndexError):
                    fenetre_tcp = int()
                try:
                    bits_reserves = search("(?<= RES=)(\\S*)(?= )", ligne_a_decouper).groups()[0]
                except (AttributeError, IndexError):
                    bits_reserves = ""
                try:
                    paquet_urgent = search("(?<= URGP=)[0|1](?= )", ligne_a_decouper).groups()[0]
                except (AttributeError, IndexError):
                    paquet_urgent = ""
                try:
                    tcp_flag = search("(?<= )(((ACK).?|(PSH).?|(FIN).?|(RST).?|(SYN).?)+?)(?= )",
                                      ligne_a_decouper).groups()[0]
                except (AttributeError, IndexError):
                    tcp_flag = ""

                # Then we assign the values to the Lignelog object attributes.
                # It makes use of dico_colonnes keys to browse the local variables and to name the object attributes :
                for cle_attribut in dico_colonnes.keys():
                    valeur = locals()[cle_attribut]
                    setattr(self, cle_attribut, valeur)

        def init_dico_filtres(self):
            """This function initializes of the variable dico_filtre.

            It's a dictionary whose keys correspond to the table columns, that's why it uses dico_colonnes.keys().
            Each value is a list used to filter the lines that will be displayed.

            """
            dico_filtre_tmp = {}
            for index_dico in dico_colonnes.keys():
                dico_filtre_tmp[index_dico] = []
            for index_trame in self.trame_filtres.winfo_children():
                valeurs = None
                if isinstance(index_trame, ttk.Entry) and len(index_trame.get()) > 0:
                    nom_attribut = index_trame.winfo_name()
                    if nom_attribut == ("port_source" or "port_destination"):
                        try:
                            valeurs = [int(nombre) for nombre in ((index_trame.get()).split(", "))]
                        except ValueError as erreur_valeur:
                            appeler_fenetre_erreur(erreur_valeur,
                                                   "Le port source ou destination doivent être des valeurs numériques")
                    else:
                        valeurs = (index_trame.get()).split(", ")
                    if valeurs is not None:
                        dico_filtre_tmp[nom_attribut].extend(valeurs)
            return dico_filtre_tmp

        def initialiser(self):
            """This function reads the log file then fills the table.

            It calls the functions lire_fichier_log() and remplir_tableau(). This is necessary if we don't want to have
            to read the log file again each time we want to filter or sort the results.

            """
            self.liste_lignes_log_initiale = self.lire_fichier_log()
            self.remplir_tableau()

        def filtrer_colonnes(self):
            """The purpose of this function is to narrow down the columns that are displayed."""
            self.tableau["displaycolumns"] = self.liste_colonnes_a_afficher.curselection()

        def lire_fichier_log(self):
            """This function reads the log file and returns a list of objects Lignelog."""
            liste_lignes = []
            try:
                with open("iptables.log", "r") as fichier:
                    lignes = fichier.readlines()
                    num_ligne = 0
                    for ligne in lignes:
                        num_ligne += 1
                        ligne_coupee = self.Lignelog(ligne, num_ligne)
                        liste_lignes.append(ligne_coupee)
            except FileNotFoundError as erreur:
                appeler_fenetre_erreur(erreur, "Fichier log introuvable, veuillez lire le README.")
            return liste_lignes

        def remplir_tableau(self):
            """This function clears the treeview object "tableau", then inserts the new fresh lines in it.

            It calls the funtion trier_resultats to gather the list of lines to insert.

            """
            try:
                self.tableau.delete(*self.tableau.get_children())
                liste_triee_a_inserer_dans_tableau = self.trier_resultats(self.liste_lignes_log_initiale)
                for ligne_liste_triee in liste_triee_a_inserer_dans_tableau:
                    self.tableau.insert("", "end", values=(list(ligne_liste_triee.__dict__.values())))
            except NameError as err_remplir_tableau:
                appeler_fenetre_erreur(err_remplir_tableau, "Liste non initialisée, veuillez cliquer sur Initialiser.")

        def trier_resultats(self, lignes_du_log):
            """This function is invoked by the function remplir_tableau().

            Its purpose is mainly to trigger other functions to sort and filter results.

            """
            # cle contains the columns that we want to display in our table :
            cle = "".join(x for x, y in dico_colonnes.items() if y == self.combobox_tri.get())
            # v_inverser_tri is a boolean, its value is True if we want to reverse the sorting :
            v_inverser_tri = self.checkbox_var_tri.get()
            self.dico_filtre = self.init_dico_filtres()
            liste_filtree_tri = self.filtrer_liste(lignes_du_log, self.dico_filtre)
            liste_limitee_tri = self.limiter_resultats(liste_filtree_tri)
            liste_triee = self.tri_liste(liste_limitee_tri, cle, v_inverser_tri)
            return liste_triee

        @staticmethod
        def filtrer_liste(liste_a_filtrer, liste_filtres):
            """This function's purpose is to filter the results.

            It takes as arguments the list of lines to filter and the list of filters.
            It then compares each line "attribute" to the filters' ones. If it finds a match, the line is added to the
            list liste_filtree_generee that is returned.

            """
            liste_filtree_generee = []
            for ligne_a_filtrer in liste_a_filtrer:
                present = True
                for cle_dico in dico_colonnes.keys():
                    attribut_filtre = liste_filtres[cle_dico]
                    attribut_ligne = getattr(ligne_a_filtrer, cle_dico)
                    if len(attribut_filtre) > 0 and attribut_ligne not in attribut_filtre:
                        present = False
                if present is True:
                    liste_filtree_generee.append(ligne_a_filtrer)
            return liste_filtree_generee

        def limiter_resultats(self, liste_filtree):
            """This function limits the number of lines to display in the table.

            It takes as argument the list of lines to narrow down and returns a list limited by the specified number.

            """
            # We fetch the number of elements to display. If the input box is empty or if the number is bigger than the
            # number of elements in the list (the number of lines in the log file), then we keep all of them.
            # This number is stored in the variable nombre_elements_a_afficher.
            nombre_elements_dans_liste = len(liste_filtree)
            liste_limitee = []
            try:
                nombre_elements_a_afficher = int(self.inpbox_nb_lignes_a_afficher.get()) \
                    if (int(self.inpbox_nb_lignes_a_afficher.get()) <= nombre_elements_dans_liste) \
                    else nombre_elements_dans_liste
            except ValueError:
                nombre_elements_a_afficher = nombre_elements_dans_liste
            nombre_elements_affiches = 0
            # We check the status of the checkbox "checkbox_dernier". If it's checked, we create a list of X lasts lines
            # of the log file, else we create a list of X firsts ones (where X is the number of lines to display).
            if self.checkbox_dernier.get():
                nombre_elements_affiches = nombre_elements_dans_liste - nombre_elements_a_afficher
                while nombre_elements_affiches < nombre_elements_dans_liste:
                    dico_attrib = vars(liste_filtree[nombre_elements_affiches])
                    liste_limitee.insert(nombre_elements_affiches, self.Lignelimitee(list(dico_attrib.values())))
                    nombre_elements_affiches += 1
            else:
                while nombre_elements_affiches < nombre_elements_a_afficher:
                    dico_attrib = vars(liste_filtree[nombre_elements_affiches])
                    liste_limitee.insert(nombre_elements_affiches, self.Lignelimitee(list(dico_attrib.values())))
                    nombre_elements_affiches += 1
            return liste_limitee

        @staticmethod
        def tri_liste(liste_a_trier, colonne_tri, inverse):
            """This function sorts the provided list.

            It takes as arguments the list of lines to sort, the column to sort by (str), and
            a boolean to reverse the sorting if needed.

            """
            liste_a_trier.sort(key=lambda ligne_tri: getattr(ligne_tri, colonne_tri), reverse=inverse)
            return liste_a_trier

        class Lignelimitee:
            """The objects from this class have similar attributes to those of Lignelog.

            It basically recreates the lines after all filters and sorting have been applied.

            """

            def __init__(self, liste_arguments):
                index_dico_attributs = 0
                for cle_dico_attribut in dico_colonnes.keys():
                    setattr(self, cle_dico_attribut, liste_arguments[index_dico_attributs])
                    index_dico_attributs += 1
    except Exception as err_generale:
        appeler_fenetre_erreur(err_generale)


verif_sudo()


