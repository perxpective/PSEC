# StudentID:	p2104005
# Name:	        Lee Quan Jun Ervin
# Class:		DISM/FT/1B/05
# Assessment:	CA2
#
# Script name:	admin.py
#
# Purpose:	Administration Purposes - Editing Quiz Settings, View Past Attempt Records, Generate Report, Manage User Accounts in Quiz Application, Manage Modules and Topics and Quizzes.
#
# Note: DEFAULT ADMIN ACCOUNT: username: admin1, password: 1Qwer#@!
#
# Usage syntax:	python ./Code/admin.py
#
# Data Files: Code\userid_pswd.txt
#             Code\question_pool.txt
#             Code\quiz_settings.txt
#             Code\quiz_results.txt
#             Code\modules.txt
#             Code\quiz_report.csv
#             Code\quizzes.txt
#             
#
# Python ver:	Python 3
#
# References:
# https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007 (ANSI Color Code Class)
#
# Modules: os, statistics, re, pickle, socket, sys, time, prettytable, textwrap, getpass, json

# Imports
import os               # Clearing terminal
import pickle           # For sending and receiving
import statistics       # For displaying statistics for overall performance of users in quizzes
import re               # For regex password check
import socket           # To connect the client program to the server program
import sys              # For exiting the program
import time             # For time sleeping and displaying time
from prettytable import PrettyTable     # For displaying management report for quizzes
import textwrap         # For wrapping text for table column
import getpass          # Hides password input
import json             # Loads json string from prettytable

# Class for text colours
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

# Outputs Title ASCII Art
print(Colors.CYAN+
'''
 ██████  ██    ██ ██ ███████      █████  ██████  ██████  ██      ██  ██████  █████  ████████ ██  ██████  ███    ██ 
██    ██ ██    ██ ██    ███      ██   ██ ██   ██ ██   ██ ██      ██ ██      ██   ██    ██    ██ ██    ██ ████   ██ 
██    ██ ██    ██ ██   ███       ███████ ██████  ██████  ██      ██ ██      ███████    ██    ██ ██    ██ ██ ██  ██ 
██ ▄▄ ██ ██    ██ ██  ███        ██   ██ ██      ██      ██      ██ ██      ██   ██    ██    ██ ██    ██ ██  ██ ██ 
 ██████   ██████  ██ ███████     ██   ██ ██      ██      ███████ ██  ██████ ██   ██    ██    ██  ██████  ██   ████ 
    ▀▀                                                                                                    
'''
+ Colors.END)

# ============================================================================
# SOCKET PROGRAMMING
# ============================================================================
global client_socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'  
port = 8000         

try:
    client_socket.connect((host, port))     # Connect client to server
except:
    print("[ERROR] Connection Error!")      # If there is no connection, terminate the client program
    sys.exit()  # Termination if client is unable to connect to the 



# ===================================================================================
# FUNCTION DECLARATIONS
# ===================================================================================

# A very normal function!!! (Easter Egg won't affect the program)
def normal_function():
    os.system("cls")
    print("there is no secret here...")
    imput = input("go back pls press da enter key...")
    if imput == "doge":
        with open("./Data/quizfile.txt", "r", encoding='utf8') as file:
            dog = file.read()

        print(dog)
        print("dog says hi")
        input("frfr go back pls")
    

# Print Menu Function
def print_menu():   
    print(Colors.BLUE + """
    [ADMIN MENU]
    [1] Question Pool Settings
    [2] Module Settings
    [3] Manage User Accounts
    [4] View Results
    [5] Manage Quizzes
    Enter [e] to exit
    """ + Colors.END)

# Function to display question pool menu
def question_pool_menu():
    print('''
    ╔═╗ ╦ ╦╔═╗╔═╗╔╦╗╦╔═╗╔╗╔  ╔═╗╔═╗╔═╗╦  
    ║═╬╗║ ║║╣ ╚═╗ ║ ║║ ║║║║  ╠═╝║ ║║ ║║  
    ╚═╝╚╚═╝╚═╝╚═╝ ╩ ╩╚═╝╝╚╝  ╩  ╚═╝╚═╝╩═╝
    ''')

    print(Colors.PURPLE + """
    [QUESTION POOL MENU]
    [1] Add Question
    [2] Remove Question
    [3] Edit Question
    [4] Quiz Settings
    Enter [e] to exit to previous page
    """ + Colors.END)

# Function to display module menu
def module_menu():
    print("""
                               __            __                                                       
                              /  |          /  |                                                      
 _____  ____    ______    ____$$ | __    __ $$ |  ______   _____  ____    ______   _______   __    __ 
/     \/    \  /      \  /    $$ |/  |  /  |$$ | /      \ /     \/    \  /      \ /       \ /  |  /  |
$$$$$$ $$$$  |/$$$$$$  |/$$$$$$$ |$$ |  $$ |$$ |/$$$$$$  |$$$$$$ $$$$  |/$$$$$$  |$$$$$$$  |$$ |  $$ |
$$ | $$ | $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |$$    $$ |$$ | $$ | $$ |$$    $$ |$$ |  $$ |$$ |  $$ |
$$ | $$ | $$ |$$ \__$$ |$$ \__$$ |$$ \__$$ |$$ |$$$$$$$$/ $$ | $$ | $$ |$$$$$$$$/ $$ |  $$ |$$ \__$$ |
$$ | $$ | $$ |$$    $$/ $$    $$ |$$    $$/ $$ |$$       |$$ | $$ | $$ |$$       |$$ |  $$ |$$    $$/ 
$$/  $$/  $$/  $$$$$$/   $$$$$$$/  $$$$$$/  $$/  $$$$$$$/ $$/  $$/  $$/  $$$$$$$/ $$/   $$/  $$$$$$/  
    """)

    print(Colors.YELLOW + """
    [MODULE MENU]
    [1] Create a New Module
    [2] Edit an Existing Module
    [3] Remove a Module
    Enter [e] to exit to the previous page
    """ + Colors.END)


# Function to list modules
global list_modules
def list_modules(module_list):
    print("[LIST OF MODULES]")
    for i, module in enumerate(module_list):
        print(f"[{i+1}] {module['Module']}")

# Function to list topics under the selected module
def list_topics(module_list, selection):
    print(f"[LIST OF TOPICS IN MODULE {module_list[selection-1]['Module']}]")
    for i, topic in enumerate(module_list[selection-1]["TopicList"]):
        print(f"{i+1}. {topic}")

# Function to display quiz menu
def quiz_menu():
    print("""
     ██████╗ ██╗   ██╗██╗███████╗    ███╗   ███╗███████╗███╗   ██╗██╗   ██╗
    ██╔═══██╗██║   ██║██║╚══███╔╝    ████╗ ████║██╔════╝████╗  ██║██║   ██║
    ██║   ██║██║   ██║██║  ███╔╝     ██╔████╔██║█████╗  ██╔██╗ ██║██║   ██║
    ██║▄▄ ██║██║   ██║██║ ███╔╝      ██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║   ██║
    ╚██████╔╝╚██████╔╝██║███████╗    ██║ ╚═╝ ██║███████╗██║ ╚████║╚██████╔╝
    ╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝    ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ 
    """)
    print("""[QUIZ MENU]
    [1] Create a New Quiz
    [2] Manage Quizzes
    [3] Remove a Quiz
    Enter [e] to exit to the previous page
    """)

# Function to display create a new module
def new_module():
    module_dictionary = {}
    print("[CREATE A NEW MODULE]")
    module_name = input("Enter a name for your new module: ")
    while len(module_name) == 0:
        print("You cannot leave the module name blank!")
        module_name = input("Enter a name for your new module: ")
    
    topic_list = []
    while True:
        topic = input("Add topics to your modules (Enter [!] to skip this step): ")
        if len(topic) == 0:
            print("You cannot leave your topic blank!")
            continue
        elif topic == "!":
            if len(topic_list) < 2:
                print("You must have at least 2 topics in your module!")
                continue
            else:
                break
        else:
            print(f"You have successfully added the topic: {topic} to your module!")
            topic_list.append(topic)

    module_dictionary["Module"] = module_name
    module_dictionary["TopicList"] = topic_list

    print("Adding new module to server database...")
    time.sleep(1)
    client_socket.sendall(("append§modules.txt§"+str(module_dictionary)).encode("utf8"))

