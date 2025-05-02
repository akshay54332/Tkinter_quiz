import tkinter as tk
from Quiz_logics import QuizLogic
import tkinter.messagebox as mb



class Quiz_GUI:
    def __init__(self, master, quiz_logic):
        self.master = master
        self.master.title("Quiz")

        self.quiz_logic = quiz_logic

        self.question_label = tk.Label(self.master,text="",wraplength=400, justify="center")
        self.question_label.pack(pady=20)

        self.option_frame = tk.Frame(self.master)
        self.option_frame.pack(pady=20)

        self.var = tk.StringVar(value=-1)

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
        self.var.set(-1)
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


if __name__ == "__main__":
    quiz_logic = QuizLogic('question_data.json')

    if not quiz_logic.questions:
        print("No questions available, exiting...")
    else:
        root = tk.Tk()
        root.geometry('500x400')
        app = Quiz_GUI(root, quiz_logic)
        root.mainloop()