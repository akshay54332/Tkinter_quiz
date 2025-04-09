import json
import tkinter as tk
import tkinter.messagebox as mb

class QuizLogic:

    # initialised with variables that needed for this class
    def __init__(self,data_file):
        self.questions = load_json(data_file) # load json data file and store in question variable...
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

        if selected_answer == correct_answer:
            self.score += 1
        self.question_number += 1

    def check_quiz_finish(self):
        return self.question_number>= len(self.questions)
    
    def get_score(self):
        return self.score
    

class Quiz_GUI:
    def __init__(self, master, quiz_logic):
        self.master = master
        self.master.title("Quiz")

        self.quiz_logic = quiz_logic

        self.question_label = tk.Label(self.master,text="",wraplength=400, justify="center")
        self.question_label.pack(pady=20)

        self.option_frame = tk.Frame(self.master)
        self.option_frame.pack(pady=20)

        self.var = tk.StringVar()

        self.option = []
        for i in range(4):
            btn = tk.Radiobutton(self.option_frame,text="", variable=self.var,value=str(i))
            btn.pack()
            self.option.append(btn)

        self.nextBtn = tk.Button(self.master,text="Next",command=self.next_question)
        self.nextBtn.pack(pady=10)

        self.score_frame = tk.Frame(self.master)
        self.score_frame.pack(anchor="center")
        self.score_label = tk.Label(self.score_frame,text="score: ")
        self.score_label.pack(side="left", pady=20)

        self.score_number = tk.Label(self.score_frame, text="0")
        self.score_number.pack(side="left", pady=20)

        self.load_question()

    def next_question(self):
        selected_option = int(self.var.get())
        self.quiz_logic.check_answer(selected_option)
        self.score_number.config(text=str(self.quiz_logic.get_score()))
            
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


def load_json(questions):
    try:
        with open(questions,'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("The data file is not found!")
        return []
    

if __name__ == "__main__":
    quiz_logic = QuizLogic('question_data.json')

    if not quiz_logic.questions:
        print("No questions available, exiting...")
    else:
        root = tk.Tk()
        root.geometry('500x400')
        app = Quiz_GUI(root, quiz_logic)
        root.mainloop()
        root.maxsize(600,400)