# Function to edit a module
def edit_module():
    # Extract list of modules from modules.txt
    client_socket.sendall("extract_modules".encode("utf8"))
    print("Extracting list of modules from server database...")
    time.sleep(1)
    received_list = client_socket.recv(5120)
    module_dictionary_list = pickle.loads(received_list)
    print("Modules received!")
    os.system("cls")
    if len(module_dictionary_list) == 0:
        print("Well, you don't have nothing... Maybe create a new module?")
        input("Press [ENTER] to continue...")
    
    else:
        list_modules(module_dictionary_list)

        while True:
            try:
                selection = int(input("Select a module to edit (Press 0 to exit): "))
                if selection not in range(len(module_dictionary_list) + 1):
                    print("Please select the modules in range.")
                    continue
                else:
                    break

            except ValueError:
                print("Please input a number.")
        
        os.system("cls")
        if selection != 0:
            selected_module = module_dictionary_list[selection-1]
            # Outputs module and the list of topics
            print("[EDIT MODULE]")
            print("Module Name: " + selected_module["Module"])
            print("Topics in this module: ")
            for i, topic in enumerate(selected_module["TopicList"]):
                print(f"{i+1}. {topic}")

            # Module options
            print("\n[1] Edit Module Name")
            print("[2] Add Topic")
            print("[3] Remove Topic")
            print("[4] Edit Topic")
            print("Enter 0 to exit.")
            
            # Get valid input option
            while True:
                try:
                    edit_option = int(input("Select option: "))
                    if edit_option not in range(5):
                        print("Please only enter an option number within the range above.")
                        continue
                    else: 
                        break
                except ValueError:
                    print("Please input a valid option number.")

            # Add new module name
            if edit_option == 1:
                new_module_name = input("Enter a new module name: ")
                while len(new_module_name) == 0:
                    print("You cannot leave your module name blank!")   # Blank validation
                    new_module_name = input("Enter a new module name: ")
                selected_module["Module"] = new_module_name
            
            # Add new topic name
            elif edit_option == 2:
                while True:
                    topic = input("Enter a name for your new topic (Enter ! to stop adding): ")
                    if len(topic) == 0:     
                        print("Don't leave your topic name blank!")
                        continue
                    if topic == "!":
                        break
                    else:
                        print(f"Added new topic {topic} to the module!")
                        selected_module["TopicList"].append(topic)

            # Remove a topic
            elif edit_option == 3:
                while True:
                    try:
                        remove_selection = int(input("Select a topic to remove (Enter 0 to cancel): "))
                        if remove_selection == 0:
                            break
                        elif remove_selection not in range(1, len(selected_module["TopicList"]) + 1):
                            print("Please only enter an option number within the range above.")
                            continue
                        else:
                            break

                    except ValueError:
                        print("Select a valid option.")

                selected_module["TopicList"].remove(selected_module["TopicList"][remove_selection-1])
            
            # Edit topic
            elif edit_option == 4:
                while True:
                    try:
                        edit_topic = int(input("Select a topic to edit (Enter 0 to cancel): "))
                        if edit_topic not in range(len(selected_module["TopicList"]) + 1):
                            print("Please only enter an option number within the range above.")
                            continue
                        else:
                            break
                    except ValueError:
                        print("Select a valid option.")

                if edit_topic != 0:
                        new_topic_name = input("Enter a new name for your topic: ")
                        while len(new_topic_name) == 0:
                            print("Don't leave your topic name blank!")
                            new_topic_name = input("Enter a new name for your topic: ")
                        selected_module["TopicList"][edit_topic-1] = new_topic_name
            
            module_dictionary_list[selection-1] = selected_module

        # Send updated modules to the server to write
        print("Saving module changes...")
        time.sleep(1)
        client_socket.sendall(("write_modules§" + str(module_dictionary_list)).encode("utf8"))

# Function to remove module
def remove_module():
    # Extract list of modules from the server
    client_socket.sendall("extract_modules".encode("utf8"))
    print("Extracting list of modules from server database...")
    time.sleep(1)
    received_list = client_socket.recv(5120)
    module_dictionary_list = pickle.loads(received_list)
    print("Modules received!")
    os.system("cls")
    list_modules(module_dictionary_list)
    
    # Get valid input option to remove a module
    while True:
        try:
            remove_index = int(input("Select a module to remove (Enter 0 to cancel): "))
            if remove_index not in range(len(module_dictionary_list) + 1):
                print("Please enter an option number within the given range.")
                continue
            else:
                break
        except ValueError:
            print("Enter a valid option number.")

    # Skip this step if input is 0 to stop removing module
    if remove_index != 0:
        module_dictionary_list.remove(module_dictionary_list[remove_index-1])
        
        # Sends changes to the server to update the database
        print("Saving module changes...")
        time.sleep(1)
        client_socket.sendall(("write_modules§" + str(module_dictionary_list)).encode("utf8"))
    
# Function to add a new quiz
def add_quiz():
    quiz_dictionary = {}
    quiz_name = input("Enter a name for your new quiz: ")
    quiz_dictionary["QuizName"] = quiz_name
    while len(quiz_name) == 0:
        print("You cannot leave your quiz name blank!")
    
    # Extract list of modules from modules.txt
    client_socket.sendall("extract_modules".encode("utf8"))
    print("Extracting list of modules from server database...")
    time.sleep(1)
    received_list = client_socket.recv(5120)
    module_dictionary_list = pickle.loads(received_list)
    print("Modules received!")

    os.system("cls")
    list_modules(module_dictionary_list)
    while True:
        try:
            module_choice = int(input("Select a module for the quiz: "))
            if module_choice not in range(1, len(module_dictionary_list) + 1):
                print("Please select within the given range.")
                continue
            else:
                break
        except ValueError:
            print("Please input a valid option.")
    
    selected_module = module_dictionary_list[module_choice-1]["Module"]
    tested_topics_list = []
    os.system("cls")
    list_topics(module_dictionary_list, module_choice)

    # Add all the questions related to selected topics into the quiz
    print("Extracting questions from server...")
    client_socket.sendall("extract_questions".encode("utf8"))
    print("Questions extracted.")
    received_list = client_socket.recv(5120)
    question_pool = pickle.loads(received_list)

    quiz_question_list = []
    topics_list = []
    number_list = []
    while True:
        # Prompts user to choose topic to test for quiz
        while True:
            try:
                topic_choice = int(input("Select a topic for the quiz (Enter 0 to continue): "))
                if topic_choice not in range(len(module_dictionary_list[module_choice-1]["TopicList"]) + 1):
                    print("Please select within the given range.")
                    continue
                else:
                    break
            except ValueError:
                print("Please input a valid option.")

        if topic_choice == 0:
            break
            
        # Check if the topic is already added or does not exist in the list
        else:
            selected_topic = module_dictionary_list[module_choice - 1]["TopicList"][topic_choice-1]
            if selected_topic in tested_topics_list:
                print("You already chosen this topic to test in your quiz!")
                continue
            else:
                print(f"You have selected the topic: {selected_topic}")
                tested_topics_list.append(selected_topic)

        # Prompts user for number of questions to test for each tested module
        for topic in tested_topics_list:
            question_topic_count = 0
            for question in question_pool:
                if topic == question["TestedTopic"]:
                    question_topic_count += 1

        while True:
            try:
                print("Enter 0 to test all questions in topic")
                number = int(input(f"Enter number of questions to test for topic {topic}: "))
                if number > question_topic_count:
                    print("You cannot select more topic questions than it has!")
                    continue
                else:
                    break
            except ValueError:
                print("Please enter a number input.")

        number_list.append(number)
        
    for count, topic in zip(number_list, tested_topics_list):
        topics_list.append((count, topic))


    # Appends tested questions filtered based on topics tested
    for topic in tested_topics_list:
        for question in question_pool:
            if question["TestedTopic"] == topic and question["TestedModule"] == selected_module:
                quiz_question_list.append(question)

    quiz_dictionary["Module"] = selected_module
    quiz_dictionary["Topics"] = topics_list
    quiz_dictionary["Questions"] = quiz_question_list

    print("Added all questions based on selected topics to the quiz!")
    input("Press [ENTER] to continue...")
    print("Adding questions...")
    time.sleep(1)
    client_socket.sendall(("append§quizzes.txt§"+str(quiz_dictionary)).encode("utf8"))

# Function to remove a quiz
def remove_quiz():
    print("Extracting quizzes...")
    client_socket.sendall("extract_quizzes".encode("utf8"))
    received_list = client_socket.recv(5120)
    quiz_list = pickle.loads(received_list)
    os.system("cls")
    print("[QUIZZES]")
    for quiz in quiz_list:
        print(f"[{quiz_list.index(quiz) + 1}] {quiz['QuizName']}")
    while True:
        try:
            remove_selection = int(input("Select a quiz to remove (Enter 0 to cancel.): "))
            if remove_selection not in range(len(quiz_list) + 1):
                print("Please only select options within the given range.")
                continue
            else:
                break
        except ValueError:
            print("Please select a valid option.")

    if remove_selection != 0:
        quiz_list.remove(quiz_list[remove_selection-1])
        client_socket.sendall(("write_quizzes§"+str(quiz_list)).encode("utf8"))
        print("Removing quiz...")
        input("Quiz removed! Press [ENTER] to continue...")

