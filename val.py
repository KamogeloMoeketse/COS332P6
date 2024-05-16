#!/usr/bin/python3
import cgi


def get_correct_answer():
  # Read the correct answer from val.txt
  try:
    with open('val.txt', 'r') as val_file:
      correct_answer = int(val_file.read())
  except FileNotFoundError:
    print("Error: val.txt not found!")
    return None
  return correct_answer

def check_answer(user_answer):
  correct_answer = get_correct_answer()
  if correct_answer is None:
    return None
  try:
    user_answer = int(user_answer)
  except ValueError:
    return "Invalid answer format (use numbers)."
  if user_answer == correct_answer:
    return "Correct!"
  else:
    return "Incorrect. The correct answer is option {}".format(correct_answer)

form = cgi.FieldStorage()
user_answer = form.getvalue("answer")

result = check_answer(user_answer)
score_file = "score.txt"


def increase_score(filename):
    try:
        # Open the file in read mode to read the current score
        with open(filename, 'r') as file:
            current_score = int(file.read().strip())
    except FileNotFoundError:
        # If the file doesn't exist, start with score 0
        current_score = 0

    # Increase the score by one
    new_score = current_score + 1
    # print(new_score)

    # Write the new score back to the file
    try:
        with open('score.txt', 'w') as val_file:
            val_file.write(str(new_score))
    except OSError as e:
        print(f"Error writing to score.txt: {e}")


print("Content-Type: text/html\n")
if result is None:
  print("Error occurred. Please try again.")
elif result == "Correct!":
  score_filename = "score.txt"  # Update with your actual file path
  increase_score(score_filename)
  print("<script>")
  print("if ('score' in localStorage) {")
  print("    var score = parseInt(localStorage.getItem('score'));")
  print("    score++;")
  print("    localStorage.setItem('score', score);")
  print("} else {")
  print("    localStorage.setItem('score', 1);")
  print("}")
  print("</script>")
  print("<p>{}</p>".format(result))
else:
  print("<p>{}</p>".format(result))

print("""<form action="/cgi-bin/COS332P6/test.py" method="get">
    <input type="submit" value="Get another question">
</form>""")
print("""<form action="/cgi-bin/COS332P6/mail.py" method="get">
    <input type="submit" value="That's enough for me!">
</form>""")

print("""<style>
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

        form {
            margin-top: 20px;
        }

        input[type="submit"] {
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