import tkinter as tk
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from Quiz_GUI import Quiz_GUI
from Quiz_logics import QuizLogic
import tkinter.messagebox as mb

class start_window:
    def __init__(self, master):
        self.master = master
        self.master.title("Welcome to Quiz")

        self.welcome_label = tk.Label(self.master,text="welcome to Quiz",font=("consolas",12,"bold"))
        self.welcome_label.pack(pady=40, padx=10)

        self.entry_name = tk.Entry(self.master)
        self.entry_name.pack()

        self.name_error = tk.Label(self.master,text="Please enter you name!")
        self.name_error.pack_forget() # don't show at first...

        self.startbtn = tb.Button(self.master,text="Start",bootstyle="primary , outline",command=self.start_quiz)
        self.startbtn.pack(pady=10,padx=10)

    def check_entry(self):
        name = self.entry_name.get().strip() # get the name without spaces or tabs...
        if name:
            self.name_error.pack_forget() # Hide error label...
            return name
        else:
            self.name_error.pack() # show error message...
        
    def start_quiz(self):
        userName = self.check_entry()
        if not userName:
            return
        
        quiz_logic = QuizLogic('question_data.json')
        if not quiz_logic.questions:
            mb.showerror("Error","No question available")
            return
        
        self.master.withdraw()

        quiz_window = tk.Toplevel()
        quiz_window.geometry('700x600')
        Quiz_GUI(quiz_window,quiz_logic)



if __name__ == "__main__":
    root = tb.Window(themename="solar")
    root.geometry('700x600')
    app = start_window(root)
    root.minsize(600,500)
    root.mainloop()