# Function to edit quizzes
def edit_quiz():
    print("Extracting quizzes...")
    client_socket.sendall("extract_quizzes".encode("utf8"))
    received_list = client_socket.recv(5120)
    quiz_list = pickle.loads(received_list)
    os.system("cls")
    print("[QUIZZES]")
    for i, quiz in enumerate(quiz_list):
        print(f"[{i+1}] {quiz['QuizName']}")
    
    while True:
        try:
            select_quiz = int(input("Select a quiz to edit (Enter 0 to exit): "))
            if select_quiz not in range(len(quiz_list) + 1):
                print("Please only select the quizzes in range.")
                continue
            else:
                break
        except ValueError:
            print("Please enter a valid input.")

    if select_quiz != 0:
        # Quiz Preview
        os.system("cls")
        print("[QUIZ PREVIEW]")
        print(f"Quiz Name: {quiz_list[select_quiz-1]['QuizName']}")
        print(f"Module: {quiz_list[select_quiz-1]['Module']}")
        print_topics = "Topics: "
        for topic in quiz_list[select_quiz-1]['Topics']:
            print_topics += (topic[1] + ",")
        print(print_topics[:-1])
        print("")
        print("""[QUIZ EDIT MENU]
        [1] Edit Module
        [2] Edit Topics
        [0] Go Back to Previous Page
        """)

        while True:
            try:
                edit_option = int(input("Enter edit option: "))
                if edit_option not in range(3):
                    print("Please enter your option within the given range.")
                    continue
                break
            except ValueError:
                print("Please enter a valid input.")
        
        if edit_option == 1:
            # Extract list of modules from server database
            client_socket.sendall("extract_modules".encode("utf8"))
            print("Extracting list of modules from server database...")
            time.sleep(1)
            received_list = client_socket.recv(5120)
            module_dictionary_list = pickle.loads(received_list)
            print("Modules received!")
            os.system("cls")

            # Add all the questions related to selected topics into the quiz
            print("Extracting questions from server...")
            client_socket.sendall("extract_questions".encode("utf8"))
            received_list = client_socket.recv(5120)
            question_pool = pickle.loads(received_list)
            os.system("cls")
            list_modules(module_dictionary_list)       

            number_list = []
            topics_list = []

            # Prompt user to choose module to test
            while True:
                try:
                    module_choice = int(input("Select a module for the quiz: "))
                    if module_choice not in range(1, len(module_dictionary_list) + 1):
                        print("Please select within the given range.")
                        continue
                    else:
                        break
                except ValueError:
                    print("Please input a valid option.")

            selected_module = module_dictionary_list[module_choice-1]["Module"]
            tested_topics_list = []
            os.system("cls")
            list_topics(module_dictionary_list, module_choice)

            while True:
                # Prompt user to select topic for quiz
                while True:
                    try:
                        topic_choice = int(input("Select a topic for the quiz (Enter 0 to continue): "))
                        if topic_choice not in range(len(module_dictionary_list[module_choice-1]["TopicList"]) + 1):
                            print("Please select within the given range.")
                            continue
                        else:
                            break
                    except ValueError:
                        print("Please input a valid option.")

                # Break out of loop if user is finished adding topics to quiz
                if topic_choice == 0:
                    break
                
                # If not, check if topic is already chosen to avoid duplicates
                else:
                    selected_topic = module_dictionary_list[module_choice - 1]["TopicList"][topic_choice-1]
                    if selected_topic in tested_topics_list:
                        print("You already chosen this topic to test in your quiz!")
                        continue
                    else:
                        print(f"You have selected the topic: {selected_topic}")
                        tested_topics_list.append(selected_topic)

                    # Counts how many questions based on selected topic there are based on what topic user chose
                    for topic in tested_topics_list:
                        question_topic_count = 0
                        for topic, question in zip(tested_topics_list, question_pool):
                            if topic == question["TestedTopic"]:
                                question_topic_count += 1

                    # Prompts user for number of questions to test for each tested module
                    while True:
                        try:
                            number = int(input("Enter number of questions to test topic: "))
                            if number > question_topic_count:
                                print("You cannot test more questions than there are!")
                                continue
                            break
                        except ValueError:
                            print("Please enter a number input")
                    number_list.append(number)

            # Appends number of questions and tested topic into a tuple and append it to a list
            for count, topic in zip(number_list, tested_topics_list):
                topics_list.append((count, topic))

                quiz_question_list = []
                for topic in tested_topics_list:
                    for question in question_pool:
                        if question["TestedTopic"] == topic and question["TestedModule"] == selected_module:
                            quiz_question_list.append(question)

                quiz_list[select_quiz-1]["Module"] = selected_module
                quiz_list[select_quiz-1]["Topics"] = topics_list
                quiz_list[select_quiz-1]["Questions"] = quiz_question_list
            
            client_socket.sendall(("write_quizzes§"+str(quiz_list)).encode("utf8"))

        elif edit_option == 2:
            print("Extracting questions from server...")
            client_socket.sendall("extract_questions".encode("utf8"))
            received_list = client_socket.recv(5120)
            question_pool = pickle.loads(received_list)

            # Extract list of modules from server
            client_socket.sendall("extract_modules".encode("utf8"))
            print("Extracting list of modules from server database...")
            time.sleep(1)
            received_list = client_socket.recv(5120)
            module_dictionary_list = pickle.loads(received_list)
            print("Modules received!")
            os.system("cls")

            # Use a for loop to get selected module and topics
            for module_dict in module_dictionary_list:
                if module_dict["Module"] == quiz_list[select_quiz-1]['Module']:
                    module_index = module_dictionary_list.index(module_dict)
                    topic_list = module_dict["TopicList"]
                    break
            
            # Prints list of modules and topics
            list_topics(module_dictionary_list, module_index + 1)
            print("\nTopics tested:")
            for topic in quiz_list[select_quiz-1]['Topics']:
                print(f"- {topic[1]}")

            print("""(Add a ! prefix to add a topic and a @ prefix to remove a topic (e.g. !1 to add topic number 1 and @1 to remove)""")
            print("- Enter 0 to exit this process")
            
            while True:
                topic_select = input(">>> ")
                if topic_select == "0":
                    break

                # Input Validation
                else:
                    while True:
                        if len(topic_select) > 0:
                            # Prefix check
                            if topic_select[0] == "!" or topic_select[0] == "@":
                                # Digit check
                                if topic_select[1:].isdigit():
                                    # Range check
                                    if int(topic_select[1:]) in range(len(topic_list) + 1):
                                        break
                                    else:
                                        print("Please enter an input within the range above.")
                                        topic_select = input(">>> ")
                                else:
                                    print("Please enter a valid number input.")
                                    topic_select = input(">>> ")
                            else:
                                print("Please enter a valid prefix!")
                                topic_select = input(">>> ")
                        else:
                            print("Please do not leave your input blank!")
                            topic_select = input(">>> ")
                
                    # Add question if ! prefix entered
                    if topic_select[0] == "!":
                        # Counts how many questions based on selected topic there are based on what topic user chose
                        topic_index = int(topic_select[1:]) - 1
                        chosen_topic = module_dictionary_list[module_index]['TopicList'][topic_index]
                        question_topic_count = 0
                        # Counts the number of questions under the selected topic
                        for question in question_pool:
                            if chosen_topic == question["TestedTopic"]:
                                question_topic_count += 1

                        # Prompts user for number of questions to test for each tested module
                        while True:
                            try:
                                number = int(input("Enter number of questions to test topic: "))
                                if number > question_topic_count:
                                    print("You cannot test more questions than there are!")
                                    continue
                                break
                            except ValueError:
                                    print("Please enter a number input")
                        
                        # Inserts number of questions tested for each topic and the topic name into a tuple
                        topic_tuple = (number, topic_list[int(topic_select[1:])-1])

                        # Scan for existing topics:
                        for tuple in quiz_list[select_quiz-1]['Topics']:
                            if topic_tuple[1] in tuple:
                                print("This topic is already tested in this quiz!")
                                break
                        else:
                            print(f"Added the topic {topic_list[int(topic_select[1:])-1]}")
                            quiz_list[select_quiz - 1]['Topics'].append((number, topic_list[int(topic_select[1:])-1]))
                    
                    # Removes topics if @ prefix entered
                    elif topic_select[0] == "@":
                        check = False
                        for topic in quiz_list[select_quiz-1]['Topics']:
                            if topic_list[int(topic_select[1:])-1] in topic:
                                check = True
                                break
                        
                        if check == True:
                            print(f"Removed the topic {topic_list[int(topic_select[1:])-1]}!")
                            for i in range(len(quiz_list[select_quiz - 1]['Topics'])):
                                if quiz_list[select_quiz - 1]['Topics'][i][1] == (topic_list[int(topic_select[1:])-1]):
                                    quiz_list[select_quiz - 1]['Topics'].remove(quiz_list[select_quiz - 1]['Topics'][i])
                                    break
                        else:
                            print("This topic is not tested in the quiz!")

            quiz_question_list = []     # New quiz question list that will update the previous version of list
            for topic in quiz_list[select_quiz - 1]['Topics']:
                for question in question_pool:
                    if question["TestedTopic"] == topic[1] and question["TestedModule"] == module_dictionary_list[module_index]["Module"]:
                        quiz_question_list.append(question)

            quiz_list[select_quiz-1]["Questions"] = quiz_question_list
            client_socket.sendall(("write_quizzes§"+str(quiz_list)).encode("utf8"))

# Encryption password function (Basic Caesar Cipher shifting by 3 ASCII Values)
global encrypt
def encrypt(pwd):
    pwd = pwd.strip()
    new_pwd = ''
    for char in pwd:    # Use for loop to shift ASCII value up by 3 for every character in string
        value = ord(char)
        new_pwd += chr(value + 3)   # Compiles into a new string to return
    return new_pwd

# Decryption password function (Reverse Process)
global decrypt
def decrypt(pwd):
    new_pwd = ''
    for char in pwd:    # Uses for loop to shift ASCII value down by 3 for every character in string
        value = ord(char)
        new_pwd += chr(value - 3)
    return new_pwd

# List users from userid_pswd.txt file
global list_users
def list_users(socket):
    print("Retreiving user list from server database...")
    socket.sendall("get_user_list".encode("utf8"))
    received_list = socket.recv(5120)
    user_list = pickle.loads(received_list)

    print("[REGISTERED USER LIST]")
    for i, user in list(enumerate(user_list)):  # For loop for numbered list of user
        print("[" + str(i+1) + "]", end=" ")
        user_details = user.split(",")

        # Displays privileges of users
        if user_details[0] == "A":
            print("[ADMIN]", end=" ")
        elif user_details[0] == "U":
            print("[USER]", end=" ")
        print(user_details[1])

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

