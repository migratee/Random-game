import random
import tkinter as tk
from tkinter import messagebox

class GuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🔢 Guess Game")
        self.root.geometry("500x600")
        self.root.configure(bg='#2c3e50')
        
        # Game variables
        self.secret = None
        self.lower, self.upper = 1, 100
        self.max_attempts = 7
        self.attempts = 0
        self.round_num = 1
        
        # UI Elements
        tk.Label(root, text="🎲 NUMBER GUESSING GAME 🎲", font=('Arial', 16, 'bold'), 
                bg='#2c3e50', fg='white').pack(pady=10)
        
        self.info = tk.Label(root, text="", font=('Arial', 12), bg='#2c3e50', fg='#f39c12')
        self.info.pack(pady=5)
        
        self.range_label = tk.Label(root, text="", font=('Arial', 11), bg='#2c3e50', fg='white')
        self.range_label.pack()
        
        self.attempt_label = tk.Label(root, text="", font=('Arial', 11), bg='#2c3e50', fg='white')
        self.attempt_label.pack()
        
        # Input area
        frame = tk.Frame(root, bg='#2c3e50')
        frame.pack(pady=20)
        
        tk.Label(frame, text="Your guess:", font=('Arial', 12), bg='#2c3e50', fg='white').pack(side=tk.LEFT)
        self.entry = tk.Entry(frame, font=('Arial', 14), width=10, justify='center')
        self.entry.pack(side=tk.LEFT, padx=10)
        self.entry.bind('<Return>', self.guess)
        
        # Buttons
        btn_frame = tk.Frame(root, bg='#2c3e50')
        btn_frame.pack(pady=10)
        
        self.guess_btn = tk.Button(btn_frame, text="🔍 GUESS", command=self.guess, 
                                   bg='#3498db', fg='white', font=('Arial', 11, 'bold'), width=10)
        self.guess_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🔄 NEW", command=self.reset_game, 
                 bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'), width=10).pack(side=tk.LEFT, padx=5)
        
        # Message area
        self.log = tk.Text(root, height=15, width=55, font=('Consolas', 10), 
                          bg='#ecf0f1', fg='#2c3e50', state=tk.DISABLED)
        self.log.pack(pady=10)
        
        # Progress bar (simple)
        self.progress = tk.Canvas(root, height=20, bg='#34495e', highlightthickness=0)
        self.progress.pack(fill=tk.X, padx=20, pady=5)
        self.progress_bar = self.progress.create_rectangle(0, 0, 0, 20, fill='#3498db')
        
        self.new_game()
    
    def add_msg(self, msg, color='black'):
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)
    
    def update_ui(self):
        remaining = self.max_attempts - self.attempts
        self.info.config(text=f"✨ ROUND {self.round_num} ✨")
        self.range_label.config(text=f"Range: {self.lower} - {self.upper}")
        self.attempt_label.config(text=f"Attempts left: {remaining}")
        
        # Update progress bar
        width = self.progress.winfo_width()
        if width > 0:
            percent = (self.attempts / self.max_attempts) * width
            self.progress.coords(self.progress_bar, 0, 0, percent, 20)
            color = '#f39c12' if remaining <= 2 else '#e74c3c' if remaining <= 4 else '#3498db'
            self.progress.itemconfig(self.progress_bar, fill=color)
    
    def new_game(self):
        self.secret = random.randint(self.lower, self.upper)
        self.attempts = 0
        self.entry.config(state=tk.NORMAL)
        self.guess_btn.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)
        self.entry.focus()
        
        self.log.config(state=tk.NORMAL)
        self.log.delete(1.0, tk.END)
        self.log.config(state=tk.DISABLED)
        
        self.add_msg("=" * 45, 'blue')
        self.add_msg(f"🎮 NEW ROUND {self.round_num}! 🎮", 'green')
        self.add_msg("=" * 45, 'blue')
        self.add_msg(f"Guess number between {self.lower} and {self.upper}")
        self.add_msg(f"You have {self.max_attempts} attempts!")
        self.add_msg("")
        
        self.update_ui()
    
    def guess(self, event=None):
        if self.attempts >= self.max_attempts:
            return
        
        # Get input
        text = self.entry.get().strip()
        if not text:
            self.add_msg("⚠️ Please enter a number!", 'orange')
            self.entry.delete(0, tk.END)
            return
        
        try:
            guess = int(text)
        except:
            self.add_msg(f"❌ '{text}' is not a number!", 'red')
            self.entry.delete(0, tk.END)
            return
        
        if guess < self.lower or guess > self.upper:
            self.add_msg(f"❌ Enter between {self.lower}-{self.upper}!", 'red')
            self.entry.delete(0, tk.END)
            return
        
        # Process guess
        self.attempts += 1
        remaining = self.max_attempts - self.attempts
        
        self.add_msg(f"Attempt #{self.attempts}: {guess}")
        
        if guess < self.secret:
            self.add_msg(f"📈 Too low! ({remaining} left)", 'orange')
        elif guess > self.secret:
            self.add_msg(f"📉 Too high! ({remaining} left)", 'orange')
        else:
            # WIN!
            self.add_msg("=" * 45, 'green')
            self.add_msg(f"🎉 CORRECT! 🎉", 'green')
            self.add_msg(f"✅ You won in {self.attempts} attempts!", 'green')
            self.add_msg("=" * 45, 'green')
            
            self.entry.config(state=tk.DISABLED)
            self.guess_btn.config(state=tk.DISABLED)
            
            if messagebox.askyesno("Victory!", f"Won Round {self.round_num}!\nNext round?"):
                self.next_round()
            else:
                self.show_stats()
            return
        
        # LOSS?
        if self.attempts >= self.max_attempts:
            self.add_msg("=" * 45, 'red')
            self.add_msg(f"❌ GAME OVER! ❌", 'red')
            self.add_msg(f"Number was: {self.secret}", 'red')
            self.add_msg("=" * 45, 'red')
            
            self.entry.config(state=tk.DISABLED)
            self.guess_btn.config(state=tk.DISABLED)
            
            if messagebox.askyesno("Game Over!", f"The number was {self.secret}\nPlay again?"):
                self.reset_game()
        
        self.update_ui()
        self.entry.delete(0, tk.END)
        self.entry.focus()
    
    def next_round(self):
        # Increase difficulty
        if self.round_num == 1:
            self.upper = 200
            self.max_attempts = 6
        elif self.round_num == 2:
            self.upper = 500
            self.max_attempts = 5
        elif self.round_num == 3:
            self.upper = 1000
            self.max_attempts = 4
        else:
            self.upper *= 2
            self.max_attempts = max(3, self.max_attempts - 1)
        
        self.round_num += 1
        self.add_msg(f"\n🔧 Difficulty up! Range: 1-{self.upper}, Attempts: {self.max_attempts}", 'orange')
        self.new_game()
    
    def reset_game(self):
        self.lower, self.upper = 1, 100
        self.max_attempts = 7
        self.round_num = 1
        self.new_game()
    
    def show_stats(self):
        self.add_msg("=" * 45, 'blue')
        self.add_msg(f"🏆 Completed {self.round_num - 1} rounds! Thanks for playing!", 'green')
        self.add_msg("👋 Goodbye!", 'blue')
        self.add_msg("=" * 45, 'blue')
        
        if messagebox.askyesno("Game Complete", f"You finished {self.round_num - 1} rounds!\nPlay again?"):
            self.reset_game()

# Run
if __name__ == "__main__":
    root = tk.Tk()
    game = GuessingGame(root)
    root.mainloop()