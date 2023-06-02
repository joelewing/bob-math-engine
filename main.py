import spacy
from spacy.util import compile_infix_regex
from sympy import symbols, Add, Mul, sqrt, simplify, factorial

nlp = spacy.load('en_core_web_sm')

# Add special case rule
special_case = [{"ORTH": "square root"}]
nlp.tokenizer.add_special_case("square root", special_case)

# Assume the user input is something like "What is 5.5 plus 3.2 plus 2.3? And also, what is 4.1 times 2.2 times 2.3? And what is the square root of 16.4? And what is 10.6 minus 7.7 minus 2.2? And what is 15.5 divided by 3.3 divided by 5.5?"
user_input = "What is 5.5 plus 3.2 plus 2.3 and what is the river Thames? And also, what is 4.1 times 2.2 times 2.3? And what is the square root of 16.4? And what is 10.6 minus 7.7 minus 2.2? And what is 15.5 divided by 3.3 divided by 5.5?"

# Tokenize the user input
doc = nlp(user_input)

# Initialize an empty list to store the sentences with results
sentences_with_results = []
unrelated_sentences = []

def remove_trailing_zeros(num):
    return str(num).rstrip('0').rstrip('.') if '.' in str(num) else num

# Function to format the result: remove trailing zeros after a decimal point
def format_result(result):
    if isinstance(result, float):
        return format(result, ".2f").rstrip('.').rstrip('0')
    else:
        return result

# Loop over the sentences in the user input
for sent in doc.sents:
    # Create a dictionary to store the numbers and operations in the current sentence
    current_expr = {"numbers": [], "operations": []}

    # Loop over the tokens in the current sentence
    for token in sent:
        if token.pos_ == "NUM" and token.text.replace('.', '', 1).isdigit():
            current_expr["numbers"].append(float(token.text))
        elif token.text in ["plus", "times", "minus", "divided", "square root", "+", "*", "-", "/", "factorial"]:
            current_expr["operations"].append(token.text)

    # Check if the current expression is valid (i.e., it contains at least one number and one operation)
    if current_expr["numbers"] and current_expr["operations"]:
        # Perform the operations in the current expression
        result = current_expr["numbers"][0]
        for i in range(len(current_expr["operations"])):
            operation = current_expr["operations"][i]
            if i + 1 < len(current_expr["numbers"]):
                num = current_expr["numbers"][i + 1]

                if operation == "plus":
                    result = simplify(Add(result, num))
                elif operation == "+":
                    result = simplify(Add(result, num))
                elif operation == "times":
                    result = simplify(Mul(result, num))
                elif operation == "*":
                    result = simplify(Mul(result, num))
                elif operation == "minus":
                    result = simplify(result - num)
                elif operation == "-":
                    result = simplify(result - num)    
                elif operation == "divided":
                    result = simplify(result / num)
                elif operation == "/":
                    result = simplify(result / num)
                elif operation == "/":
                    result = simplify(result / num)

        if "square root" in current_expr["operations"]:
            result = sqrt(result)

        # Append the result to the current sentence
        sentences_with_results.append("*" + str(sent.text) + "*" + f" The result is {remove_trailing_zeros(result)}.")
    else:
        # If the sentence does not contain a mathematical expression, add it to the list as is
        unrelated_sentences.append(str(sent.text))

# Join the sentences back together
output = " ".join(sentences_with_results)
output2 = " ".join(unrelated_sentences)

# Print the output
print(output)
print(output2)