# User Menu Function
def users():
    print('''                                           
  _   _  ___ _ __   _ __ ___   ___ _ __  _   _   _
 | | | / __|/ _ \ '__| | '_ ` _ \ / _ \ '_ \| | | |
 | |_| \__ \  __/ |    | | | | | |  __/ | | | |_| |
  \__,_|___/\___|_|    |_| |_| |_|\___|_| |_|\__,_|                                      
                                                   
    ''')
    print(Colors.YELLOW + """
    [MANAGE USER ACCOUNTS]
    [1] List Users
    [2] Add a new user
    [3] Remove a user
    [4] Edit User Details
    - Enter [e] to exit to previous page
    """ + Colors.END)


# Add User Function
def add_user():
    print("""
    [ADD USER]
    [1] Admin
    [2] User
    [0] Cancel
    """)
        
    # Option to choose to add admin or normal user
    user_type = input("Select user type: ")
    # Choice Validation
    while user_type not in ["0", "1", "2"]:
        print("Select only from the options above!")
        user_type = input("Select user type: ")
    if user_type != "0":
        if user_type == "1":    # Admin User
            user_type = "A"
        elif user_type == "2":  # Normal User
            user_type = "U"

        # Username for new user
        # Check if username is blank or username already exists
        while True:

            username = input("Enter username: ")
            client_socket.sendall(("check_username-" + username).encode("utf8"))
            # Checks if username already exists in the userid_pswd.txt file
            verification = client_socket.recv(5120).decode("utf8")
            if len(username) == 0:
                print("Your username cannot be blank!")
            elif verification == "True":
                print("This username already exists! Please enter a unique username.")
            else:
                break
        # Display password requirements
        print("\nPassword Requirements:")
        print("- Include at least one uppercase and lowercase letter")
        print("- At least one special character")
        print("- At least one number")
        print("- Should be between 8-24 characters long")

        # Infinite loop until password requirements are met
        while True:
            new_password = getpass.getpass("Enter your password: ")
            if check_password(new_password) == True:

                # Confirm password check
                re_enter_password = getpass.getpass("Re-enter your password: ")
                while re_enter_password != new_password:
                    print("Password does not match! Enter again!")
                    re_enter_password = getpass.getpass("Re-enter your password: ")
                
                # Encrypts and writes password to userid_pswd file
                encrypted_password = encrypt(new_password)
                print(f"New user {username} with password {new_password} has been successfully added!")
                input(Colors.NEGATIVE + "Press ENTER to continue!" + Colors.END)
                break
            else:
                print("Password does not meet the requirements!")

        # Joins list into a string separated by a comma, writing it to userid_pswd.txt
        id_string = ",".join([user_type, username, encrypted_password])
        # Append string to the end of userid_pswd file
        client_socket.sendall(("adduser§" + id_string).encode("utf8"))

# Remove a User Function
def remove_user():
    print("[REMOVE A USER]")
    list_users(client_socket)
    client_socket.sendall("get_user_list".encode("utf8"))
    received_list = client_socket.recv(5120)
    users = pickle.loads(received_list)
    while True:
        try:
            # Get index of user to delete
            # Press 0 to cancel the selection
            index = int(input("Select index of user to remove ([0] to cancel): "))
            if index == 0:
                break
            # Range input check
            if index not in range(1, len(users) + 1):   # Check if range is between 1 and number of users
                print("Please only select an index from the user list.")
                continue
            break
        except ValueError:
            print("Please enter a number.")
    
    # If the index the user input is 0, this makes sure that value does not get into the following process instead of skipping it
    if index != 0:
        # Double checks with the user if they really want to remove the user (Confirmation prompt)
        verify = input("Are you sure you want to remove this user? [y/n]: ")

        # Only take in yes or no inputs
        while verify not in ["y", "Y", "n", "N"]:
            print("Please select yes or no.")
            verify = input("Are you sure you want to remove this user? [y/n]: ")
        if verify == "y" or verify == "Y":
            removed_user = users[index-1]   # Detects user with inputted index from the user list
            users.remove(removed_user)      # Removes selected user
            print("Updating user list...")
            client_socket.sendall(("update_user_list-" + str(users)).encode("utf8"))
            print("User successfully removed.")

# Function to edit username or password
def edit_user():
    list_users(client_socket)
    print("[0] Back to Previous Page")
    # Extract list of users from the userid_pswd.txt file
    print("Extracting user list from server database...")
    client_socket.sendall("get_user_list".encode("utf8"))
    received_list = client_socket.recv(5120)
    lines = pickle.loads(received_list)

    while True:     # Iterates until a valid integer input is entered
        try:
            user_index = int(input("Select a user to edit: "))
            if user_index not in range(len(lines) + 1):
                print("Please only select the user index from the list above.")
                continue
            break
        except ValueError:
            print("Please enter a number.")

    # Prompts user to edit either username or password
    if user_index != 0:
        os.system("cls")
        print("[EDIT USER DETAILS]")
        print("[1] Edit Username")
        print("[2] Change Password")
        print("[0] Exit to Previous Page")
        # Data validation for choice
        while True:
            try:
                choice = int(input("Select option: "))
                if choice not in range(3):
                    print("Only select from the options above.")
                    continue
                break
            except ValueError:
                print("Please enter an integer input.")
        
        # Changes username
        if choice == 1:
            new_user_list = []  # Creates a new list to be joined to be written to the userid_pswd.txt file
            new_username = input("Enter new username: ")
            
            # Extracts list of users from userid_pswd.txt
            client_socket.sendall("get_user_list".encode("utf8"))
            received_list = client_socket.recv(5120)
            user_list = pickle.loads(received_list)   

            # Runs a for loop to scan for matching index to replace the username
            for user in user_list:
                # Splits into a list so that the username can be replaced with the new one
                id_list = user.split(",")
                if (user_index - 1) == user_list.index(user):
                    id_list[1] = new_username   # Writes new username over old username
                    
                new_list = ",".join(id_list)    # Joins list back into string separated by commas            
                # Appends to new list
                new_user_list.append(new_list)

            # Writes updated user list into the userid_pswd.txt file
            client_socket.sendall(("update_user_list-" + str(new_user_list)).encode("utf8"))

            print("Username successfully changed.")
            input(Colors.NEGATIVE + "Press ENTER to continue" + Colors.END)

        # Changes password
        elif choice == 2:
            new_user_list = []
            print("\nPassword Requirements:")
            print("- Include at least one uppercase and lowercase letter")
            print("- At least one special character")
            print("- At least one number")
            print("- Should be between 5-12 characters long")

            # Password validation
            while True:
                new_password = getpass.getpass("Enter your password: ")
                if check_password(new_password) == True:
                    re_enter_password = getpass.getpass("Re-enter your password: ")
                    while re_enter_password != new_password:
                        print("Password does not match! Enter again!")
                        re_enter_password = getpass.getpass("Re-enter your password: ")
                    encrypted_password = encrypt(new_password)
                    print("Password succesfully changed!")
                    input(Colors.NEGATIVE + "Press ENTER to continue!" + Colors.END)
                    break
                else:
                    print("Password does not meet the requirements!")

            client_socket.sendall("get_user_list".encode("utf8"))
            received_list = client_socket.recv(5120)
            user_list = pickle.loads(received_list)
            
            # Runs for loop to scan for matching index to update password
            for user in user_list:
                id_list = user.split(",")
                if (user_index - 1) == user_list.index(user):
                    id_list[2] = encrypted_password + "\n"
                new_list = ",".join(id_list)
                new_user_list.append(new_list)

            client_socket.sendall("update_user_list".encode("utf8"))

        elif choice == 0:
            return

# Verfication of username and password based on user_pswd.txt
def checkID(username, password):   
    check_flag = False
    file = open("./Data/userid_pswd.txt", "r")
    lines = file.readlines()
    for line in lines:
        id_list = line.split(",")

        # Checks if entered username and password matches that in the file userid_pswd.txt
        if username == id_list[1] and password == decrypt(id_list[2].strip()):
            check_flag = True
            break
        else:
            check_flag = False
    file.close()
    return check_flag

