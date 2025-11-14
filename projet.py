import tkinter as tk
import random
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ----------------------
#   FILES
# ----------------------
LOGIN_FILE = "login.txt"
IMAGE_FILE = "dog-and-cat-paws-with-sharp-claws-cute-animal-footprints-png.png"


# ----------------------
#   QUESTIONS
# ----------------------
questions = [
    {"q": "Capitale de la France ?", "o": ["Lyon", "Paris", "Nice", "Toulouse"], "r": "Paris"},
    {"q": "Plus grand océan ?", "o": ["Atlantique", "Indien", "Pacifique", "Arctique"], "r": "Pacifique"},
    {"q": "Combien de côtés un triangle ?", "o": ["2", "3", "4", "5"], "r": "3"},
    {"q": "Qui a peint la Joconde ?", "o": ["Picasso", "Van Gogh", "Da Vinci", "Monet"], "r": "Da Vinci"},
]


# ----------------------
#   GLOBAL VARIABLES
# ----------------------
user = ""
score = 0
question_number = 0
current_question = {}
options = []


# ----------------------
#   READ ACCOUNTS
# ----------------------
def lire_users():
    users = {}
    if not os.path.exists(LOGIN_FILE):
        return users
    try:
        with open(LOGIN_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(":")
                if len(parts) == 3:
                    name, pwd, best = parts
                    users[name] = [pwd, int(best)]
    except:
        pass
    return users


# ----------------------
#   WRITE ACCOUNT
# ----------------------
def ecrire_user(name, pwd, sc):
    users = lire_users()
    users[name] = [pwd, sc]
    with open(LOGIN_FILE, "w", encoding="utf-8") as f:
        for u, info in users.items():
            f.write(u + ":" + info[0] + ":" + str(info[1]) + "\n")


# ----------------------
#   MAIN WINDOW
# ----------------------
f = tk.Tk()
f.title("Mon Quiz")
f.geometry("600x520")
f.configure(bg="#FFE4F2")


# ----------------------
#   MENU BAR
# ----------------------
menuBar = tk.Menu(f)

menu_jeu = tk.Menu(menuBar, tearoff=0)
menu_jeu.add_command(label="Voir Stats", command=lambda: voir_stats(skip_login=False))
menu_jeu.add_separator()
menu_jeu.add_command(label="Quitter", command=f.quit)
menuBar.add_cascade(label="Jeu", menu=menu_jeu)

menu_aide = tk.Menu(menuBar, tearoff=0)
menu_aide.add_command(label="Aide", command=lambda: montrer_aide())
menuBar.add_cascade(label="Aide", menu=menu_aide)

f.config(menu=menuBar)  # ← MENU ATTACHED


# ----------------------
#   HEADER (Canvas)
# ----------------------
can = tk.Canvas(f, width=560, height=90, bg="#FFCCE1", highlightthickness=0)
can.pack(pady=15)

can.create_text(280, 25, text="Bienvenue au Quiz !", font=("Arial", 16, "bold"), fill="#C84B74")

try:
    img = tk.PhotoImage(file=IMAGE_FILE)
    if img.width() > 70 or img.height() > 70:
        img = img.subsample(3, 3)
    can.create_image(55, 45, image=img)
except:
    pass

can.create_rectangle(160, 55, 400, 82, fill="#FFB6D5", outline="#FFB6D5")
username_display = can.create_text(280, 69, text="", font=("Arial", 13, "bold"), fill="#C84B74")


# ----------------------
#   UPDATE USERNAME
# ----------------------
def update_username():
    can.itemconfig(username_display, text=user)


# ----------------------
#   LOGIN / SIGNUP
# ----------------------
def login():
    global user
    name = entry_user.get().strip()
    pwd = entry_pass.get()

    if not name or not pwd:
        label_info.config(text="Entrez nom et mot de passe", fg="red")
        return

    users = lire_users()

    if name in users and users[name][0] == pwd:
        user = name
        update_username()
        label_info.config(text="Connecté !", fg="green")
        f.after(800, debut_quiz)
    else:
        label_info.config(text="Mauvais identifiants !", fg="red")


def inscription():
    global user
    name = entry_user.get().strip()
    pwd = entry_pass.get()

    if len(name) < 2 or len(pwd) < 1:
        label_info.config(text="Nom ou mot de passe trop court", fg="red")
        return

    users = lire_users()
    if name in users:
        label_info.config(text="Ce nom existe déjà !", fg="red")
    else:
        ecrire_user(name, pwd, 0)
        user = name
        update_username()
        label_info.config(text="Compte créé !", fg="green")
        f.after(1000, debut_quiz)


# ----------------------
#   START QUIZ
# ----------------------
def debut_quiz():
    global score, question_number
    score = 0
    question_number = 0
    f.geometry("600x520")
    f.attributes('-fullscreen', False)
    cacher_tout()
    charger_question()


# ----------------------
#   LOAD QUESTION
# ----------------------
def charger_question():
    global current_question, options

    if question_number >= len(questions):
        fin_quiz()
        return

    current_question = questions[question_number]
    options = current_question["o"][:]
    random.shuffle(options)

    label_question.config(text=current_question["q"])

    for i in range(4):
        boutons[i].config(text=options[i])
        boutons[i]['value'] = options[i]

    label_question.pack(pady=20)
    for b in boutons:
        b.pack(pady=4)
    btn_valider.pack(pady=14)
    label_result.pack_forget()


# ----------------------
#   CHECK ANSWER
# ----------------------
def verifier():
    global score
    choix = answer_var.get()

    if choix == current_question["r"]:
        score += 1
        label_result.config(text="Correct !", fg="green")
    else:
        label_result.config(text="Faux ! La bonne réponse était : " + current_question["r"], fg="red")

    label_result.pack(pady=10)
    btn_valider.pack_forget()
    btn_suivant.pack(pady=10)


# ----------------------
#   NEXT QUESTION
# ----------------------
def suivant():
    global question_number
    question_number += 1
    btn_suivant.pack_forget()
    label_result.pack_forget()
    charger_question()


# ----------------------
#   END QUIZ
# ----------------------
def fin_quiz():
    users = lire_users()
    old_best = users[user][1] if user in users else 0
    new_best = max(score, old_best)

    if new_best > old_best:
        pwd = users[user][0] if user in users else entry_pass.get()
        ecrire_user(user, pwd, new_best)

    f.geometry("600x520")
    f.attributes('-fullscreen', False)
    cacher_tout()

    msg = f"Bravo {user} !\nScore : {score}/{len(questions)}\nMeilleur score : {new_best}"
    tk.Label(f, text=msg, font=("Arial", 16, "bold"), bg="#FFE4F2").pack(pady=35)

    tk.Button(f, text="Rejouer", command=debut_quiz,
              bg="#FF8DB4", fg="white", width=15).pack(pady=5)

    tk.Button(f, text="Voir Stats", command=lambda: voir_stats(skip_login=True),
              bg="#D679A6", fg="white", width=15).pack(pady=5)

    tk.Button(f, text="Quitter", command=f.quit,
              bg="#FF6F91", fg="white", width=15).pack(pady=5)


# ----------------------
#   SEE STATS
# ----------------------
def voir_stats(skip_login=False):
    if not skip_login and not user:
        label_info.config(text="Connectez-vous d'abord !", fg="red")
        return

    f.attributes('-fullscreen', True)
    cacher_tout()
    tk.Label(f, text="Meilleurs Scores", font=("Arial", 22, "bold"), bg="#FFE4F2").pack(pady=10)
    tk.Button(f, text="Retour", command=lambda: f.attributes('-fullscreen', False) or (fin_quiz() if user else montrer_login()),
              bg="#D97A9D", fg="white", font=("Arial", 12), width=18).pack(pady=20)

    users = lire_users()
    if not users:
        tk.Label(f, text="Aucun score enregistré", bg="#FFE4F2", font=("Arial", 14)).pack(pady=30)
        tk.Button(f, text="Retour", command=lambda: f.attributes('-fullscreen', False) or fin_quiz() if user else montrer_login(),
                  bg="#D97A9D", fg="white", font=("Arial", 12)).pack(pady=15)
        return

    names = list(users.keys())
    scores = [users[n][1] for n in names]

    fig, ax = plt.subplots(figsize=(12, 7), facecolor="#FFE4F2")
    bars = ax.barh(names, scores, color="#F4A9C4", edgecolor="#C84B74", height=0.6)
    ax.set_facecolor("#FFFFFF")
    ax.tick_params(colors="#C84B74", labelsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color("#C84B74")
    ax.spines['bottom'].set_color("#C84B74")
    ax.set_xlabel("Score", color="#C84B74", fontsize=16)
    ax.set_title("Classement des joueurs", color="#C84B74", fontsize=20, pad=30)

    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 0.4, bar.get_y() + bar.get_height()/2, str(scores[i]),
                va='center', color="#C84B74", fontweight='bold', fontsize=14)

    canvas = FigureCanvasTkAgg(fig, master=f)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=30, padx=80, expand=True)


