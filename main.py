from tkinter import *
import pandas
import random

# Initialize variables and data
learn = {}
bg = "#B1DDC6"
current_card = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    orig_data = pandas.read_csv("data/french_words.csv")
    learn = orig_data.to_dict(orient="records")
else:
    learn = data.to_dict(orient="records")

# Functions
def is_known():
    learn.remove(current_card)
    print(len(learn))
    data = pandas.DataFrame(learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(learn)
    canvas.itemconfig(card_title, text="French", fill="grey")
    canvas.itemconfig(card_word, text=current_card["French"], fill="grey")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

# Create GUI window
window = Tk()
window.title("Flash")
window.config(padx=50, pady=50, bg=bg)

# Initialize flip timer
flip_timer = window.after(3000, func=flip_card)

# Create canvas for flashcards
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=bg, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Create "I don't know" button
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

# Create "I know" button
check_image = PhotoImage(file="images/right.png")
button = Button(image=check_image, highlightthickness=0, command=is_known)
button.grid(row=1, column=1)

# Start with the first flashcard
next_card()

# Run the GUI main loop
window.mainloop()