# Add Question Function
def add_question():
    os.system("cls")
    print("[ADD QUESTION]")
    mcq = ["A", "B", "C", "D"]
    # Dictionary to store question description, multiple choice answers, correct answer, marks 
    question_dictionary = {}    
    question_description = input("Please enter a question: ")   # Enters question
    question_dictionary["Question"] = question_description      # Stores question in dictionary with key "Question"

    # For loop to store entered answer choices in respective answer keys
    for i in range(len(mcq)):
        choice = input(f"Enter an option for {mcq[i]}: ")
        question_dictionary[mcq[i]] = choice

    # Validates input marks for a question (Maximum 10 marks)
    while True:
        try:
            marks = int(input("Enter number of marks to be allocated (max. 10 marks): "))
            if marks not in range(0, 11):
                print("Out of range! You can only enter a maximum 10 marks.")
                continue
            break
        except ValueError:
            print("Please enter a number, nothing else.")
    
    # Stores marks awarded for answering question correctly in dictionary with key "Marks"
    question_dictionary["Marks"] = marks    
    question_dictionary["InputAnswer"] = ''     # Stores chosen answer in key "InputAnswer" (Only used to check if question attempted or not in the quiz. Will not be rewritten in the question pool) 

    # Prompts user to select a correct answer for question
    correct_answer = input(f"Enter a correct answer {mcq}: ")
    correct_answer = correct_answer.upper()

    # Validate if correct answer is within the mcq list
    while correct_answer not in mcq:
        print(f"Only select a correct answer from {mcq}!")
        correct_answer = input(f"Enter a correct answer {mcq}: ")
        correct_answer = correct_answer.upper()

    question_dictionary["CorrectAnswer"] = correct_answer

    # Extract list of modules from modules.txt
    client_socket.sendall("extract_modules".encode("utf8"))
    print("Extracting list of modules from server database...")
    time.sleep(1)
    received_list = client_socket.recv(5120)
    module_dictionary_list = pickle.loads(received_list)
    print("Modules received!")
    os.system("cls")

    list_modules(module_dictionary_list)

    # Prompts the user to select a module to test the question under
    while True:
        try:
            module_choice = int(input("Enter a choice of module to test this question under: "))
            if module_choice not in range(1, len(module_dictionary_list) + 1):
                print("Please select only from the following modules above.")
                continue
            else:
                break
        except ValueError:
            print("Enter a valid option number.")
    
    tested_module = module_dictionary_list[module_choice-1]["Module"]
    question_dictionary["TestedModule"] = tested_module
    

    list_topics(module_dictionary_list, module_choice)

    # Prompts the user to select a topic under the module for the question
    while True:
        try:
            topic_choice = int(input("Select a topic under this module for this question: "))
            if topic_choice not in range(1, len(module_dictionary_list[module_choice-1]["TopicList"]) + 1):
                print("Please select only from the following topics above.")
                continue
            else:
                break
        except ValueError:
            print("Enter a valid option number.")
    
    tested_topic = module_dictionary_list[module_choice-1]["TopicList"][topic_choice-1]
    question_dictionary["TestedTopic"] = tested_topic

    # Appends new question to a new line in question_pool.txt file
    print("Updating questions...")
    client_socket.sendall(("append§question_pool.txt§" + str(question_dictionary).encode("utf8")))

    print(f"""\nThe question: {question_description} with choices:\nA: {question_dictionary['A']}\nB: {question_dictionary['B']}\nC: {question_dictionary['C']}\nD: {question_dictionary['D']}\nhave been added!\nMarks: {question_dictionary['Marks']}\nCorrect Answer: {question_dictionary['CorrectAnswer']}\nTested Module: {tested_module}\nTested Topic: {tested_topic}\n""")

    input(Colors.NEGATIVE + "Press ENTER to continue..." + Colors.END)

global print_question   # making print_question function global for easy declaration of function in other functions
# Print Question Function
def print_question(): 
    print("Extracting questions from server...")
    client_socket.sendall("extract_questions".encode("utf8"))
    received_list = client_socket.recv(5120)
    question_list = pickle.loads(received_list)
    os.system("cls")
    # Checks if there are questions or no questions in question_pool.txt
    if len(question_list) == 0:
        print("There are no questions to see here... Maybe try adding a new one?")
    else:
        # Lists questions in a numbered format with choices (using enumerate)
        print("Here are the list of questions:")
        for number, question in list(enumerate(question_list)):
            print(f"\nQuestion {number+1}: {question['Question']}")
            print(f"(a) {question['A']}")
            print(f"(b) {question['B']}")
            print(f"(c) {question['C']}")
            print(f"(d) {question['D']}")

# Remove Question Function
def remove_question():
    os.system("cls")
    print("Extracting questions from server...")
    client_socket.sendall("extract_questions".encode("utf8"))
    received_list = client_socket.recv(5120)
    question_list = pickle.loads(received_list)
    os.system("cls")
    print("[REMOVE QUESTION]")
    print_question()

    # Checks if there are questions in the question pool
    if len(question_list) == 0:
        print("You cannot delete any questions because they all don't exist!")
        input(Colors.NEGATIVE + "Press Enter to continue..." + Colors.END)
    else:
        # Input validation (Range and Integer Check)
        while True:
            try:
                # Prompts index of question to remove from the question pool
                index = int(input("\nEnter a question number to remove or [0] to delete everything: "))
                # Range Check
                if index not in range(0, len(question_list)+1):
                    print("That question number does not exist. Try again!")
                    continue

                # User option to clear all questions in the question pool
                if index == 0:
                    confirm = input("[WARNING!] YOU ARE ABOUT TO CLEAR THE QUESTION POOL. ARE YOU SURE YOU WANT TO PROCEED? (Enter Y to proceed, enter any key to cancel) ~ ")
                    if confirm == "y" or confirm == 'Y':
                        # Wipes all questions from the question_pool.txt file by rewriting a blank string into file
                        client_socket.sendall("clear_question_pool".encode("utf8"))
                        break
                    else:
                        continue
                break
            except ValueError:
                print(Colors.RED + "Invalid Input! Please try again." + Colors.BLUE)

        # Otherwise, prompt question number user wants to remove from the question pool
        if index != 0:
            question_list.remove(question_list[index-1])
            client_socket.sendall(("update_question_list§" + str(question_list)).encode("utf8"))
        

# ===================================================================================
# MAIN ADMIN LOGIC
# ===================================================================================

def admin_main():
    # Main Program Logic for Admin Menu
    print_menu()
    option = input(f"{admin_username}@admin ~$ ")
    while option != "e" and option != "E":
        # Question Pool Settings
        if option == '1':
            output = ""
            os.system("cls")
            question_pool_menu()
            option2 = input(f"{admin_username}@admin ~$ ")
            while option2 != "e" and option2 != "E":
                if option2 == '1':
                    add_question()      # Adds question
                    os.system("cls")
                elif option2 == '2':
                    remove_question()   # Removes question
                    os.system("cls")
                elif option2 == '3':
                    edit_question()     # Edits question
                    os.system("cls")
                elif option2 == '4':
                    quiz_settings()     # Settings
                    os.system("cls")
                else:
                    os.system("cls")
                    print(Colors.RED + "Invalid Input!" + Colors.END)
                question_pool_menu()
                option2 = input(f"{admin_username}@admin ~$ ")

        # Module Settings
        elif option == '2':
            output = ""
            output2 = ""
            os.system("cls")
            print(output2)
            module_menu()
            option2 = input(f"{admin_username}@admin ~$ ")
            while option2 != 'e' and option2 != 'E':
                if option2 == '1':
                    output2 = ""
                    os.system("cls")
                    new_module()
                elif option2 == '2':
                    output2 = ""
                    os.system("cls")
                    edit_module()
                elif option2 == "3":
                    output2 = ""
                    os.system("cls")
                    remove_module()
                else:
                    output2 = Colors.RED + "Invalid Input!" + Colors.BLUE
                    os.system("cls")
                
                os.system("cls")
                print(output2)
                module_menu()
                option2 = input(f"{admin_username}@admin ~$ ")

        # User Settings
        elif option == '3':
            output = ""
            output2 = ""
            os.system("cls")
            users()
            option2 = input(f"{admin_username}@admin ~$ ")
            while option2 != 'e' and option2 != 'E':
                if option2 == '1':
                    output2 = ""
                    os.system("cls")
                    list_users(client_socket)    # Lists users
                    input(Colors.NEGATIVE + "Press ENTER to exit" + Colors.END)
                elif option2 == '2':
                    output2 = ""
                    os.system("cls")
                    add_user()      # Adds new user with username and password
                elif option2 == '3':
                    output2 = ""
                    os.system("cls")
                    remove_user()   # Removes a user
                elif option2 == '4':
                    output2 = ""
                    os.system("cls")
                    edit_user()     # Edits user's username or password
                else:
                    output2 = Colors.RED + "Invalid Input!" + Colors.BLUE

                os.system("cls")
                print(output2)  # invalid input message (if any)
                users() 
                option2 = input(f"{admin_username}@admin ~$ ")

        # Quiz Results
        elif option == "4":
            output = ""
            output2 = ""
            os.system("cls")
            results_menu()
            option2 = input(f"{admin_username}@admin ~$ ")
            while option2 != 'e' and option2 != 'E':
                if option2 == '1':
                    output2 = ""
                    os.system("cls")
                    view_results()      # View Quiz Reports
                elif option2 == '2':
                    output2 = ""
                    os.system("cls")
                    generate_report()   # Generate Report
                elif option2 == '3':
                    output2 = ""
                    os.system("cls")
                    export_user_report_csv()        # Export results to CSV
                elif option2 == '4':
                    output2 = ""
                    os.system("cls")
                    # Management Report Function goes here!
                    generate_management_report()
                elif option2 == '5':
                    output2 = ""
                    os.system("cls")
                    clear_results()     # Clears all results from the text file quiz_results
                else:
                    output2 = Colors.RED + "Invalid Input!" + Colors.BLUE
                os.system("cls")
                print(output2)
                results_menu()
                option2 = input(f"{admin_username}@admin ~$ ")
                
        # Manage Quizzes
        elif option == "5":
            output = ""
            output2 = ""
            os.system("cls")
            quiz_menu()
            option2 = input(f"{admin_username}@admin ~$ ")
            while option2 != "e" and option2 != "E":
                if option2 == "1":
                    os.system("cls")
                    output2 = ""
                    add_quiz()      # Creates a new quiz 
                elif option2 == "2":
                    os.system("cls")
                    output2 = ""
                    edit_quiz()
                elif option2 == "3":
                    os.system("cls")
                    output2 = ""
                    remove_quiz()
                else:
                    output2 = Colors.RED + "Invalid Input!" + Colors.END
                    
                os.system("cls")
                print(output2)
                quiz_menu()
                option2 = input(f"{admin_username}@admin ~$ ")
        
        elif option == "call a very normal function":   # Calls a very normal function
            output = ""
            os.system("cls")
            normal_function()
        
        else:
            output = Colors.RED + "Invalid Input" + Colors.BLUE

        os.system("cls")
        print(output)
        print_menu()
        option = input(f"{admin_username}@admin ~$ ")

