# StudentID:	p2104005
# Name:	        Lee Quan Jun Ervin
# Class:		DISM/FT/1B/05
# Assessment:	CA2
#
# Script name:	user.py
#
# Purpose:      Users can take part in a multiple choice quiz with set attempts
#
# Usage syntax:	python ./Code/user.py
#
# Data Files: Code\userid_pswd.txt
#             Code\question_pool.txt
#             Code\quiz_settings.txt
#             Code\quiz_results.txt
#             Code\quiz_report.csv
#
# Python ver:	Python 3
#
# References:
# https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007 (ANSI Color Code Class)
#
# Modules: os, statistics, re, pickle, socket, sys, time, prettytable, textwrap, getpass, json, random

# Imports
import os                       # For clearing terminal for cleaner look :D
import random                   # For randomizing questions
import socket                   # To connect the client program to the server program
import time                     # For time limit for quiz
from datetime import date       # For getting date of attempt and time sleeping
import re                       # For regex password check
import sys                      # For exiting program
import pickle                   # For sending and receiving sockets
import getpass                  # Hides password input

# ============================================================================
# SOCKET PROGRAMMING
# ============================================================================
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 8000
try:
    client_socket.connect((host, port))
except:
    print("[ERROR] Connection Error!")
    sys.exit()

# Class of text color codes
global Colors
class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"


# Declaration of Quiz Result Dictionary
global user_report
user_report = {}    # Result that will be written to quiz_results.txt with all details regarding past attempt

# Outputs Title ASCII Art
print(Colors.BLUE + '''
 ██████  ██    ██ ██ ███████      █████  ██████  ██████  ██      ██  ██████  █████  ████████ ██  ██████  ███    ██ 
██    ██ ██    ██ ██    ███      ██   ██ ██   ██ ██   ██ ██      ██ ██      ██   ██    ██    ██ ██    ██ ████   ██ 
██    ██ ██    ██ ██   ███       ███████ ██████  ██████  ██      ██ ██      ███████    ██    ██ ██    ██ ██ ██  ██ 
██ ▄▄ ██ ██    ██ ██  ███        ██   ██ ██      ██      ██      ██ ██      ██   ██    ██    ██ ██    ██ ██  ██ ██ 
 ██████   ██████  ██ ███████     ██   ██ ██      ██      ███████ ██  ██████ ██   ██    ██    ██  ██████  ██   ████ 
    ▀▀                                                                                                    
''' + Colors.END)



# ============================================================================
# FUNCTION DECLARATIONS
# ============================================================================

# Encryption password function (Basic Caesar Cipher shifting by 3 ASCII Values)
global encrypt
def encrypt(pwd):
    pwd = pwd.strip()
    new_pwd = ''
    for char in pwd:
        value = ord(char)
        new_pwd += chr(value + 3)   
    return new_pwd


# Decryption password function (Reverse Process)
global decrypt
def decrypt(pwd):
    new_pwd = ''
    for char in pwd:
        value = ord(char)
        new_pwd += chr(value - 3)   # Shift ASCII values down by three
    return new_pwd


# Password Check Function
global check_password
def check_password(password):
    # using regex to verify password requirements
    pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{5,12}$"
    regex = re.compile(pattern)
    if re.search(regex, password):
        return True
    else:
        return False

def view_results(userID, results_list):
    user_result = []
    for result in results_list:
        if result["UserID"] == userID:
            user_result.append(result)
    return user_result

