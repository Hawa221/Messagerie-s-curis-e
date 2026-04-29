import tkinter as tk
from tkinter import messagebox

class AppMessagerie:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Messagerie Sécurisée 🔐")
        self.fenetre.geometry("400x500")
        self.fenetre.configure(bg="#1e1e2e")
        self.username_actuel = None
        self.afficher_connexion()
        self.fenetre.mainloop()

    def vider_fenetre(self):
        for widget in self.fenetre.winfo_children():
            widget.destroy()

    def afficher_connexion(self):
        self.vider_fenetre()

        tk.Label(self.fenetre, text="🔐 Messagerie Sécurisée",
                 font=("Arial", 18, "bold"), bg="#1e1e2e", fg="white").pack(pady=30)

        tk.Label(self.fenetre, text="Nom d'utilisateur",
                 bg="#1e1e2e", fg="white").pack()
        self.champ_username = tk.Entry(self.fenetre, width=30)
        self.champ_username.pack(pady=5)

        tk.Label(self.fenetre, text="Mot de passe",
                 bg="#1e1e2e", fg="white").pack()
        self.champ_password = tk.Entry(self.fenetre, width=30, show="*")
        self.champ_password.pack(pady=5)

        tk.Button(self.fenetre, text="Se connecter", width=20,
                  bg="#7c3aed", fg="white",
                  command=self.connexion).pack(pady=15)

        tk.Button(self.fenetre, text="Pas de compte ? S'inscrire",
                  bg="#1e1e2e", fg="#a78bfa", bd=0,
                  command=self.afficher_inscription).pack()

    def connexion(self):
        username = self.champ_username.get()
        password = self.champ_password.get()

        if username == "" or password == "":
            messagebox.showerror("Erreur", "Remplis tous les champs !")
        else:
            self.username_actuel = username
            self.afficher_conversations()

    def afficher_inscription(self):
        self.vider_fenetre()

        tk.Label(self.fenetre, text="📝 Inscription",
                 font=("Arial", 18, "bold"), bg="#1e1e2e", fg="white").pack(pady=30)

        tk.Label(self.fenetre, text="Nom d'utilisateur",
                 bg="#1e1e2e", fg="white").pack()
        self.champ_username = tk.Entry(self.fenetre, width=30)
        self.champ_username.pack(pady=5)

        tk.Label(self.fenetre, text="Mot de passe",
                 bg="#1e1e2e", fg="white").pack()
        self.champ_password = tk.Entry(self.fenetre, width=30, show="*")
        self.champ_password.pack(pady=5)

        tk.Label(self.fenetre, text="Confirmer mot de passe",
                 bg="#1e1e2e", fg="white").pack()
        self.champ_confirm = tk.Entry(self.fenetre, width=30, show="*")
        self.champ_confirm.pack(pady=5)

        tk.Button(self.fenetre, text="S'inscrire", width=20,
                  bg="#7c3aed", fg="white",
                  command=self.inscription).pack(pady=15)

        tk.Button(self.fenetre, text="Déjà un compte ? Se connecter",
                  bg="#1e1e2e", fg="#a78bfa", bd=0,
                  command=self.afficher_connexion).pack()

    def inscription(self):
        username = self.champ_username.get()
        password = self.champ_password.get()
        confirm = self.champ_confirm.get()

        if username == "" or password == "" or confirm == "":
            messagebox.showerror("Erreur", "Remplis tous les champs !")
        elif password != confirm:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas !")
        else:
            self.username_actuel = username
            self.afficher_conversations()

    def afficher_conversations(self):
        self.vider_fenetre()
        self.chat_actif = None

        tk.Label(self.fenetre, text=f"Bonjour {self.username_actuel} 👋",
                 font=("Arial", 16, "bold"), bg="#1e1e2e", fg="white").pack(pady=20)

        tk.Label(self.fenetre, text="Mes conversations",
                 font=("Arial", 12), bg="#1e1e2e", fg="#a78bfa").pack()

        self.cadre_conversations = tk.Frame(self.fenetre, bg="#1e1e2e")
        self.cadre_conversations.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Button(self.fenetre, text="+ Nouvelle conversation",
                  bg="#7c3aed", fg="white", width=25,
                  command=self.nouvelle_conversation).pack(pady=10)

        tk.Button(self.fenetre, text="Se déconnecter",
                  bg="#1e1e2e", fg="#a78bfa", bd=0,
                  command=self.afficher_connexion).pack()

    def nouvelle_conversation(self):
        popup = tk.Toplevel(self.fenetre)
        popup.title("Nouvelle conversation")
        popup.geometry("300x200")
        popup.configure(bg="#1e1e2e")
        popup.grab_set()
        popup.focus_force()

        tk.Label(popup, text="Nom d'utilisateur :",
                 bg="#1e1e2e", fg="white").pack(pady=10)

        champ = tk.Entry(popup, width=25)
        champ.pack(pady=5)
        champ.focus()

        def confirmer():
            user = champ.get()
            if user == "":
                messagebox.showerror("Erreur", "Entre un nom d'utilisateur !", parent=popup)
            else:
                popup.destroy()
                self.afficher_chat(user)

        tk.Button(popup, text="Démarrer la conversation",
                  bg="#7c3aed", fg="white",
                  command=confirmer).pack(pady=15)

        popup.bind("<Return>", lambda e: confirmer())
    def afficher_chat(self, destinataire):
        self.vider_fenetre()
        self.chat_actif = destinataire

        tk.Label(self.fenetre, text=f"💬 {destinataire}",
                 font=("Arial", 16, "bold"), bg="#1e1e2e", fg="white").pack(pady=10)

        tk.Button(self.fenetre, text="⬅ Retour",
                  bg="#1e1e2e", fg="#a78bfa", bd=0,
                  command=self.afficher_conversations).pack(anchor="w", padx=10)

        self.zone_messages = tk.Text(self.fenetre, width=45, height=15,
                                     bg="#2d2b55", fg="white",
                                     font=("Arial", 10),
                                     state="disabled",
                                     wrap="word")
        self.zone_messages.pack(padx=10, pady=10)

        cadre_bas = tk.Frame(self.fenetre, bg="#1e1e2e")
        cadre_bas.pack(fill="x", padx=10, pady=5)

        self.champ_message = tk.Entry(cadre_bas, width=30, font=("Arial", 11))
        self.champ_message.pack(side="left", padx=5)

        tk.Button(cadre_bas, text="Envoyer →",
                  bg="#7c3aed", fg="white",
                  command=lambda: self.envoyer_message(destinataire)).pack(side="left")

        self.rafraichir_messages(destinataire)

    def envoyer_message(self, destinataire):
        message = self.champ_message.get()

        if message == "":
            messagebox.showerror("Erreur", "Écris un message !")
            return

        self.zone_messages.config(state="normal")
        self.zone_messages.insert("end", f"Moi : {message}\n")
        self.zone_messages.config(state="disabled")
        self.zone_messages.see("end")
        self.champ_message.delete(0, "end")

    def rafraichir_messages(self, destinataire):
        if hasattr(self, 'chat_actif') and self.chat_actif == destinataire:
            self.fenetre.after(3000, lambda: self.rafraichir_messages(destinataire))

AppMessagerie()