# Edit Question Function
def edit_question():
    # Preview Question function
    def question_preview(index, lst):
        print("[Question Preview]")
        print(f"Module: {lst[index-1]['TestedModule']}")
        print(f"Topic: {lst[index-1]['TestedTopic']}")
        print(f"Question {index}: {lst[index-1]['Question']} ({lst[index-1]['Marks']} marks)")
        print(f"(a) {lst[index-1]['A']}")
        print(f"(b) {lst[index-1]['B']}")
        print(f"(c) {lst[index-1]['C']}")
        print(f"(d) {lst[index-1]['D']}")
        print(f"Correct Answer: {lst[index-1]['CorrectAnswer']}")

    os.system("cls")
    print("Extracting questions from server...")
    client_socket.sendall("extract_questions".encode("utf8"))
    received_list = client_socket.recv(5120)
    question_list = pickle.loads(received_list)
    os.system("cls")
    print("[EDIT QUESTION]")
    print_question()    # Prints question selected

    
    # Check if there are any questions
    if len(question_list) == 0:
        print("You cannot edit non-existent questions!")
        input("Press [ENTER] to continue")
    else:
        # Select a question number to edit
        while True:
            try:
                # Integer and range check
                select_question = int(input("\nEnter a question number to edit (Enter 0 to cancel): "))
                if select_question not in range(0, len(question_list) + 1):
                    print("Out of range!")
                    continue
                break
            except ValueError:
                print(Colors.RED + "Invalid Input. Enter a valid number choice." + Colors.BLUE)
        
        if select_question != 0:
            # Question Preview
            os.system("cls")
            question_preview(select_question, question_list)

            # Select Edit Choice in Question
            def print_edit():
                print(
                f"""
                Choose what to edit in Question {select_question}:
                - Question Description\t\t(Enter Q)
                - Choice A\t\t\t(Enter A)
                - Choice B\t\t\t(Enter B)
                - Choice C\t\t\t(Enter C)
                - Choice D\t\t\t(Enter D)
                - Correct Answer\t\t(Enter X)
                - Marks\t\t\t\t(Enter M)
                - Change Module or Topic\t(Enter T)
                ~ Enter [s] to exit and save changes
                """
                )

            def edit_module_topic(question_list, select_question):
                print("""
                [EDIT QUESTION MODULE AND TOPIC]
                [1] Change Module
                [2] Change Topic
                """)
                while True:
                    try:
                        prompt = int(input("Select option: "))
                        if prompt not in range(1, 3):
                            print("Please only select the options in range.")
                            continue
                        else:
                            break
                    except ValueError:
                        print("Please select an option number")
                            
                # Extract list of modules from modules.txt
                client_socket.sendall("extract_modules".encode("utf8"))
                print("Extracting list of modules from server database...")
                time.sleep(1)
                received_list = client_socket.recv(5120)
                module_dictionary_list = pickle.loads(received_list)
                print("Modules received!")
                os.system("cls")

                if prompt == 1:
                    list_modules(module_dictionary_list)
                    while True:
                        try:
                            new_module_selection = int(input("Select a new module for the question: "))
                            if new_module_selection not in range(1, len(module_dictionary_list) + 1):
                                print("Please only select options within the following range.")
                            else:
                                break
                        except ValueError:
                            print("Please select a valid option.")

                    question_list[select_question-1]["TestedModule"] = module_dictionary_list[new_module_selection-1]["Module"]
                    
                    list_topics(module_dictionary_list, new_module_selection)
                    
                    while True:
                        try:
                            new_topic_selection = int(input("Select a new topic for the question: "))
                            if new_topic_selection not in range(1, len(module_dictionary_list[new_module_selection-1]["TopicList"]) + 1):
                                print("Please only select options within the following range.")
                            else:
                                break
                        except ValueError:
                            print("Please select a valid option.")
                    
                    question_list[select_question - 1]["TestedTopic"] = module_dictionary_list[new_module_selection-1]["TopicList"][new_topic_selection-1]
                
                elif prompt == 2:
                    module = question_list[select_question-1]["TestedModule"]
                    print(f"[LIST OF TOPICS IN MODULE {module}]")
                    for module_dictionary in module_dictionary_list:
                        if module_dictionary["Module"] == module:
                            module_index = module_dictionary_list.index(module_dictionary)
                            for i, topic in enumerate(module_dictionary["TopicList"]):
                                print(f"{i+1}. {topic}")
                            break

                    while True:
                        try:
                            new_topic_selection = int(input("Select a new topic for the question: "))
                            if new_topic_selection not in range(1, len(module_dictionary_list[module_index]["TopicList"]) + 1):
                                print("Please only select options within the following range.")
                                continue
                            else:
                                break
                        except ValueError:
                            print("Please select a valid option.")
                        
                    question_list[select_question-1]["TestedTopic"] = module_dictionary_list[module_index]["TopicList"][new_topic_selection-1]
            
            print_edit()
            
            option = input('>>> ')
            while option != 's' and option != 'S':
                if option == "A" or option == "a":
                    edit = input("Enter your changes for Choice A: ")   # Edit answer for choice A
                    question_list[select_question-1]["A"] = edit
                elif option == "B" or option == "b":
                    edit = input("Enter your changes for Choice B: ")   # Edit answer for choice B
                    question_list[select_question-1]["B"] = edit
                elif option == "C" or option == "c":
                    edit = input("Enter your changes for Choice C: ")   # Edit answer for choice C
                    question_list[select_question-1]["C"] = edit
                elif option == "D" or option == "d":
                    edit = input("Enter your changes for Choice D: ")   # Edit answer for choice D
                    question_list[select_question-1]["D"] = edit
                elif option == "Q" or option == "q":
                    edit = input("Enter your changes for Question Description: ")   # Edit question
                    question_list[select_question-1]["Question"] = edit
                elif option == "X" or option == "x":
                    correct_answer = input("Enter a correct answer [A, B, C, D]: ")     # Edit a correct answer
                    while correct_answer not in ["A", "B", "C", "D", "a", "b", "c", "d"]:
                        print("Only select a correct answer from the four A, B, C, D options!")
                        correct_answer = input("Enter a correct answer [A, B, C, D]: ")
                    question_list[select_question-1]["CorrectAnswer"] = correct_answer.upper()
                elif option == "M" or option == "m":    # Edit number of marks to award
                    while True:
                        try:
                            marks = int(input("Enter number of marks to be allocated (max. 10 marks): "))
                            if marks not in range(0, 11):
                                print("Out of range! You can only enter a maximum 10 marks.")
                                continue
                            break
                        except ValueError:
                            print("Please enter a number, nothing else.")
                    question_list[select_question - 1]["Marks"] = marks
                elif option == "T" or option == "t":    
                    edit_module_topic(question_list, select_question)
                os.system("cls")
                question_preview(select_question, question_list)    # Previews question after edits made
                print_edit()
                option = input('>>> ')

            os.system("cls")
            print("Question has been updated!\n")
            question_preview(select_question, question_list)    # Outputs final changes made to the selected question
            input(Colors.NEGATIVE + "Press ENTER to continue" + Colors.END)

            # Updates edited question in the question_pool.txt file
            print("Updating question pool...")
            client_socket.sendall(("update_question_list§" + str(question_list)).encode("utf8"))
            
 
def quiz_settings():
    os.system("cls")
    settings_dictionary = {}

    client_socket.sendall("get_settings".encode("utf8"))
    received_list = client_socket.recv(5120)
    settings_list = pickle.loads(received_list)

    for line in settings_list:
        line_split = line.split(":")    # Splits settings into a list
        settings_dictionary[line_split[0]] = line_split[1].strip()  # Strips toggled settings of any new lines and stores them into a dictionary with the setting as a key
    
    # Displays options
    def print_options():
        print("[QUIZ SETTINGS]")
        print(
        f"""
        1. Randomize Questions ({settings_dictionary['RandomizeQuestion']}) 
        2. Enable Time Limit ({settings_dictionary['TimeLimit']} >>> {settings_dictionary["Duration"]} mins)
        3. Set Number of Attempts ({settings_dictionary['Attempts']})
        4. Select a Quiz to Test Users >>> ({settings_dictionary['QuizTested']})
        Select an option to toggle or edit setting.
        - Press 'q' to exit and save settings.
        """
        )

    print_options()
    option = input("Enter option: ")

    # Loops until user saves settings by entering 'q'
    while option != 'q':

        # Randomize Questions option
        if option == '1':
            # Toggles setting on or off when choice is selected
            if settings_dictionary['RandomizeQuestion'] == "On":
                settings_dictionary['RandomizeQuestion'] = "Off"
            else:
                settings_dictionary['RandomizeQuestion'] = "On"
        
        # Time Limit option
        elif option == '2':
            # Toggles setting on or off when choice is selected
            if settings_dictionary['TimeLimit'] == "On":
                settings_dictionary['TimeLimit'] = "Off"    # Time limit is 0 when off
                settings_dictionary['Duration'] = 0
            else:
                settings_dictionary['TimeLimit'] = "On"     # When time limit is turned on, set the duration in mins
                while True:
                    try:
                        time = int(input("Enter number of minutes for the duration of the quiz (max. 60 mins): "))
                        if time <= 0:   # Reject negative numbers entered
                            print("Time only exists in the positive plane of integers!")
                            continue
                        elif time > 60:     # Maximum time: 1 hour or 60 minutes
                            print("The maximum time you can give is 60 minutes.")
                            continue
                        break
                    except ValueError:      # Integer type check
                        print("Enter a valid integer value.")
                settings_dictionary['Duration'] = time
        
        # Attempts settings
        elif option == '3':
            while True:
                try:
                    attempts = int(input("Set number of attempts: "))
                    if attempts <= 0:      # Less than 0 attempts are not allowed
                        print("You cannot give 0 or less attempts!")
                        continue
                    break
                except ValueError:
                    print("Please enter an integer input.")
            settings_dictionary["Attempts"] = attempts
        
        # Select a quiz to test the users
        elif option == '4':
            # Requests list of quizzes from the server
            print("Extracting quizzes from the server database...")
            client_socket.sendall("extract_quizzes".encode("utf8"))
            received_list = client_socket.recv(5120)
            quiz_list = pickle.loads(received_list)
            # List quizzes
            print("[LIST OF QUIZZES]")
            for i, quiz in enumerate(quiz_list):
                print(f"[{i+1}] {quiz['QuizName']}")
            
            # Valid quiz selection
            while True:
                try:
                    select_quiz = int(input("Select a quiz to test users: "))
                    if select_quiz not in range(1, len(quiz_list) + 1):
                        print("Please enter your option within the following range above.")
                        continue
                    else:
                        break
                except ValueError:
                    print("Please enter a valid option number.")
            
            chosen_quiz = quiz_list[select_quiz-1]["QuizName"]
            settings_dictionary["QuizTested"] = chosen_quiz

        else:
            print("Please select a valid option.")
        os.system("cls")
        print_options()
        option = input("Enter option: ")

    # Writes updated settings back to quiz_settings text file
    client_socket.sendall(("update_settings§" + str(settings_dictionary)).encode("utf8"))

