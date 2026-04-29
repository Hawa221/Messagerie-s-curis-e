import tkinter as tk
from tkinter import messagebox
from gestion_utilisateurs import inscrire_utilisateur, connecter_utilisateur, get_user_id
from gestion_messages import envoyer_message, recevoir_messages
from database import create_tables

# ── Palette ────────────────────────────────────────────────
BG        = "#0f0f17"
PANEL     = "#1a1a2e"
CARD      = "#16213e"
ACCENT    = "#6c63ff"
ACCENT2   = "#e94560"
TXT       = "#e0e0e0"
TXT_DIM   = "#7a7a9a"
GREEN     = "#00d4aa"
BUBBLE_ME = "#6c63ff"
BUBBLE_HIM= "#1e1e3a"
FONT      = "Helvetica"


def style_entry(e):
    e.configure(bg=CARD, fg=TXT, insertbackground=TXT,
                relief="flat", font=(FONT, 11),
                highlightthickness=1, highlightcolor=ACCENT,
                highlightbackground=TXT_DIM)


def style_btn(b, color=ACCENT, text_color="white"):
    b.configure(bg=color, fg=text_color, relief="flat",
                font=(FONT, 10, "bold"), cursor="hand2",
                activebackground=ACCENT2, activeforeground="white",
                padx=12, pady=6)


