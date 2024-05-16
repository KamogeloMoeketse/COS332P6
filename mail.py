#!/usr/bin/env python3

import socket
import ssl
import base64
import cgi
import os
import http.cookies

print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>Email Form</title>")
print("</head>")
print("<body>")
print("<h2>Enter your email</h2>")
print("<form method='post' action=''>")
print("Email: <input type='text' name='email'>")
print("CC1: <input type='text' name='cc1'>")
print("CC2: <input type='text' name='cc2'>")
print("<input type='submit' name='submit' value='Send Email'>")
print("</form>")

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

# Get the value of a specific cookie
score_file = "score.txt"

def get_score_from_file():
    try:
        # Open the file in read mode to read the current score
        with open(score_file , 'r') as file:
            score = int(file.read().strip())
    except FileNotFoundError:
        # If the file doesn't exist, start with score 0
        score = 0
    # print(score)
    return score

score = get_score_from_file()



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

form = cgi.FieldStorage()
cc1 = ''
cc2 = ''

if "submit" in form:
    email = form.getvalue("email")
    cc1 = form.getvalue("cc1")
    cc2 = form.getvalue("cc2")
    if not email:
        print("<p style='color:red;'>Please enter your email!</p>")
    else:
        # Proceed with the rest of your code here
        # SMTP server settings
        smtp_server = 'localhost'
        smtp_port = 25

        # Email content
        sender_email = "hughjasscos332@gmail.com"
        receiver_email = email
        subject = "COS332 Test Results!"
        ccemails = ''
        if cc1 != None and cc2 != None:
            ccemails = "CC:" + cc1 + "," + cc2
        elif (cc1 != None and cc2 == None):
            ccemails = "CC:" + cc1
        elif (cc2 != None and cc1 == None):
            ccemails = "CC:" + cc2


        body = "Thank you for playing!\nName: " + name + '\nStudent number: ' + student_number + '\nScore:' + str(score)

        # Construct email message
        email_from = f"From: {sender_email}\r\n"
        email_to = f"To: {receiver_email}\r\n"
        email_cc = f"{ccemails}\r\n"
        email_subject = f"Subject: {subject}\r\n\r\n"
        email_body = f"{body}\r\n.\r\n"
        email_message = email_from + email_to + email_cc + email_subject + email_body

        try:
            # Connect to SMTP server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.connect((smtp_server, smtp_port))
                server_socket.recv(1024)  # Receive server greeting

                # Send HELO command
                server_socket.sendall(b"HELO kamogelo\r\n")
                response = server_socket.recv(1024)
                if not response.startswith(b'250'):
                    raise Exception(f"Unexpected response from server: {response.decode()}")

                # Send MAIL FROM command
                server_socket.sendall(f"MAIL FROM:<{sender_email}>\r\n".encode())
                response = server_socket.recv(1024)
                if not response.startswith(b'250'):
                    raise Exception(f"Unexpected response from server: {response.decode()}")

                # Send RCPT TO command
                server_socket.sendall(f"RCPT TO:<{receiver_email}>\r\n".encode())
                response = server_socket.recv(1024)
                if not response.startswith(b'250'):
                    raise Exception(f"Unexpected response from server: {response.decode()}")
                    

                if (cc1 != None):
                    server_socket.sendall(f"RCPT TO:<{cc1}>\r\n".encode())
                    response = server_socket.recv(1024)
                    if not response.startswith(b'250'):
                        raise Exception(f"Unexpected response from server: {response.decode()}")
                
                if (cc2 != None):
                    server_socket.sendall(f"RCPT TO:<{cc2}>\r\n".encode())
                    response = server_socket.recv(1024)
                    if not response.startswith(b'250'):
                        raise Exception(f"Unexpected response from server: {response.decode()}")

                # Send DATA command
                server_socket.sendall(b"DATA\r\n")
                response = server_socket.recv(1024)
                if not response.startswith(b'354'):
                    raise Exception(f"Unexpected response from server: {response.decode()}")

                # Send email content
                server_socket.sendall(email_message.encode())
                response = server_socket.recv(1024)
                if not response.startswith(b'250'):
                    raise Exception(f"Unexpected response from server: {response.decode()}")

                # Send QUIT command
                server_socket.sendall(b"QUIT\r\n")
                response = server_socket.recv(1024)
                if not response.startswith(b'221'):
                    raise Exception(f"Unexpected response from server: {response.decode()}")

            print("Email sent successfully")
            # print(f"<p>Email received: {email}</p>")
            try:
                with open('score.txt', 'w') as val_file:
                    val_file.write(str(0))
            except OSError as e:
                print(f"Error writing to score.txt: {e}")

            print("<meta http-equiv='refresh' content='3;url=/home.html'>")

        except Exception as e:
            print(f"Error sending email: {e}")
            print("<br><br><h3>Please try re-entering your email</h3>")

print("</body>")
print("</html>")