# Function to view results
def results_menu():
    print("""
       ____    U _____ u   _   _   ____       _   _    _       _____   ____          __  __  U _____ u _   _       _   _  
U |  _"\ u \| ___"|/U |"|u| | / __"| u U |"|u| |  |"|     |_ " _| / __"| u     U|' \/ '|u\| ___"|/| \ |"|   U |"|u| | 
 \| |_) |/  |  _|"   \| |\| |<\___ \/   \| |\| |U | | u     | |  <\___ \/      \| |\/| |/ |  _|" <|  \| |>   \| |\| | 
  |  _ <    | |___    | |_| | u___) |    | |_| | \| |/__   /| |\  u___) |       | |  | |  | |___ U| |\  |u    | |_| | 
  |_| \_\   |_____|  <<\___/  |____/>>  <<\___/   |_____| u |_|U  |____/>>      |_|  |_|  |_____| |_| \_|    <<\___/  
  //   \\\\_  <<   >> (__) )(    )(  (__)(__) )(    //  \\\\  _// \\\\_  )(  (__)    <<,-,,-.   <<   >> ||   \\\\,-.(__) )(   
 (__)  (__)(__) (__)    (__)  (__)         (__)  (_")("_)(__) (__)(__)          (./  \.) (__) (__)(_")  (_/     (__)  
    """)

    print(Colors.GREEN)
    print("""
    [VIEW RESULTS]
    [1] View Past Attempts
    [2] Generate Overall Report
    [3] Export CSV User Report
    [4] View Management Report
    [5] Clear All Attempts
    - Enter [e] to exit to previous page
    """)
    print(Colors.END)

# Function to clear all results
def clear_results():

    client_socket.sendall("extract_results".encode("utf8"))
    received_list = client_socket.recv(5120)
    results_list = pickle.loads(received_list)

    # Checks if there are attempts in the quiz_results file
    if len(results_list) == 0:
        print("There are no attempts to clear!")
        input(Colors.NEGATIVE + "Press ENTER to continue..." + Colors.END)
    else:
        # Confirmation prompt
        choice = input("WARNING, YOU ARE ABOUT TO CLEAR YOUR PAST ATTEMPTS! Are you sure you want to do this? [y/n] ")
        choice = choice.upper()
        while choice not in ["Y", "N"]:     # Yes or no validation
            print("Please only choose Y or N")
            choice = input("WARNING, YOU ARE ABOUT TO CLEAR YOUR PAST ATTEMPTS! Are you sure you want to do this? [y/n] " )
            choice = choice.upper()
        if choice == "Y":
            print("Cleaing attempts...")
            client_socket.sendall("clear_results".encode("utf8"))
            input(Colors.NEGATIVE + "Press ENTER to continue" + Colors.END)    

# Function to view results
def view_results():
    print("Extracting quiz results...")
    client_socket.sendall("extract_results".encode("utf8"))
    received_list = client_socket.recv(5120)
    results_list = pickle.loads(received_list)
    
    # Check if there are any results
    if len(results_list) == 0:
        print("There are no recent attempts...")
        input(Colors.NEGATIVE + "Press ENTER to continue" + Colors.END)
    
    # Lists all attempts from quiz_results file
    else:
        os.system("cls")
        print(Colors.YELLOW)
        print("[LIST OF PAST ATTEMPTS]")
        print("User\t\tDate Attempted\tQuiz")
        for num, user_attempt in enumerate(results_list):
            print(f"[{num+1}] {user_attempt['UserID']}\t{user_attempt['AttemptDate']}\t{user_attempt['QuizName']}")
        
        # Users can select which attempt they want to view in-depth (Tested Questions, Anwers, Marks, Correct Answers)
        print("Select a quiz attempt to view: (Enter 0 to exit)")
        while True:
            try:
                choose_user = int(input(">>> "))
                if choose_user == 0:
                    break
                if choose_user < 0 or choose_user > len(results_list):
                    print("Please select an appropriate option from above.")
                    continue 
                break
            except ValueError:
                print("Please enter a number.")
        
        # Display individual report for a selected attempt
        if choose_user != 0:
            choose_user -= 1
            selected_user = results_list[choose_user]
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

# Generates a general report of performance of quiz attempts

def generate_report():
    # Average, Highest, Lowest, Standard Deviation
    client_socket.sendall("extract_results".encode("utf8"))
    received_list = client_socket.recv(5120)
    results_list = pickle.loads(received_list)

    if len(results_list) == 0:
        print("No attempts to generate report...")
        input(Colors.NEGATIVE + "Press ENTER to continue" + Colors.END)
    else:
        quantity = len(results_list)    # Displays number of attempts in the quiz application
        score_list = []
        for result in results_list:
            score_list.append(result["Score"])  # List of scores to add up
        
        total = sum(score_list)     # Total score
        print(Colors.CYAN + "="*30)
        print("[STATISTICS REPORT]")
        print("="*30)
        print(f"[AVERAGE] >>> {total/quantity}")     # Average
        print(f"[HIGHEST SCORE] >>> {max(score_list)}")  # Highest Score
        print(f"[LOWEST SCORE] >>> {min(score_list)}")   # Lowest Score
        print(f"[MEDIAN SCORE] >>> {statistics.median(score_list)}") # Median Score
        print(f"[MODE SCORE] >>> {statistics.mode(score_list)}" + Colors.END) # Mode Score
        if quantity > 1:    # Display standard deviation if there is more than one quiz attempt
            print(f"{Colors.CYAN}[STANDARD DEVIATION] >>> {round(statistics.stdev(score_list), 3)} {Colors.END}")
        input(Colors.NEGATIVE + "Press ENTER to continue" + Colors.END)

def export_user_report_csv():
    # Get results list from quiz_results.txt file with extracting results function
    client_socket.sendall("extract_results".encode("utf8"))
    received_list = client_socket.recv(5120)
    results_list = pickle.loads(received_list)

    # Finding the result with the most questions
    max_length = 0
    for result in results_list:
        get_length = len(result["Questions"])
        if get_length > max_length:
            max_length = get_length
    
    # Headers in a list to be combined into comma separated strings later on
    header_list = ["UserID", "Quiz Name", "Date Attempted", "Module", "Topics", "Number of Questions", "Score (%)"]
    # For loop to create question headers for description, answer and correct answer
    for i in range(1, max_length+1):
        # String for Question Title
        string1 = "Question "
        string1 += str(i)

        # String for User's Answer
        string2 = "Entered Answer for Question "
        string2 += str(i)

        # String for Correct Answer
        string3 = "Correct Answer for Question "
        string3 += str(i)

        # Append headers to a row list
        header_list.append(string1)
        header_list.append(string2)
        header_list.append(string3)

    print("Writing CSV headers...")
    # Joins them into CSVs
    headers = ",".join(header_list)
    # Sends CSV to server to write to CSV file
    client_socket.sendall(("export_user_csv_headers§" + headers).encode("utf8"))
    time.sleep(2)
    # For each result in the results list, append a row in the CSV
    count = 0
    loading = len(results_list)
    for result in results_list:
        data_list = []
        data_list.append(result["UserID"])      # Adds userid into list
        data_list.append(result["QuizName"])    # Adds name of quiz into list
        data_list.append(result["Module"])      # Adds module tested in quiz
        data_list.append('"' + ", " .join(result["Topics"]) + '"')      # Adds topics tested in quiz
        question_list = result["Questions"]     # Stores list of questions into a variable
        answer_list = result["Answers"]         # Stores list of answers entered by user into a variable
        correct_answer_list = result["CorrectAnswers"]  # Stores list of correct answers into a variable
        data_list.append(result["AttemptDate"]) # Appends date of attempt in data list
        data_list.append(str(len(question_list)))    # Appends number of questions into data list
        data_list.append(str(result["Score"]))      # Appends score into data list

        # Appends question, answer, correct answer for each attempt into each column
        for question, answer, correct_answer in zip(question_list, answer_list, correct_answer_list):
            if "," in question:
                question = '"' + question + '"'
        
            data_list.append(question)
            data_list.append(answer)
            data_list.append(correct_answer)

        # Joins list into a string separated by commas and then appends to the CSV
        data = ",".join(data_list)
        os.system("cls")
        count += 1

        # Loading progress
        print(f"Writing CSV data to server... [{count}/{loading}]")
        client_socket.sendall(("export_user_csv_data§" + data).encode("utf8"))
        # Pause the program to give the server to write a row before the next iteration
        time.sleep(2)

    print("CSV has been generated! Open the file in Excel to see the magic :)")
    input(Colors.NEGATIVE + "Press ENTER to continue..." + Colors.END)