class AppMessagerie:
    def __init__(self):
        create_tables()
        self.username_actuel = None
        self.chat_actif = None
        self._refresh_job = None

        self.root = tk.Tk()
        self.root.title("Messagerie Sécurisée")
        self.root.geometry("460x580")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root, bg=BG)
        self.frame.pack(fill="both", expand=True)

        self.afficher_connexion()
        self.root.mainloop()

    def vider(self):
        
        if self._refresh_job:
            self.root.after_cancel(self._refresh_job)
            self._refresh_job = None
        self.chat_actif = None
        for w in self.frame.winfo_children():
            w.destroy()
        self.root.unbind("<Return>")

    # ════════════════════════════════════════════════════
    # CONNEXION
    # ════════════════════════════════════════════════════

    def afficher_connexion(self):
        self.vider()

        tk.Label(self.frame, text="🔐", font=(FONT, 40),
                 bg=BG, fg=ACCENT).pack(pady=(50, 5))
        tk.Label(self.frame, text="SecureChat",
                 font=(FONT, 22, "bold"), bg=BG, fg=TXT).pack()
        tk.Label(self.frame, text="Messagerie chiffrée de bout en bout",
                 font=(FONT, 9), bg=BG, fg=TXT_DIM).pack(pady=(2, 30))

        self._champ_user = self._champ("Nom d'utilisateur")
        self._champ_pass = self._champ("Mot de passe", secret=True)

        btn = tk.Button(self.frame, text="Se connecter", width=22,
                        command=self._connexion)
        style_btn(btn)
        btn.pack(pady=(18, 6))

        lien = tk.Label(self.frame, text="Pas encore de compte ? S'inscrire →",
                        font=(FONT, 9), bg=BG, fg=ACCENT, cursor="hand2")
        lien.pack()
        lien.bind("<Button-1>", lambda e: self.afficher_inscription())
        self.root.bind("<Return>", lambda e: self._connexion())

    def _connexion(self):
        u = self._champ_user.get().strip()
        p = self._champ_pass.get()
        if not u or not p:
            messagebox.showerror("Erreur", "Remplis tous les champs !")
            return
        ok, err = connecter_utilisateur(u, p)
        if ok:
            self.username_actuel = u
            self.afficher_accueil()
        else:
            messagebox.showerror("Connexion échouée", err)

    # ════════════════════════════════════════════════════
    # INSCRIPTION
    # ════════════════════════════════════════════════════

    def afficher_inscription(self):
        self.vider()

        tk.Label(self.frame, text="Créer un compte",
                 font=(FONT, 20, "bold"), bg=BG, fg=TXT).pack(pady=(50, 5))
        tk.Label(self.frame, text="Vos clés de chiffrement seront générées automatiquement",
                 font=(FONT, 9), bg=BG, fg=TXT_DIM).pack(pady=(0, 25))

        self._champ_user = self._champ("Nom d'utilisateur")
        self._champ_pass = self._champ("Mot de passe (8 car. min.)", secret=True)
        self._champ_conf = self._champ("Confirmer le mot de passe", secret=True)

        btn = tk.Button(self.frame, text="Créer mon compte", width=22,
                        command=self._inscription)
        style_btn(btn)
        btn.pack(pady=(18, 6))

        lien = tk.Label(self.frame, text="← Déjà un compte ? Se connecter",
                        font=(FONT, 9), bg=BG, fg=ACCENT, cursor="hand2")
        lien.pack()
        lien.bind("<Button-1>", lambda e: self.afficher_connexion())
        self.root.bind("<Return>", lambda e: self._inscription())

    def _inscription(self):
        u = self._champ_user.get().strip()
        p = self._champ_pass.get()
        c = self._champ_conf.get()
        if not u or not p or not c:
            messagebox.showerror("Erreur", "Remplis tous les champs !")
            return
        if p != c:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas !")
            return
        if len(p) < 8:
            messagebox.showerror("Erreur", "Mot de passe trop court (8 caractères minimum).")
            return
        ok, err = inscrire_utilisateur(u, p)
        if ok:
            self.username_actuel = u
            messagebox.showinfo("Compte créé ✅", f"Bienvenue {u} !\nVos clés RSA ont été générées.")
            self.afficher_accueil()
        else:
            messagebox.showerror("Erreur", err)

    # ════════════════════════════════════════════════════
    # ACCUEIL
    # ════════════════════════════════════════════════════

    def afficher_accueil(self):
        self.vider()

        header = tk.Frame(self.frame, bg=PANEL, pady=14)
        header.pack(fill="x")
        tk.Label(header, text=f"👤  {self.username_actuel}",
                 font=(FONT, 13, "bold"), bg=PANEL, fg=TXT).pack(side="left", padx=16)
        tk.Button(header, text="Déconnexion", font=(FONT, 8),
                  bg=PANEL, fg=TXT_DIM, relief="flat", cursor="hand2",
                  command=self.afficher_connexion).pack(side="right", padx=16)

        tk.Label(self.frame, text="Nouvelle conversation",
                 font=(FONT, 11, "bold"), bg=BG, fg=TXT).pack(anchor="w", padx=20, pady=(20, 4))

        row = tk.Frame(self.frame, bg=BG)
        row.pack(fill="x", padx=20)
        self._dest_entry = tk.Entry(row, width=24)
        style_entry(self._dest_entry)
        self._dest_entry.pack(side="left", ipady=6)
        self._dest_entry.insert(0, "Nom d'utilisateur…")
        self._dest_entry.bind("<FocusIn>",
            lambda e: self._dest_entry.delete(0, "end")
                      if self._dest_entry.get() == "Nom d'utilisateur…" else None)
        btn = tk.Button(row, text="→", width=4, command=self._ouvrir_chat)
        style_btn(btn)
        btn.pack(side="left", padx=(8, 0), ipady=4)

        tk.Label(self.frame,
                 text="🔒  Tous vos messages sont chiffrés avec RSA 2048 bits",
                 font=(FONT, 8), bg=BG, fg=TXT_DIM).pack(pady=(20, 0))

        self.root.bind("<Return>", lambda e: self._ouvrir_chat())

    def _ouvrir_chat(self):
        dest = self._dest_entry.get().strip()
        if not dest or dest == "Nom d'utilisateur…":
            messagebox.showerror("Erreur", "Entre un nom d'utilisateur !")
            return
        if dest == self.username_actuel:
            messagebox.showerror("Erreur", "Tu ne peux pas te parler à toi-même !")
            return
        if not get_user_id(dest):
            messagebox.showerror("Introuvable", f"L'utilisateur '{dest}' n'existe pas.")
            return
        self.afficher_chat(dest)

    # ════════════════════════════════════════════════════
    # CHAT
    # ════════════════════════════════════════════════════

    def afficher_chat(self, destinataire):
        self.vider()
        self.chat_actif = destinataire

      
        header = tk.Frame(self.frame, bg=PANEL, pady=12)
        header.pack(fill="x")
        tk.Button(header, text="←", font=(FONT, 13),
                  bg=PANEL, fg=TXT, relief="flat", cursor="hand2",
                  command=self.afficher_accueil).pack(side="left", padx=10)
        tk.Label(header, text=f"💬  {destinataire}",
                 font=(FONT, 13, "bold"), bg=PANEL, fg=TXT).pack(side="left")
        tk.Label(header, text="🔒 E2E",
                 font=(FONT, 8), bg=PANEL, fg=GREEN).pack(side="right", padx=14)


        canvas_frame = tk.Frame(self.frame, bg=BG)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=(8, 4))

        self._canvas = tk.Canvas(canvas_frame, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical",
                                 command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._msg_frame = tk.Frame(self._canvas, bg=BG)
        self._canvas_window = self._canvas.create_window(
            (0, 0), window=self._msg_frame, anchor="nw")
        self._msg_frame.bind("<Configure>", self._on_frame_resize)
        self._canvas.bind("<Configure>", self._on_canvas_resize)


        eph_bar = tk.Frame(self.frame, bg=PANEL, pady=4)
        eph_bar.pack(fill="x")
        self._var_eph = tk.BooleanVar()
        tk.Checkbutton(eph_bar, text="⏱  Message éphémère (disparaît en 5 min)",
                       variable=self._var_eph,
                       bg=PANEL, fg=TXT_DIM, selectcolor=PANEL,
                       activebackground=PANEL, activeforeground=ACCENT,
                       font=(FONT, 8), cursor="hand2").pack(side="left", padx=12)

        bottom = tk.Frame(self.frame, bg=PANEL, pady=10)
        bottom.pack(fill="x")
        self._msg_entry = tk.Entry(bottom, width=28)
        style_entry(self._msg_entry)
        self._msg_entry.pack(side="left", padx=(12, 6), ipady=7)
        self._msg_entry.focus()

        send_btn = tk.Button(bottom, text="Envoyer ➤",
                             command=lambda: self._envoyer(destinataire))
        style_btn(send_btn)
        send_btn.pack(side="left", ipady=5)

        self.root.bind("<Return>", lambda e: self._envoyer(destinataire))

      
        self._charger_messages(destinataire)

    def _on_frame_resize(self, event):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_resize(self, event):
        self._canvas.itemconfig(self._canvas_window, width=event.width)

    def _charger_messages(self, destinataire):
        # Stopper si on a changé d'écran
        if self.chat_actif != destinataire:
            return

        msgs = recevoir_messages(self.username_actuel, destinataire)

       
        for w in self._msg_frame.winfo_children():
            w.destroy()

        for msg in msgs:
            est_moi = (msg["expediteur"] == self.username_actuel)
            self._bulle(msg["contenu"], est_moi, msg.get("is_ephemere", False))

        self._canvas.update_idletasks()
        self._canvas.yview_moveto(1.0)

        # Relancer dans 1 seconde (et stocker le job pour pouvoir l'annuler)
        self._refresh_job = self.root.after(1000, lambda: self._charger_messages(destinataire))

    def _bulle(self, texte, est_moi, ephemere=False):
        row = tk.Frame(self._msg_frame, bg=BG)
        row.pack(fill="x", pady=3, padx=8)

        couleur = BUBBLE_ME if est_moi else BUBBLE_HIM
        side = "right" if est_moi else "left"
        anchor = "e" if est_moi else "w"
        prefixe = "⏱ " if ephemere else ""

        tk.Label(row, text=f"{prefixe}{texte}",
                 bg=couleur, fg=TXT,
                 font=(FONT, 10),
                 wraplength=260,
                 justify="left" if not est_moi else "right",
                 padx=12, pady=8).pack(side=side, anchor=anchor)

    def _envoyer(self, destinataire):
        texte = self._msg_entry.get().strip()
        if not texte:
            return
        ephemere = self._var_eph.get()
        ok, err = envoyer_message(self.username_actuel, destinataire, texte, ephemere=ephemere)
        if ok:
            self._msg_entry.delete(0, "end")
            self._var_eph.set(False)
            
            if self._refresh_job:
                self.root.after_cancel(self._refresh_job)
                self._refresh_job = None
            self._charger_messages(destinataire)
        else:
            messagebox.showerror("Erreur", err)

    # ════════════════════════════════════════════════════
    # UTILITAIRES
    # ════════════════════════════════════════════════════

    def _champ(self, placeholder, secret=False):
        tk.Label(self.frame, text=placeholder,
                 font=(FONT, 9), bg=BG, fg=TXT_DIM).pack(anchor="w", padx=60)
        e = tk.Entry(self.frame, width=30, show="*" if secret else "")
        style_entry(e)
        e.pack(ipady=7, pady=(2, 10))
        return e


AppMessagerie()