# Function to add user
def add_user():
    print(Colors.BLUE + "[ADD USER]")
    # Check if username is blank or username already exists
    while True:
        print(Colors.NEGATIVE + "Enter [e] to exit" + Colors.BLUE)
        username = input("Enter username: ")
        print("Sending new username to server for verification...")
        if len(username) != 0:  # Validates blank inputs
            if username.isalnum():
                client_socket.sendall(("check_username-" + username).encode("utf8"))
                verification = client_socket.recv(5120).decode("utf8")  # Checks if username already exists in the userid_pswd.txt file
                if verification == "False":
                    break
                else:
                    print("Username already exists!")
            else:
                print("Your username cannot contain any special characters!")
        else:
            print("Your username cannot be blank!")
    
    # Skips entire process if exit input [e] is not entered
    if username != "e": 
        print("\nPassword Requirements:")
        print("- Include at least one uppercase and lowercase letter")
        print("- At least one special character (!, @, #, $, %, &)")
        print("- At least one number")
        print("- Should be between 5-12 characters long")

        while True:
            # Enter a new password
            new_password = getpass.getpass("Enter your password: ")
            # Require verification of password via re-entering when password requirements met
            if check_password(new_password) == True:
                re_enter_password = getpass.getpass("Re-enter your password: ")
                # Repeats prompt if re-enter password not the same
                while re_enter_password != new_password:
                    print("Password does not match! Enter again!")
                    re_enter_password = getpass.getpass("Re-enter your password: ")
                
                # Encrypts password to be written to userid_pswd.txt
                encrypted_password = encrypt(new_password)

                # Outputs the new user created
                print(f"New user {username} with password {new_password} has been successfully added!")
                input(Colors.NEGATIVE + "Press ENTER to continue..." + Colors.END)
                break
            else:
                # Outputs when password does not meet requirements
                print("Password does not meet the requirements!")
        
        # Joins list into a string with comma separators to write to the userid_pswd.txt
        id_string = ",".join(["U", username, encrypted_password])

        # Append string to the end of userid_pswd file
        client_socket.sendall(("adduser§" + id_string).encode("utf8"))

# Change Password Function
def change_password(username):
    new_user_list = []

    # Prints password requirements
    print("\nPassword Requirements:")
    print("- Include at least one uppercase and lowercase letter")
    print("- At least one special character")
    print("- At least one number")
    print("- Should be between 8-24 characters long")
    while True:
        # Password Validations
        new_password = getpass.getpass("Enter your password: ")
        if check_password(new_password) == True:
            re_enter_password = getpass.getpass("Re-enter your password: ")
            while re_enter_password != new_password:
                print("Password does not match! Enter again!")
                re_enter_password = getpass.getpass("Re-enter your password: ")
            encrypted_password = encrypt(new_password)
            print("Password succesfully changed!")
            input(Colors.NEGATIVE + "Press ENTER to continue..." + Colors.END)
            break
        else:
            print("Password does not meet the requirements!")

    client_socket.sendall("get_user_list".encode("utf8"))
    received_list = client_socket.recv(5120)
    user_list = pickle.loads(received_list)

    # Updates password by splitting user details into a list and finds username to reassign password to
    for user in user_list:
        id_list = user.split(",")
        # Finds the username the password belongs to and updates it
        if username == id_list[1]:
            id_list[2] = encrypted_password + "\n"
        new_list = ",".join(id_list)    # joins list into string with comma separators
        new_user_list.append(new_list)  # appends to new list to be rewritten to file

    client_socket.sendall(("update_user_list-" + str(new_user_list)).encode("utf8"))

# Extract Settings from quiz_settings.txt file
global get_settings
def get_settings(socket):
    global settings_dictionary
    settings_dictionary = {}
    print("Loading settings from server database...")
    socket.sendall("get_settings".encode("utf8"))
    received_list = socket.recv(5120)
    settings_list = pickle.loads(received_list)
    for setting in settings_list:
        setting = setting.strip()   # Strips strings of newlines
        split_settings = setting.split(":") # Settings are separated by colons, splits then into a list
        settings_dictionary[split_settings[0]] = split_settings[1]  # Reassigns settings into key-value pairs in dictionary

# Function to output quetion and answer choices in the quiz
global output_question
def output_question(number, dictionary, choice_list):
    print(f"Question {number + 1}:")
    print(f"{Colors.YELLOW}{dictionary['Question']}{Colors.BLUE}")
    print(f"(a) {dictionary[choice_list[0]]}")
    print(f"(b) {dictionary[choice_list[1]]}")
    print(f"(c) {dictionary[choice_list[2]]}")
    print(f"(d) {dictionary[choice_list[3]]}")