def generate_management_report():
    # Extract quiz list from the server
    print("Extracting quizzes from server database...")
    client_socket.sendall("extract_quizzes".encode("utf8"))
    received_list = client_socket.recv(5120)
    quiz_list = pickle.loads(received_list)

    # Extract quiz results from the server
    print("Extracting quiz results from server database...")
    client_socket.sendall("extract_results".encode("utf8"))
    received_list = client_socket.recv(5120)
    results_list = pickle.loads(received_list)


    while True:
        os.system("cls")
        print('''
                                                                                       dP   
                                                                                       88   
88d8b.d8b. .d8888b. 88d888b. .d8888b. .d8888b. .d8888b. 88d8b.d8b. .d8888b. 88d888b. d8888P 
88'`88'`88 88'  `88 88'  `88 88'  `88 88'  `88 88ooood8 88'`88'`88 88ooood8 88'  `88   88   
88  88  88 88.  .88 88    88 88.  .88 88.  .88 88.  ... 88  88  88 88.  ... 88    88   88   
dP  dP  dP `88888P8 dP    dP `88888P8 `8888P88 `88888P' dP  dP  dP `88888P' dP    dP   dP   
                                           .88                                              
                                       d8888P                                                                                                 
        ''')
        # List of quizzes
        print("[QUIZZES]")
        for i, quiz in enumerate(quiz_list):
            print(f"[{i+1}] {quiz['QuizName']}")
        while True:
            try:
                quiz_selection = int(input("Select a quiz (Enter 0 to exit): "))
                if quiz_selection not in range(len(quiz_list) + 1):
                    continue
                else:
                    break
            except ValueError:
                print("Please enter a valid number option.")

        if quiz_selection != 0:
    
            table1 = PrettyTable()   # Table that will display questions, choices, correct answer and marks
            table2 = PrettyTable()  # Table that will display the answers users inputted for each question in the quiz

            # Headers for table1
            table1.field_names = ["No.", "Topic", "Question", "A", "B", "C", "D", "Correct Answer", "Marks"] 
            question_list = quiz_list[quiz_selection-1]['Questions']    # List of questions from the selected quiz

            # Appends each row for table1 by compiling all data into a row list
            for question in question_list:
                index = question_list.index(question) + 1
                topic = textwrap.fill(question["TestedTopic"], 20) + "\n"
                question_description = textwrap.fill(question["Question"], 15) + "\n"
                a_choice = textwrap.fill(question["A"], 15) + "\n"
                b_choice = textwrap.fill(question["B"], 15) + "\n"
                c_choice = textwrap.fill(question["C"], 15) + "\n"
                d_choice = textwrap.fill(question["D"], 15) + "\n"
                correct_answer = question["CorrectAnswer"]
                score = question["Marks"]
                row = [index, topic, question_description, a_choice, b_choice, c_choice, d_choice, correct_answer, score]
                table1.add_row(row)
            
            os.system("cls")
            print(f"[VIEWING TABLE FOR QUIZ {quiz_list[quiz_selection-1]['QuizName']}]")
            print(f"Quiz Name: {quiz_list[quiz_selection-1]['QuizName']}")
            print(f"Module: {quiz_list[quiz_selection-1]['Module']}")
            print(f"[PERFORMANCE REVIEW FOR QUIZ {quiz_list[quiz_selection-1]['QuizName']}]")

            # Compile number of columns for table2 based on number of questions in the selected quiz
            quiz_attempt_list = []
            for result in results_list:
                # Add the selected attempt from all results to a list if quiz name of attempt matches the selected quiz name 
                if result["QuizName"] == quiz_list[quiz_selection-1]["QuizName"]:
                    quiz_attempt_list.append(result)

            fieldnames = ["User"]
            
            # Creating columns for each question in quiz 
            for q in range(1, len(quiz_list[quiz_selection-1]['Questions']) + 1):
                fieldnames.append(("Q" + str(q)))

            fieldnames.append(("Marks " + "(%)"))   # Marks obtained from quiz by user
            fieldnames.append("Attempt Date")       # Date of attempt by user
                
            table2.field_names = fieldnames     # Add headers for table2
            quiz_question_list = []            

            # Compile a list of questions in the selected quiz
            for quiz_question in quiz_list[quiz_selection-1]['Questions']:
                quiz_question_list.append(quiz_question['Question'])
            
            user_answers_list = []  # List of answers from different users
            user_answers = []       # List of answers by a user who took the selected quiz

            
            for result in quiz_attempt_list:
                row_list = []
                result_question_list = result['Questions']
                row_list.append(result['UserID'])

                # Checks if the question the user attempted exists and appends the inputted answer into the table column
                for quiz_question in quiz_question_list:
                    if quiz_question in result_question_list:
                        for result_question in result_question_list:
                            if quiz_question == result_question:
                                index = result_question_list.index(result_question)
                                row_list.append(result['Answers'][index])
                                user_answers.append(result['Answers'][index])

                    # Append x if user did not get a question set in the quiz tested
                    else:
                        row_list.append("x")

                row_list.append(result['Score'])        # Append score of user
                row_list.append(result["AttemptDate"])  # Append attempt date of user
                table2.add_row(row_list)                # Append row of table2
                user_answers_list.append(user_answers)  # Append list of answers by user to list of set of answers by different users
                
            
            # Gather list of correct answers in the quiz
            correct_answer_list = []
            for quiz_questions in quiz_list[quiz_selection-1]['Questions']:
                correct_answer = quiz_questions['CorrectAnswer']
                correct_answer_list.append(correct_answer)
            
            # Create a row list for the last table3
            last_row_list = []
            table_json = table2.get_json_string()   # Get json string of table2
            data = json.loads(table_json)           # Converts json string into a list
            data = data[1:]                         # Get only the list of dictionaries with user quiz data
            key_list = []

            # Create a list of keys for every question
            for i in range(1, len(correct_answer_list) + 1):
                key_list.append(("Q" + str(i)))

            # Create table3
            table3 = PrettyTable(key_list)

            # Counts the number of people who the question correct and maximum number of people who did the question
            for key in key_list:
                max_correct_count = 0
                correct_count = 0
                for dictionary in data:
                    answer = dictionary[key]
                    if answer != 'x':
                        max_correct_count += 1
                        index = key_list.index(key)
                        if answer == correct_answer_list[index]:
                            correct_count += 1
                string = str(correct_count) + "/" + str(max_correct_count)
                last_row_list.append(string)

            table3.add_row(last_row_list)

            # Print all tables
            print(table1)
            print("\n")
            print("[PAST USER ANSWERS]")
            print(table2)
            print("\n")
            print("[NUMBER OF CORRECT ANSWERS FROM USERS]")
            print(table3)
            input("Press [ENTER] to continue...")
        else:
            break        

# ===================================================================================
# LOGIN SECTION
# ===================================================================================
while True: # Login loop until a valid user and password input is received
    print(Colors.GREEN + "[ADMIN LOGIN PAGE]")  # Login Header
    print(Colors.YELLOW + "[1] Login")
    print(Colors.RED + "[0] Quit" + Colors.END)

    # Main screen validation
    while True:
        try:
            prompt = int(input(">>> "))
            if prompt not in range(2):
                print(Colors.RED + "Please only select from the following options!" + Colors.END)
                continue
            break
        except ValueError:
            print(Colors.RED + "Please select a number option!" + Colors.END)
        
    if prompt == 1:
        admin_username = input(Colors.BLUE + "Enter Username: " + Colors.END)  # username
        admin_password = getpass.getpass(Colors.BLUE + "Enter Password: " + Colors.END)  # password
        print("Verifying admin credentials...")
        userid = "login-" + admin_username + "-" + admin_password
        print("Sending to server to verify credentials...")
        # Verify user details
        client_socket.sendall(userid.encode("utf8"))
        verify = client_socket.recv(5120).decode("utf8")

        # Verify admin privileges
        print("Verifying admin privileges credentials...")
        admin_userid = "check_admin-" + admin_username + "-" + admin_password
        client_socket.sendall(admin_userid.encode("utf8"))
        verify_admin = client_socket.recv(5120).decode("utf8")
        time.sleep(1)
        if verify == "False":
            os.system("cls")
            print(Colors.RED + "Invalid Username or Password." + Colors.END)  # invalid input message
            continue
        elif verify_admin == "False":
            # Display when non-admins login here
            print(Colors.RED + "Only users with admin privileges can access this application!" + Colors.END)
            input(Colors.NEGATIVE + "Press ENTER to continue" + Colors.END) 
            os.system("cls")
            continue
        else:
            os.system("cls")
            print(f"{Colors.GREEN} Login Succesful! Welcome, {Colors.BOLD + admin_username + Colors.END}.\n")   # Welcome output
            admin_main()
            os.system("cls")
    else:
        client_socket.sendall("quit".encode("utf8"))
        break
    os.system("cls")
print("Bye! See you soon! o7 o7 o7")
