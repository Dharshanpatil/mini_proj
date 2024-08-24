import tkinter as tk
from alphabet_app import AlphabetApp  # Assuming your AlphabetApp class is in alphabet_app.py
from number_app import NumberApp  # Assuming your NumberApp class is in number_app.py

class LearningApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Educational Games")

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack()

        self.educational_games_button = tk.Button(self.main_frame, text="Educational Games", font=("Arial", 24, "bold"), command=self.open_learning_page, bg="#ffb3b3", fg="#000000")
        self.educational_games_button.pack(pady=30)

    def open_learning_page(self):
        """Transitions to the learning page with options for alphabets and numbers."""
        self.main_frame.pack_forget()

        self.learning_frame = tk.Frame(self.master)
        self.learning_frame.pack()

        learn_alphabets_button = tk.Button(self.learning_frame, text="Learn Alphabets (A-Z)", font=("Arial", 20, "bold"), command=self.start_alphabet_learning, bg="#ffb3b3", fg="#000000")
        learn_alphabets_button.pack(pady=20)

        learn_numbers_button = tk.Button(self.learning_frame, text="Learn Numbers (0-9)", font=("Arial", 20, "bold"), command=self.start_number_learning, bg="#e0e0ff", fg="#000080")
        learn_numbers_button.pack(pady=20)

        back_button = tk.Button(self.learning_frame, text="Back", command=self.switch_to_main, bg="#ffffb3", fg="#800000")
        back_button.pack(pady=20)

    def switch_to_main(self):
        """Transitions back to the main menu window."""
        self.learning_frame.pack_forget()
        self.main_frame.pack()

    def start_alphabet_learning(self):
        """Starts the alphabet learning game."""
        self.learning_frame.pack_forget()
        self.alphabet_frame = tk.Frame(self.master)
        self.alphabet_frame.pack()

        alphabet_app = AlphabetApp(self.alphabet_frame)

        back_button = tk.Button(self.alphabet_frame, text="Back", command=self.switch_to_alphabet_menu, bg="#ffffb3", fg="#800000")
        back_button.pack(pady=20)

    def switch_to_alphabet_menu(self):
        """Transitions back to the alphabet menu."""
        self.alphabet_frame.pack_forget()
        self.open_learning_page()

    def start_number_learning(self):
        """Starts the number learning game."""
        self.learning_frame.pack_forget()
        self.number_frame = tk.Frame(self.master)
        self.number_frame.pack()

        number_app = NumberApp(self.number_frame)

        back_button = tk.Button(self.number_frame, text="Back", command=self.switch_to_number_menu, bg="#ffffb3", fg="#800000")
        back_button.pack(pady=20)

    def switch_to_number_menu(self):
        """Transitions back to the number menu."""
        self.number_frame.pack_forget()
        self.open_learning_page()

def main():
    root = tk.Tk()
    app = LearningApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
