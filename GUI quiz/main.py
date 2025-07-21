import json
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk
from ttkbootstrap.constants import *
import ttkbootstrap as tb
import random
import csv
import os.path

#global variables for name and score...
NAME = ''
SCORE = ''


class QuizLogic:

    """
    QuizLogics will handle the logical side of the program
    """

    # initialised with variables that needed for this class
    def __init__(self,data_file):
        self.questions = load_json(data_file) # load json data file and store in question variable...

        random.shuffle(self.questions) #shuffle the question order...
        
        # score and question number is set to 0 when the quiz is started...
        self.score = 0
        self.question_number = 0

    def load_current_question(self):
        if self.question_number < len(self.questions):
            # this will return the question with the question number index...
            return self.questions[self.question_number]
        else:
            return None
    
    def check_answer(self,selected_answer):
        # asigning answer to correct answer...
        correct_answer = self.questions[self.question_number]['answer']
        # if correct it will be true otherwise it will be false...
        is_correct = selected_answer == correct_answer
        
        self.question_number += 1
        if is_correct:
            self.score += 1
        return is_correct

    def check_quiz_finish(self):
        # check if the question data is ending, if it ends this will end the quiz program.
        return self.question_number>= len(self.questions)
    
    def get_score(self):
        # this function return the score value to show the score in GUI
        return self.score
    

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

        self.progress_bar = tb.Progressbar(self.master,bootstyle="success", maximum= 26, length=150, value=1)
        self.progress_bar.pack()

        self.leaderboard_btn = tb.Button(self.master, text="leaderboard",bootstyle = "primary , outline", command = self.show_leaderboard)

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
            self.leaderboard_btn.pack(pady=10)
            global SCORE
            SCORE = self.quiz_logic.get_score()
            store(NAME,SCORE)
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

    def show_leaderboard(self):
        score_window = tk.Toplevel()
        score_window.geometry('700x600')
        leaderboard(score_window)


'''Function to load question data'''
def load_json(questions):
    try:
        with open(questions,'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("The data file is not found!")
        return []
    

# for checking if the file exist...
def get_file_path(data_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(script_dir,data_file)

    return file_path

def is_file(data_file):
    file_path = get_file_path(data_file)
    file_exist = os.path.exists(file_path)
    return file_exist

def store(name, score):
    file_path = is_file('scoreBoard.csv')

    if file_path:
        with open('scoreBoard.csv','a', newline="") as file:
            fieldnames = ['first_name','score']
            csvwriter = csv.DictWriter(file, fieldnames=fieldnames)
            csvwriter.writerow({"first_name":name, "score": score})

    else:
        with open('scoreBoard.csv','a', newline="") as file:
            fieldnames = ['first_name','score']
            csvwriter = csv.DictWriter(file, fieldnames=fieldnames)
            csvwriter.writeheader()
            csvwriter.writerow({"first_name":name, "score": score})


class leaderboard:
    def __init__(self, master):
        self.master = master
        self.master.title("leaderboard")

        self.leaderboard_label = tk.Label(self.master,text="leaderboard",font=('consolas',12,'bold'), justify="center").pack()

        file_path = get_file_path('scoreBoard.csv')
        file = open(file_path)
        csvreader = csv.reader(file)
        l1 = []
        l1 = next(csvreader)
        r_set = [row for row in csvreader]


        trv = ttk.Treeview(self.master,selectmode='browse')
        trv.pack()
        
        trv['height'] = 5
        trv['show'] = 'headings'
        trv['column'] = l1

        for i in l1:
            trv.column(i, width=100,anchor='c')
            trv.heading(i, text=i)

        for dt in r_set:
            v=[r for r in dt]
            trv.insert('','end',iid=v[0],values=v)



class start_window:
    def __init__(self, master):
        self.master = master
        self.master.title("Welcome to Quiz")

        self.welcome_label = tk.Label(self.master,text="welcome to Quiz",font=("consolas",12,"bold"))
        self.welcome_label.pack(pady=40, padx=10)

        self.name_label = tk.Label(self.master, text="Enter your name please:", font=("consolas",10)).pack()
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

            global NAME
            NAME = name
            
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