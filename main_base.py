#-------------------------------------------------------------------------------
# Name:        téléchargeur de video V 1.0
# Purpose:     Logiciel permettant le téléchargement de video Youtube
#
# Author:      Didier Mathias
#
# Created:     11/05/2021
#-------------------------------------------------------------------------------
# visualisation fenêtre
#-------------------------------------------------------------------------------
# enregistrer sous     format        |_| mode automatique
#-------------------------------------------------------------------------------
#                       Veuillez entrer un url
#              |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#                               Valider
#-------------------------------------------------------------------------------

from tkinter import Entry, Button, Tk, Label, Menu, filedialog, messagebox, StringVar
from pytube import YouTube # mettre d'autres site, on sait jamais


class telechargeur:
    def __init__(self):
        self.dossier_enregistrement = "contenue_telecharger/"
        self.format = ".mp3"

    def choice_dossier(self):
        fichier = filedialog.askdirectory()
        if fichier != "":
            self.dossier_enregistrement = fichier

    def choice_format(self, format):
        self.format = format

    def lancement(self):
        self.root = Tk()
        self.root.title("Télechargeur")
        self.root.iconbitmap("telechargeur_icone.ico")

        barre_menu = Menu(self.root)
        barre_menu.add_command(label = "enregistrer sous", command = self.choice_dossier)

        format = Menu(barre_menu, tearoff = 0)
        format.add_command(label = ".mp3 (audio)", command = lambda x=".mp3": self.choice_format(x))
        format.add_command(label = ".mp4 (video)", command = lambda x=".mp4": self.choice_format(x))

        barre_menu.add_cascade(label = "format", menu = format)

        self.root.configure(menu = barre_menu, bg = "green")

        """
        bouton pour mode automatique, une foir appuyer, le fenêtre se vide et on aperçoit un compteur avec 2 boutons radio en dessous = telechargement mp3 ou mp4, le mp3 est chois de base
        Toutes les minutes, on vérifie l'url de la page courante, s'il est différents du précédent enregistrer et qu'on n'as pas déjà télécharger cette musique, alors elle est télécharger
        si la musique a déjà été télécharger, elle apparait dans une listbox, un double clique dessus et elle se télécharge
        """

        Label(self.root, text = "Entrez l'url de la video :").pack()
        barre = Entry(self.root, width = 100)
        barre.pack()

        Button(self.root, text = "Valider", command = lambda x=barre: self.telechargement(x.get())).pack()

        self.root.mainloop()

    def telechargement(self, url):
        """
        on détecte le site (youtube, daylimotion, ...) grâce à l'url, si le site n'est pas pris en charge, on affiche une erreur l'indiquant
        on télécharge la vidéo selon le format selectionner
        si on n'y parvient pas, on affiche une erreur indiquant que c'est impossible (réessayer plus tard)
        """
        self.root.configure(bg = "red")
        self.root.update()

        try:
            video = YouTube(url)
            if self.format == ".mp3":
                streams = video.streams.filter(only_audio = True, file_extension = 'mp3')
            elif self.format == ".mp4":
            	streams = video.streams.filter(progressive = True, file_extension = 'mp4').order_by("resolution").desc()

            streams[0].download(output_path = self.dossier_enregistrement)
        except:
            messagebox.showerror("Erreur de téléchargement", "Une erreur s'est produite, veuillez essayer une des propositions suivantes :\n\t- Vérifier l'url\n\t- Vérifier la connexion internet\n\t- Retenter plus tard")

        self.root.configure(bg = "green")


if __name__ == "__main__":
    App = telechargeur()
    App.lancement()