# ----------------------
#   AIDE
# ----------------------
def montrer_aide():
    aide = tk.Toplevel(f)
    aide.title("Aide - Comment jouer")
    aide.geometry("550x480")
    aide.configure(bg="#FFE4F2")
    aide.transient(f)
    aide.grab_set()

    tk.Label(aide, text="Comment jouer au Quiz ?", font=("Arial", 16, "bold"), bg="#FFE4F2", fg="#C84B74").pack(pady=15)

    texte = """
• Connectez-vous ou inscrivez-vous avec un nom et mot de passe.
• Cliquez sur "Se connecter" ou "S'inscrire".
• Répondez aux questions en choisissant une option.
• Cliquez sur "Valider" puis "Suivant".
• À la fin, voyez votre score et vos stats !

Astuces :
- Les options sont mélangées à chaque fois.
- Votre meilleur score est sauvegardé.
- Utilisez le menu "Jeu → Voir Stats" pour voir le classement.
    """
    tk.Label(aide, text=texte, font=("Arial", 11), bg="#FFE4F2", justify="left", wraplength=500).pack(pady=10, padx=20)

    tk.Button(aide, text="Fermer", command=aide.destroy, bg="#FF8DB4", fg="white", width=15).pack(pady=15)


# ----------------------
#   SHOW LOGIN
# ----------------------
def montrer_login():
    f.geometry("600x520")
    f.attributes('-fullscreen', False)
    cacher_tout()

    tk.Label(f, text="Connexion / Inscription", font=("Arial", 16),
             bg="#FFE4F2").pack(pady=20)

    login_frame = tk.Frame(f, bg="#FFE4F2")
    login_frame.pack(pady=10)

    tk.Label(login_frame, text="Nom :", font=("Arial", 16), bg="#FFE4F2")\
        .grid(row=0, column=0, sticky="e", padx=(0, 10), pady=5)
    global entry_user
    entry_user = tk.Entry(login_frame, font=("Arial", 12), width=22, justify="center")
    entry_user.grid(row=0, column=1, pady=5)

    tk.Label(login_frame, text="Mot de passe :", font=("Arial", 16), bg="#FFE4F2")\
        .grid(row=1, column=0, sticky="e", padx=(0, 10), pady=5)
    global entry_pass
    entry_pass = tk.Entry(login_frame, font=("Arial", 12), width=22, show="*", justify="center")
    entry_pass.grid(row=1, column=1, pady=5)

    tk.Button(f, text="Se connecter", command=login,
              bg="#FF8DB4", fg="white", width=18).pack(pady=6)

    tk.Button(f, text="S'inscrire", command=inscription,
              bg="#D97A9D", fg="white", width=18).pack(pady=6)

    global label_info
    label_info = tk.Label(f, text="", bg="#FFE4F2")
    label_info.pack()