# ============================================================================
# QUIZ APPLICATION LOGIC
# ============================================================================
def main_quiz(name):
    # Function to read settings and store them into a dictionary to use later on
    get_settings(client_socket)
    # Function to output a summary page to show all questions and inputted answers for the quiz attempt
    def show_summary(tested_questions, unanswered_questions):
        print("[QUIZ SUMMARY]")
        for i, question in enumerate(tested_questions):
            output_question(i, question, options_list)
            print(f"Answer: {question['InputAnswer']}\n")
        if len(unanswered_questions) > 0:
            print(f"Unanswered Questions: {unanswered_questions}")
    
    # Configuring Settings
    attempts = int(settings_dictionary["Attempts"])     # Reading number of attempts for user to do
    duration = int(settings_dictionary["Duration"])     # Reading the time limit for user attempt
    quiz_name = settings_dictionary["QuizTested"]        # Extracts the set quiz to test the users 

    user_report["QuizName"] = quiz_name

    def total_marks(dictionary):    # Function to add total marks the quiz is out of
        marks = 0
        for question in dictionary:
            marks += question["Marks"]
        return marks

    # Function to print results for user once they have used up one attempt
    def display_results(dictionary, max_marks):
        print("[QUIZ RESULTS]")
        mark_list = list(dictionary.values())
        total = sum(mark_list)
        global percentage   # Calculates the percentage out of total marks user scored
        percentage = round((total/max_marks)*100, 3)
        print(f"You scored {Colors.BOLD + str(total) + Colors.BLUE} out of {max_marks} marks ({percentage}%)")  # Displays user's raw score

        # Messages to output when user scores a certain amount
        if percentage >= 80:
            print(Colors.GREEN + "Good. Well Done!!!" + Colors.END)
        elif 50 <= percentage <= 79:
            print(Colors.YELLOW + "Fair. You can definitely do better with more effort!!!" + Colors.END)
        else:
            print(Colors.LIGHT_RED + "Poor. You need to work harder..." + Colors.END)

    # Lists for all questions, answers and correct answers for every attempt taken
    # Takes the attempt with the highest mark to be exported to quiz result files
    total_marks_list = []
    overall_answer_list = []
    overall_question_list = []
    overall_correct_answers = []

    # Search for quiz in quizzes.txt
    tested_quiz = None
    client_socket.sendall("extract_quizzes".encode("utf8"))
    received_list = client_socket.recv(5120)
    quiz_list = pickle.loads(received_list)

    for quiz in quiz_list:
        if quiz["QuizName"] == quiz_name:
            tested_quiz = quiz
            break

    if tested_quiz == None:
        print("This quiz does not exist! Perhaps it was deleted somehow? Make sure the admins have set a quiz that actually exists bruh...")
        input("Press [ENTER] to continue...")

    else:
        # Repeat Quiz for a limited number of attempts
        for i in range(attempts):
            # Calculate total number of questions in quiz
            total_questions = 0
            for topic in tested_quiz["Topics"]:
                count = 0
                if topic[0] == 0:
                    for question in tested_quiz["Questions"]:
                        if topic[1] == question["TestedTopic"]:
                            total_questions += 1
                else:
                    total_questions += topic[0]
            # Contruct a dictionary of marks to allocate marks for each question answered
            marks_dictionary = {}
            for j in range(1, total_questions + 1):    # For loop iterates depending on how many questions tested set by admins
                marks_dictionary[j] = 0

            options_list = ["A", "B", "C", "D"]
    
            # Limits the number of questions to test for each topic
            questions_tested_list = []
            for topic in tested_quiz["Topics"]:
                if topic[0] != 0:
                    count = 0
                    limit = topic[0]
                    for question in tested_quiz["Questions"]:
                        if topic[1] == question["TestedTopic"]:
                            questions_tested_list.append(question)
                            count += 1
                        if count == limit:
                            break
                elif topic[0] == 0:
                    for question in tested_quiz["Questions"]:
                        if topic[1] == question["TestedTopic"]:
                            questions_tested_list.append(question)

            # Check Toggle Settings
            # Shuffle Questions each attempt
            if settings_dictionary["RandomizeQuestion"] == "On":
                random.shuffle(questions_tested_list)

            unanswered_questions = []   #  list questions that were skipped and unanswered, removes if questions are answered later on
            output = ""     # What to output when terminal clears and prints menus again
            t1 = time.time()
            def check_time(t1):
                if settings_dictionary["TimeLimit"] == "On":
                    t2 = time.time()
                    global time_left
                    time_left = duration - ((t2 - t1)/60)
                    if time_left <= 0:
                        print(Colors.RED + "Your time is up, please enter your final answer." + Colors.END)
                    else:
                        print(f"You have {Colors.NEGATIVE + str(round(time_left, 2)) + Colors.BLUE} minutes left!")

            # Compiling the maximum marks the user can get in the quiz
            global max_marks
            max_marks = total_marks(questions_tested_list)

            topic_list = []
            for topic in tested_quiz["Topics"]:
                topic_list.append(topic[1])

            topic_string = ", ".join(topic_list)

            os.system("cls")
            # Pre Quiz Information for user
            print(f"""{Colors.BLUE}
            [QUIZ TIME]
            Welcome {Colors.LIGHT_WHITE + name + Colors.BLUE}, please choose your best answer for the questions.
            There are {Colors.LIGHT_WHITE + str(total_questions) + Colors.BLUE} questions in this quiz.
            Time Allowed: {Colors.LIGHT_WHITE + str(duration) + Colors.BLUE} minutes (0 minutes = Unlimited Time)
            Attempts Allowed: {Colors.LIGHT_WHITE + str(attempts) + Colors.BLUE}
            Total marks for this quiz: {Colors.LIGHT_WHITE + str(max_marks) + Colors.BLUE} marks
            Module: {Colors.LIGHT_WHITE + tested_quiz["Module"] + Colors.BLUE}
            Topics Tested: {Colors.LIGHT_WHITE + topic_string + Colors.BLUE}
            Today's date is {Colors.LIGHT_WHITE + today_date + Colors.BLUE}

            The best attempt will be taken. Do your best!
            """)
            input("Press ENTER to start the quiz...")
            os.system("cls")

            answers_list = []
            
            
            # Section where user can move back and forth questions
            count = 0
            while True:
                os.system("cls")
                print(output)
                question = questions_tested_list[count]     # Takes the question based on index from the question list
                output_question(count, question, options_list)  # Prints question for user to view
                print(f"Answer Entered: {question['InputAnswer']}")
                # Takes the current time subtracted by the start time to output the time left (Function only outputs if time limit is on)
                check_time(t1)
                print("Select from the question choices (a) to (d) to answer, enter [P] to go to previous question or [N] to go to next question ")
                option = input(">>> ")  # User option input
                option = option.upper() # Makes answer uppercase to prevent mixing of cases when checking answers

                # Answer Validation
                while option not in options_list and option not in ["P", "p", "N", "n"]:
                    check_time(t1)
                    print("Please select an appropriate option!")
                    print( "Select from the question choices (a) to (d) to answer, enter [P] to go to previous question or [N] to go to next question ")
                    option = input(">>> ")
                    option = option.upper()

                # Only output time's up message if the time limit is on
                if settings_dictionary["TimeLimit"] == "On":
                    if time_left <= 0:
                        print("Your time is up! You can no longer do this quiz!")
                        input(Colors.NEGATIVE + "Press ENTER to continue and view results." + Colors.END)
                        break   # Break out of the loop when time is up

                
                # If Statements for option
                if option == "P":   # Going to previous question
                    if count - 1 < 0:   # If count is negative, after subtracting 1, means first question cannot be skipped back
                        output = Colors.RED + "There is no previous question before the first question!" + Colors.END
                        continue        # Skip and repeat loop
                    else:
                        output = "" 
                        count -= 1      # If not, can subtract count and index goes down to previous question in list
                        continue
                elif option == "N": # Going to the next question
                    output = ""
                    count += 1      # Increases index by 1 to the next question in the list
                else:
                    output = ""
                    # Check if Answer matches Correct Answer and award marks, remove if answer changed is wrong.
                    question["InputAnswer"] = option
                    if question["InputAnswer"] == question["CorrectAnswer"]:
                        marks_dictionary[count+1] = question["Marks"]   # Allocates marks to the question key
                    elif question["InputAnswer"] != question["CorrectAnswer"] and marks_dictionary[count+1] == question["Marks"]:
                        marks_dictionary[count+1] = 0       # Removes marks from the question key if answer is changed and it is wrong
                
                # If answer is not selected, and the input answer value is blank, add question to list of unanswered questions
                if question["InputAnswer"] == "":
                    if count not in unanswered_questions:   # If question does not exist in unanswered questions list, append to the list
                        unanswered_questions.append(count)
                elif question["InputAnswer"] != "":
                    # If question is answered and exists in the unanswered questions list, remove it from the list
                    if (count+1) in unanswered_questions:
                        unanswered_questions.remove(count+1)

                # If question is answered without pressing next question, add 1 to count
                if not(option == "N" or option == "n"):
                    count += 1

                # If count is more than the number of questions tested, user has come to the end of the quiz and can view summary
                if count >= total_questions:
                    os.system("cls")
                    unanswered_questions.sort() # Sorts unanswered question numbers in sequence
                    # Prints summary of questions and answers with unanswered questions
                    show_summary(questions_tested_list, unanswered_questions)

                    # Prompt the user to jump to a certain question
                    while True:
                        # Validation (Range and Type Check)
                        try:
                            jump_question = int(input("Select a question to jump to or enter '0' to submit answers: "))
                            if jump_question not in range(total_questions+1):      # Range check
                                print("Please enter a number within the range of question numbers.")
                                continue
                            break
                        except ValueError:
                            print("Please enter a number, not a string.")
                            
                    if jump_question == 0:  # Break out of loop if user presses 0 to submit answers
                        break
                    else:
                        count = jump_question - 1

            # Display results to show user's performance
            os.system("cls")
            display_results(marks_dictionary, max_marks)

            # Compile answers for attempt
            for question in questions_tested_list:
                answers_list.append(question["InputAnswer"])
            overall_answer_list.append(answers_list)    # Append attempt answers into an overall answer list for choosing best attempt

            # Compile list of questions for attempt
            attempt_questions_list = []
            correct_answer_list  = []
            for question in questions_tested_list:
                attempt_questions_list.append(question["Question"])
                # Adds attempt correct asnwers to list of marks
                correct_answer_list.append(question["CorrectAnswer"])
            
            # Append set of questions to overall questions lists for all attempts 
            overall_question_list.append(attempt_questions_list)
            
            # Adds attempt mark to list of marks
            total_marks_list.append(percentage)

            # Adds set of correct answers for the attempt
            overall_correct_answers.append(correct_answer_list)

            # If attempts are all used up, break out of loop and return the user to the login page
            if i == (attempts - 1):
                print("You are out of attempts. Thank you for participating in this quiz. You will be brought back to the login screen")
                input(Colors.NEGATIVE + "Press ENTER to continue..." + Colors.END)
                break

            # If there are still attempts, show attempts left and user has a choice to continue attempts or stop the quiz
            else:
                print(f"You currently have {attempts - (i + 1)} attempts left. Do you want to continue? [y/n]")
                continue_option = input(">>> ")
                # Yes or No Validation
                while continue_option not in ["Y", "y", "N", "n"]:
                    print("Please select 'y' or 'n'")
                    continue_option = input(">>> ")

                # Break out of loop if user does not want to continue quiz attempts
                if continue_option == "N" or continue_option == "n":
                    print("Thank you for participating in this quiz")
                    input(Colors.NEGATIVE + "Press ENTER to continue..." + Colors.END)
                    break
            
        # When quiz is over, take the highest score with the questions and answers
        highest_index = total_marks_list.index(max(total_marks_list))
        chosen_questions = overall_question_list[highest_index]
        chosen_answers = overall_answer_list[highest_index]
        chosen_correct_answers = overall_correct_answers[highest_index]

        # Store all the questions, answers, correct answers, marks obtained and date into one report dictionary to be written to quiz_results.txt
        user_report["Module"] = tested_quiz["Module"]
        user_report["Topics"] = topic_list
        user_report["Questions"] = chosen_questions 
        user_report["Answers"] = chosen_answers
        user_report["CorrectAnswers"] = chosen_correct_answers
        user_report["Score"] = max(total_marks_list)
        user_report["AttemptDate"] = today_date
        
        # Writes result to quiz_results.txt
        client_socket.sendall(("append§quiz_results.txt§"+str(user_report)).encode("utf8"))

