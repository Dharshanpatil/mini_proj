import tkinter as tk
import pyttsx3
import speech_recognition as sr
from PIL import Image, ImageTk
import inflect

class NumberApp:
    def __init__(self, master):
        self.master = master
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.number_words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        self.index = 0
        self.chocolates = 0
        self.badges = [0] * len(self.numbers)  # Initialize badges for each number
        self.attempted_once = False  # Flag to track if the kid has attempted once
        
        self.number_label = tk.Label(master, text=self.numbers[self.index], font=('Arial', 36))
        self.number_label.pack(expand=True, fill=tk.BOTH)
        
        self.message_label = tk.Label(master, text="Please say the number: zero", font=('Arial', 14))
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
        self.p = inflect.engine()
        
        self.master.bind('<Button-1>', self.next_number)
    
    def next_number(self, event):
        current_number = self.numbers[self.index]
        current_number_word = self.number_words[self.index]
        self.engine.say(f"Please say the number {current_number_word}")
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

            # Check if the user input contains the current number in words
            user_input = user_input.lower()
            if current_number_word in user_input or current_number == self.p.number_to_words(user_input):
                self.engine.say("Hurray! Great Job, You have achieved a chocolate.")
                self.engine.runAndWait()
                self.chocolates += 1
                self.badges[self.index] += 1  # Increment badge count for the current number
                if self.badges[self.index] % 3 == 0:  # Check if three badges have been earned
                    self.engine.say("Congratulations! You earned a chocolate for completing three badges.")
                    self.engine.runAndWait()
                    self.chocolates += 1
                self.index = (self.index + 1) % len(self.numbers)
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
            
            # Update the number label and prompt for the next number
            next_number = self.numbers[self.index]
            self.number_label.config(text=next_number)
            self.message_label.config(text=f"Please say the number: {self.number_words[self.index]}")
            
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
        success_gif_path = r"C:\Users\chand\Downloads\lol.gif"
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
    root.title("Number Display")
    root.geometry("400x450")  # Increased height to accommodate chocolates label
    
    app = NumberApp(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
