import tkinter as tk
import pyttsx3
import speech_recognition as sr
from PIL import Image, ImageTk
import random

class AlphabetApp:
    def __init__(self, master):
        self.master = master
        self.sentences = [
            "A for Apple",
            "B for Ball",
            "C for Cat",
            "D for Dog",
            "E for Elephant",
            "F for Fish",
            "G for Goat",
            "H for Horse",
            "I for Ice cream",
            "J for Jug",
            "K for Kite",
            "L for Lion",
            "M for Monkey",
            "N for Nest",
            "O for Orange",
            "P for Parrot",
            "Q for Queen",
            "R for Rabbit",
            "S for Sun",
            "T for Tiger",
            "U for Umbrella",
            "V for Violin",
            "W for Watch",
            "X for Xylophone",
            "Y for Yogurt",
            "Z for Zebra"
        ]
        self.index = 0
        self.chocolates = 0
        self.badges = [0] * len(self.sentences)  # Initialize badges for each sentence
        self.attempted_once = False  # Flag to track if the kid has attempted once
        
        self.sentence_label = tk.Label(master, text=self.sentences[self.index], font=('Arial', 20))
        self.sentence_label.pack(expand=True, fill=tk.BOTH)
        
        self.message_label = tk.Label(master, text="Please say the sentence: A for Apple", font=('Arial', 14))
        self.message_label.pack(expand=True, fill=tk.BOTH)
        
        self.processed_info_label = tk.Label(master, text="", font=('Arial', 12))
        self.processed_info_label.pack(expand=True, fill=tk.BOTH)
        
        self.gif_label = tk.Label(master)
        self.gif_label.pack(expand=True, fill=tk.BOTH)
        
        self.emoji_label = tk.Label(master, font=('Arial', 36))
        self.emoji_label.pack(expand=True, fill=tk.BOTH)
        
        # Add a label to display the number of chocolates achieved
        self.chocolates_label = tk.Label(master, text=f"Chocolates: {self.chocolates} 🍫", font=('Arial', 14))
        self.chocolates_label.pack(expand=True, fill=tk.BOTH)
        
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        
        self.master.bind('<Button-1>', self.next_sentence)
    
    def next_sentence(self, event):
        current_sentence = self.sentences[self.index]
        self.engine.say(f"Please say the sentence: {current_sentence}")
        self.engine.runAndWait()
        
        with sr.Microphone() as source:
            self.message_label.config(text="Listening...")
            self.master.update()  # Update the GUI to show "Listening..."
            audio = self.recognizer.listen(source)
            
        try:
            self.message_label.config(text="Listening completed")
            self.master.update()  # Update the GUI to show "Listening completed"
            user_input = self.recognizer.recognize_google(audio)
            print(user_input)
            self.processed_info_label.config(text=f"Processed Info is : {user_input}")
            self.master.update()

            # Check if the user input matches the current sentence
            user_input = user_input.upper()
            if current_sentence.upper() == user_input:
                self.engine.say("Hurray! Great Job, You have achieved a chocolate.")
                self.engine.runAndWait()
                self.chocolates += 1
                self.badges[self.index] += 1  # Increment badge count for the current sentence
                if self.badges[self.index] % 3 == 0:  # Check if three badges have been earned
                    self.engine.say("Congratulations! You earned a chocolate for completing three badges.")
                    self.engine.runAndWait()
                    self.chocolates += 1
                self.index = (self.index + 1) % len(self.sentences)
                self.attempted_once = False  # Reset the attempt flag
                self.update_emoji("✅")  # Display a checkmark emoji
                self.master.after(2000, self.reset_emoji)  # Reset emoji after 2 seconds
                self.show_success_gif()
            elif not self.attempted_once:
                self.engine.say("No problem, try again.")
                self.engine.runAndWait()
                self.attempted_once = True  # Set the attempt flag
                self.update_emoji("❌")  # Display a cross mark emoji
                self.master.after(2000, self.reset_emoji)  # Reset emoji after 2 seconds
            else:
                self.engine.say("I guess you are not focused. Try other games and come back later.")
                self.engine.runAndWait()
                self.master.quit()  # Quit the game
                self.update_emoji("❌")  # Display a cross mark emoji
                self.master.after(2000, self.reset_emoji)  # Reset emoji after 2 seconds
            
            # Update the sentence label and prompt for the next sentence
            next_sentence = self.sentences[self.index]
            self.sentence_label.config(text=next_sentence)
            self.message_label.config(text=f"Please say the sentence: {next_sentence}")
            
            # Update the chocolates label with the new count
            self.chocolates_label.config(text=f"Chocolates: {self.chocolates} 🍫")
                
        except sr.UnknownValueError:
            self.message_label.config(text="Sorry, I could not understand your audio.")
            self.update_emoji("❌")  # Display a cross mark emoji
            self.master.after(2000, self.reset_emoji)  # Reset emoji after 2 seconds
        except sr.RequestError as e:
            self.message_label.config(text=f"Error: {e}")
            self.update_emoji("❌")  # Display a cross mark emoji
            self.master.after(2000, self.reset_emoji)  # Reset emoji after 2 seconds

    def update_emoji(self, emoji):
        self.emoji_label.config(text=emoji)
        
    def reset_emoji(self):
        self.emoji_label.config(text="")
        
    def show_success_gif(self):
        # Change the path here
        success_gif_path = r"C:\Users\premk\Downloads\lol.gif" 
        success_gif = Image.open(success_gif_path)
        success_gif = success_gif.resize((150, 150))
        self.success_gif_tk = ImageTk.PhotoImage(success_gif)  # Keep a reference to the image
        self.gif_label.config(image=self.success_gif_tk)
        
        # Schedule a function to reset the GIF label after 3 seconds (3000 milliseconds)
        self.master.after(3000, self.reset_gif_label)

    def reset_gif_label(self):
        # Reset the GIF label to an empty image
        self.gif_label.config(image='')
        
def main():
    root = tk.Tk()
    root.title("Sentence Display")
    root.geometry("400x500")  # Increased height to accommodate chocolates label
    
    app = AlphabetApp(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
