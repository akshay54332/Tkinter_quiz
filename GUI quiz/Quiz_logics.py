from loading_JSON_v2 import load_json # since I made this function i'm directly importing it...

# This class is made to handle quiz logics like loading questions, tracking score etc...
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