# ----------------------
#   HIDE ALL WIDGETS
# ----------------------
def cacher_tout():
    for w in f.winfo_children():
        if w != can:
            w.pack_forget()
    for w in f.winfo_children():
        if isinstance(w, tk.Toplevel):
            w.destroy()


# ----------------------
#   QUIZ WIDGETS
# ----------------------
label_question = tk.Label(f, text="", font=("Arial", 14), bg="#FFE4F2", wraplength=520)

answer_var = tk.StringVar()
boutons = []

for i in range(4):
    b = tk.Radiobutton(f, text="", variable=answer_var, value="",
                       font=("Arial", 11), bg="#FFE4F2",
                       selectcolor="#F6D1E0", indicatoron=0,
                       width=42, height=2)
    boutons.append(b)

btn_valider = tk.Button(f, text="Valider", command=verifier,
                        bg="#FF8DB4", fg="white", font=("Arial", 11, "bold"))

btn_suivant = tk.Button(f, text="Suivant", command=suivant,
                        bg="#D97A9D", fg="white", font=("Arial", 11, "bold"))

label_result = tk.Label(f, text="", font=("Arial", 12), bg="#FFE4F2")


# ----------------------
#   INITIAL LOGIN SCREEN
# ----------------------
montrer_login()


# ----------------------
#   RUN APPLICATION
# ----------------------
f.mainloop()