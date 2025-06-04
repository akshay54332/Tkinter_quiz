from loading_JSON_v2 import load_json # since I made this function i'm directly importing it...
import random

# This class is made to handle quiz logics like loading questions, tracking score etc...
class QuizLogic:

    """
    QuizLogics will handle the logical side of the program
    """

    # initialised with variables that needed for this class
    def __init__(self,data_file):
        self.questions = load_json(data_file) # load json data file and store in question variable...

        random.shuffle(self.questions) # shuffle the questions...
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
        # check the answer is correct and add score, question number plus 1
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