# ============================================================================
# MAIN LOGIN PAGE
# ============================================================================

# Function to print the login menu
def print_login():
    print(Colors.GREEN + "[QUIZ LOGIN]")
    print("[1] User Login")
    print("[2] Register")
    print("[3] Forgot Password?")
    print("[4] View Your Past Attempts")
    print("Press [e] to exit" + Colors.END)

# Login Logic
while True:
    print_login()
    login_option = input(Colors.YELLOW + "Select Option >>> " + Colors.END)
    global today_date
    today_date = date.today().strftime("%d/%m/%Y")

    # Login
    if login_option == "1":
        username = input("Enter username: ")    # Username input
        password = getpass.getpass("Enter Password: ")    # Password input
        userid = "login-" + username + "-" + password
        print("Sending to server to verify credentials...")
        client_socket.sendall(userid.encode("utf8"))
        time.sleep(2)
        verify = client_socket.recv(5120).decode("utf8")
        if verify == "False":     # If username or password does not match database, return to login menu
            print(Colors.RED + "Invalid Username or Password!" + Colors.END)
            input(Colors.NEGATIVE + "Press ENTER to go back to login page..." + Colors.END)
            os.system("cls")
            continue
        else:
            # Records username in user_report dictionary and quiz logic called
            message_to_send = "User " + username + " has successfully logged into the quiz!"
            client_socket.sendall(message_to_send.encode("utf8"))
            user_report["UserID"] = username
            os.system("cls")
            main_quiz(username)     # Main quiz logic called
        os.system("cls")

    # Register a new user
    elif login_option == "2":
        os.system("cls")
        add_user()  # Function to add a user
        os.system("cls")

    # Change Password
    elif login_option == "3":
        os.system("cls")
        print(Colors.YELLOW)
        print("[CHANGE PASSWORD]")
        print(Colors.NEGATIVE + "Enter [e] to exit." + Colors.END)
        while True:
            # Prompt user for username to change password for
            existing_username = input(Colors.YELLOW + "Enter an existing username: ")
            # Validates if username exists in the userid_pswd.txt file or not
            client_socket.sendall(("check_username-" + existing_username).encode("utf8"))
            verification = client_socket.recv(5120).decode("utf8")  # Checks if username already exists in the 
            if existing_username == "":
                print(Colors.RED + "Username cannot be blank!" + Colors.YELLOW)
            elif existing_username == "e" or existing_username == "E":
                break 
            elif verification == "False":
                print(Colors.RED + "This user does not exist" + Colors.YELLOW)
            else:
                break
        
        change_password(existing_username)

    elif login_option == "4":
        username = input("Enter username: ")    # Username input
        password = getpass.getpass("Enter Password: ")    # Password input
        userid = "login-" + username + "-" + password
        print("Sending to server to verify credentials...")
        client_socket.sendall(userid.encode("utf8"))
        time.sleep(2)
        verify = client_socket.recv(5120).decode("utf8")
        if verify == False:     # If username or password does not match database, return to login menu
            print(Colors.RED + "Invalid Username or Password!" + Colors.END)
            input(Colors.NEGATIVE +
                  "Press ENTER to go back to login page..." + Colors.END)
            os.system("cls")
            continue
        else:
            client_socket.send("extract_results".encode("utf8"))
            received_list = client_socket.recv(5120)
            results_list = pickle.loads(received_list)
            user_result_list = view_results(username, results_list)
            if len(user_result_list) == 0:
                print("There are no attempts by this user...")
                input("Press [ENTER] to continue...")
            else:
                os.system("cls")
                print(f"[PAST ATTEMPTS BY USER {username}]")
                for i, result in enumerate(user_result_list):
                    print(f"Attempt [{i+1}] {result['AttemptDate']}")
                
                while True:
                    try:
                        select_result = int(input("Select a result to view (Enter 0 to exit): "))
                        if select_result not in range(len(user_result_list)):
                            print("Out of range! Please enter only within the range!")
                            continue
                        break
                    except ValueError:
                        print("Please enter a valid number input.")
                        
                if select_result != 0:
                    selected_user = user_result_list[select_result-1]
                    questions = selected_user["Questions"]
                    answers = selected_user["Answers"]
                    correct_answers = selected_user["CorrectAnswers"]
                    os.system("cls")
                    print(f"[QUIZ REPORT FOR USER {selected_user['UserID']}]")
                    print(f"Date Attempted: {selected_user['AttemptDate']}")
                    print(f"Module: {selected_user['Module']}")
                    print(f"Topics Tested: {', '.join(selected_user['Topics'])}")
                    print(f"Number of Questions: {len(selected_user['Questions'])}")
                    print(f"{selected_user['UserID']} scored {selected_user['Score']}% for this quiz.\n")
                    for i, question, answer, correct_answer in zip(range(1, len(questions) + 1), questions, answers, correct_answers):
                        print(f"Question {i}: {question}")
                        print(f"Chosen Answer: {answer}")
                        print(f"Correct Answer: {correct_answer}\n")

                    input(Colors.NEGATIVE + "Press ENTER to exit report" + Colors.END)
                    os.system("cls")

    # Break out of the loop tro terminate the program if user enters [e] to quit application
    elif login_option == "e" or login_option == "E":
        client_socket.sendall("quit".encode("utf8"))
        break

    else:
        # Output invalid input message
        os.system("cls")
        print(Colors.RED + "Invalid Input!" + Colors.END)

print(Colors.NEGATIVE + "Goodbye! Hope to see you again! o7 o7 o7" + Colors.END)
