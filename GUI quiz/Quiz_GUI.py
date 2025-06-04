import tkinter as tk
from Quiz_logics import QuizLogic
import tkinter.messagebox as mb
from ttkbootstrap.constants import *
import ttkbootstrap as tb



class Quiz_GUI:

    '''
    GUI class to handle make this program into an app
    '''
    def __init__(self, master, quiz_logic):
        self.master = master
        self.master.title("Quiz")

        self.quiz_logic = quiz_logic

        self.question_label = tk.Label(self.master,text="",wraplength=400, justify="center",font=("consolas", 12,"bold") )
        self.question_label.pack(pady=20)

        self.option_frame = tk.Frame(self.master)
        self.option_frame.pack(pady=20)

        self.var = tk.StringVar(value=-1) # value = -1 changed the selected button from the start of the program...

        self.option = []
        for i in range(4):
            btn = tk.Radiobutton(self.option_frame,text="", variable=self.var,value=str(i), font=("consolas",11, "bold"))
            btn.pack()
            self.option.append(btn)

        self.nextBtn = tb.Button(self.master,text="Next",bootstyle="primary , outline",command=self.next_question)
        self.nextBtn.pack(pady=10)

        self.feedback = tk.Label(self.master, text="",font=("consolas", 12, "bold"))
        self.feedback.pack()

        self.score_frame = tk.Frame(self.master)
        self.score_frame.pack(anchor="center")
        self.score_label = tk.Label(self.score_frame,text="score: ")
        self.score_label.pack(side="left", pady=20)

        self.score_number = tk.Label(self.score_frame, text="0")
        self.score_number.pack(side="left", pady=20)

        self.progress_bar = tb.Progressbar(bootstyle="success", maximum=26, length=150, value=1)
        self.progress_bar.pack()

        self.load_question()

    def next_question(self):
        selected_option = int(self.var.get())
        
        is_correct = self.quiz_logic.check_answer(selected_option)

        if is_correct:
            self.show_feedback("correct!","green")
        else:
            self.show_feedback("incorrect!","red")

        self.score_number.config(text=str(self.quiz_logic.get_score()))
        self.var.set(-1)
        self.progress_bar['value']+= 1
            
        if self.quiz_logic.check_quiz_finish():
            self.question_label.config(text="Quiz Completed!")
            self.option_frame.pack_forget()
            self.nextBtn.config(state="disabled")
            mb.showinfo("Quiz Completed", f"Your total score is: {self.quiz_logic.get_score()}")
        else:
            self.load_question()

    def load_question(self):
        question = self.quiz_logic.load_current_question()
        self.question_label.config(text=question['question'])

        for i, option in enumerate(question['options']):
            if i < len(self.option):
                self.option[i].config(text=option, value=i)
            else:
                btn = tk.Radiobutton(self.option_frame, text=option, variable=self.var, value=str(i))
                btn.pack()
                self.option.append(btn)

    def show_feedback(self,feedback, colour):
        self.feedback.config(text=feedback, foreground=colour)

        self.master.after(1500,lambda:self.feedback.config(text=""))


if __name__ == "__main__":
    quiz_logic = QuizLogic('question_data.json')

    if not quiz_logic.questions:
        print("No questions available, exiting...")
    else:
        root = tb.Window(themename="solar")
        root.geometry('700x600')
        app = Quiz_GUI(root, quiz_logic)
        root.minsize(600,500)
        root.mainloop()