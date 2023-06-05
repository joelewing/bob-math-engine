#bob-math-engine by Joel Ewing, Robert Appling

import spacy
import sympy
from spacy.util import compile_infix_regex
from sympy import symbols, Add, Mul, sqrt, simplify, factorial

nlp = spacy.load('en_core_web_sm')

# Add special case rule
special_case = [{"ORTH": "square root"}]
nlp.tokenizer.add_special_case("square root", special_case)

# Assume the user input is something like "What is 5.5 plus 3.2 plus 2.3? And also, what is 4.1 times 2.2 multiplied by 2.3? And what is the square root of 16.4? And what is 10.6 minus 7.7 minus 2.2? And what is 15.5 divided by 3.3 divided by 5.5? Additionally, what is 2 plus 4 times 3 factorial?"
user_input = "What is 5.5 plus 3.2 plus 2.3 and what is the river Thames? And also, what is 4.1 times 2.2 multiplied by 2.3? And what is the square root of 16.4? And what is 10.6 minus 7.7 minus 2.2? And what is 15.5 divided by 3.3 divided by 5.5? Additionally, what is 2 plus 4 times 3 factorial?"




def process_math_input(equation_string):
    # Tokenize the user input
    doc = nlp(equation_string)
    # Initialize an empty list to store the sentences with results
    paragraph = []

    def remove_trailing_zeros(num):
        return str(num).rstrip('0').rstrip('.') if '.' in str(num) else num

    # Loop over the sentences in the user input
    for sent in doc.sents:
        # Create a dictionary to store the numbers and operations in the current sentence
        current_expr = []
    # Loop over the tokens in the current sentence
        for token in sent:
            if token.pos_ == "NUM" and token.text.replace('.', '', 1).isdigit():
                current_expr.append(float(token.text))
                #added cast to lowercase to prevent capitalization issues
            elif token.text.lower() in ["plus", "times", "multiplied", "minus", "divided", "square root", "+", "*", "-", "/", "factorial", "!", "(", ")", "**", "^"]:
                current_expr.append(token.text)

        #exprString holds the expression read by the earlier loop
        exprString = ""
        for i in range(len(current_expr)):
            workVal = current_expr[i]
            if(isinstance(workVal,float)):
                exprString += str(workVal)
            elif workVal in ["+", "-", "/", "*", "(", ")", "!", "**"]:
                exprString += workVal
            elif workVal == "plus":
                exprString += "+"
            elif workVal == "minus":
                exprString += "-"
            elif workVal == "multiplied" or workVal == "times":
                exprString += "*"
            elif workVal == "divided":
                exprString += "/"
            elif workVal == "^":
                exprString += "**"
            elif workVal == "!" or workVal == "factorial":
                exprString += "!"

        #format for text output
        equationStr = "I read the equation as: " + exprString
        exprExpr = sympy.parse_expr(exprString)
        exprResult = sympy.simplify(exprExpr)
        answerStr = ". And I got an answer of: " + str(remove_trailing_zeros(round(exprResult, 3)) + ". \n" )
        paragraph.append(equationStr)
        paragraph.append(answerStr)
    answer = ''.join(paragraph)
    return answer

