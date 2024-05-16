#!/usr/bin/python3
import random
import cgi

print("Content-Type: text/html\n")

form = cgi.FieldStorage()
first_name = form.getfirst("name", "")
studentno = form.getfirst("stdnumber","")

if form:
    try:
        with open('userinfo.txt', 'w') as user_file:
            user_file.write(f"Name: {first_name}\nStudent Number: {studentno}")
        print("<script>")
        print("if ('score' in localStorage) {")
        print("    localStorage.setItem('score', 0);")
        print("}")
        print("</script>")
    except OSError as e:
        print(f"Error writing to userinfo.txt: {e}")

# Read name and student number from userinfo.txt
name = ""
student_number = ""
try:
    with open('userinfo.txt', 'r') as user_file:
        lines = user_file.readlines()
        for line in lines:
            if line.startswith("Name:"):
                name = line.split(":")[1].strip()
            elif line.startswith("Student Number:"):
                student_number = line.split(":")[1].strip()
except OSError as e:
    print(f"Error reading from userinfo.txt: {e}")

class Question:
    def __init__(self, question, options, corr, numcorr):
        self.question = question
        self.options = options
        self.corr = corr
        self.numcorr = numcorr

# Function to read questions from file and create Question objects
def read_questions_from_file(file_path):
    questions = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        question = ''
        options = []
        numcorr = 0
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith('?'):
                if question:
                    if numcorr == 0:
                        options.append("None of the above")
                        corr = len(options)
                    elif numcorr > 1:
                        options.append("More than one of the above")
                        corr = len(options)
                    questions.append(Question(question, options, corr, numcorr))
                    options = []
                    numcorr = 0
                question = line[1:]
            elif line.startswith(('+')):
                options.append(line[1:])
                corr = len(options)
                numcorr += 1
            elif line.startswith(('-')):
                options.append(line[1:])
        
        # Append the last question after reading the file
        if question:
            questions.append(Question(question, options, corr, numcorr))
            if numcorr == 0:
                options.append("None of the above")
                corr = len(options)
                
            elif numcorr > 1:
                options.append("More than one of the above")
                corr = len(options)
    return questions

# Example usage:
file_path = 'questions.txt'
questions = read_questions_from_file(file_path)

def randomize():
    random_question = random.choice(questions)
    try:
        with open('val.txt', 'w') as val_file:
            val_file.write(str(random_question.corr))
    except OSError as e:
        print(f"Error writing to val.txt: {e}")
    return random_question

random_question = randomize()

print(""" <style>
        body {
            background-color: #00496d; /* Blue background */
            color: #000; /* Black text */
            font-family: Arial, sans-serif;
            text-align: center;
            align-items: center;
            display: flex;
            justify-content: center;
            flex-direction: column;
            padding: 20px;
        }

        h1 {
            color: #fff; /* White text */
            text-shadow: 2px 2px #000; /* Text shadow */
        }

        form {
            margin-top: 20px;
            background-color: #fff; /* White background */
            padding: 10px;
            border-radius: 10px; /* Rounded corners */
            box-shadow: 0px 0px 10px #888; /* Box shadow */
            width: 30%;
        }   

        label {
            display: block;
            margin-bottom: 10px;
            font-size: 18px;
        }

        input[type="text"] {
            width: 20%;
            padding: 10px;
            margin-bottom: 20px;
            border: 2px solid #00aaff; /* Blue border */
            border-radius: 5px; /* Rounded corners */
            font-size: 16px;
        }

        input[type="submit"] {
            width: 40%;
            padding: 10px;
            background-color: #00aaff; /* Blue button */
            border: none;
            border-radius: 5px; /* Rounded corners */
            color: #fff; /* White text */
            font-size: 18px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        input[type="submit"]:hover {
            background-color: #0077cc; /* Darker blue on hover */
        }
    </style>""")

print("<div style='float: right; padding: 20px; background-color: blue; color: white; border-radius: 10px;'>")
print("<p style='margin: 0;'>Name: {}</p>".format(name))
print("<p style='margin: 0;'>Student Number: {}</p>".format(student_number))
print("<p style='margin: 0;'>Score: <span id='score'>{}</span></p>")
print("</div>")
print("<p>Question: {}</p>".format(random_question.question))
for i in range(len(random_question.options)):
    print("<p style='color: black;'>{}: {}</p>".format(i+1,random_question.options[i]))

print("""<form action="/cgi-bin/COS332P6/val.py" method="get" style='margin-top: 20px;'>
    <input type="text" name="answer"><br>
    <input type="submit" value="Submit" style='background-color: blue; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;'>
    </form>""")
print("<script>")
print("var score = localStorage.getItem('score') || 0;")
print("document.getElementById('score').innerText = score;")
print("</script>")
