# StudentID:	p2104005
# Name:	        Lee Quan Jun Ervin
# Class:		DISM/FT/1B/05
# Assessment:	CA2
#
# Script name:	user.py
#
# Purpose:      To receive requests from admin or user program to read and write files and keep track of how many users 
#               doing the quiz
#
# Usage syntax:	python ./Code/server.py
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
# Modules: socket, sys, Thread, threading, traceback, pickle, time

import socket   # Run the entire socket programming behind the server
import sys      # Terminates program if no connection or socket closed
from threading import Thread    # Multithreading for socket programming
import threading
import traceback
import pickle   # For sending and receiving lists to and fro the client
import time     # For time sleeping sends and receives 

# FUNCTION DECLARATIONS

# Function to extract list of modules
def extract_modules():
    with open("./Data/modules.txt", "r") as file:
        module_dictionary_list = file.readlines()
    for i in range(len(module_dictionary_list)):
        module_dictionary_list[i] = eval(module_dictionary_list[i])
    return module_dictionary_list

# Encryption password function (Basic Caesar Cipher shifting by 3 ASCII Values)
global encrypt
def encrypt(pwd):
    pwd = pwd.strip()
    new_pwd = ''
    for char in pwd:    # Use for loop to shift ASCII value up by 3 for every character in string
        value = ord(char)
        new_pwd += chr(value + 3)   # Compiles into a new string to return
    return new_pwd

# Check user privileges when logging in (Default users cannot access this file)
def check_privileges(username, password):
    check = False
    with open("./Data/userid_pswd.txt", "r") as file:
        lines = file.readlines()
    for line in lines:
        line = line.split(",")
        for i in range(len(line)):
            line[i] = line[i].strip()
        if username in line and encrypt(password) in line:
            # If user has admin privileges (A in prefix in userid_pswd.txt), flag is true
            if line[0] == "A":
                check = True
                break
    return check

# Global so that function can be reused anywhere in other functions
global extract_questions
def extract_questions():
    with open("./Data/question_pool.txt", "r") as file:
        question_dictionary_list = []   # List for question dictionaries
        # List of all question dictionaries stored in question pool each line
        lines = file.readlines()
        # Strip and eval lists
        for dictionary in lines:
            # Strip stringed dictionaries of any newlines or spaces and converts them into dictionary
            dictionary.strip()
            dictionary = eval(dictionary)
            # appends read dictionary into question dictionary list
            question_dictionary_list.append(dictionary)

    return question_dictionary_list

# Function to check if username exists in the userid_pswd file
global check_username
def check_username(username):
    check = False
    with open("./Data/userid_pswd.txt", "r") as file:
        lines = file.readlines()
    for line in lines:
        user_list = line.split(",")
        if username == user_list[1]:
            check = True
    return check

# Decryption password function (Reverse Process)
global decrypt
def decrypt(pwd):
    new_pwd = ''
    for char in pwd:
        value = ord(char)
        new_pwd += chr(value - 3)   # Shift ASCII values down by three
    return new_pwd

# Function to extract list of quizzes from text file
def extract_quizzes():
    with open("./Data/quizzes.txt", "r") as file:
        quiz_list = file.readlines()
    for i in range(len(quiz_list)):
        quiz_list[i] = eval(quiz_list[i])
    return quiz_list

# Verfication of username and password based on user_pswd.txt
def checkID(username, password):
    check_flag = False
    with open("./Data/userid_pswd.txt", "r") as file:
        lines = file.readlines()
        # Uses for loop and spit each line into individual lists and checks each user id value via index
        for line in lines:
            id_list = line.split(",")
            # Returns true if username and password match text file
            if username == id_list[1] and password == decrypt(id_list[2].strip()):
                check_flag = True
                break
            else:
                check_flag = False

    return check_flag

# Function to append contents for certain data file
def append(string):
    string_list = string.split("§")
    filename = string_list[1]
    contents = string_list[2]
    filename2 = "./Data/" + filename
    with open(filename2, "a") as file:
        file.write(contents + "\n")

# Function for extracting list of results
def extract_results():
    results_list = []
    # Extract results from quiz_results.txt file and store them into a new global list for easy reference
    with open("./Data/quiz_results.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        line = eval(line.strip())
        results_list.append(line)

    return results_list

# Client thread for receiving requests from clients and performing the requested actions accordingly
def client_thread(connection, ip, port, max_buffer_size = 5120):
    is_active = True
    while is_active:
        client_message = receive_input(connection, max_buffer_size)
        if "quit" in client_message:
            print("[CLIENT] Requesting to quit...")
            connection.close()
            print(f"[CLIENT] Connection IP: {ip} Port: {port} closed.")
            is_active = False

        if "login" in client_message:
            print("[CLIENT] Sending in login credentials for verification")
            userid_list = client_message.split("-")
            username = userid_list[1]
            password = userid_list[2]
            verify = checkID(username, password)
            print(f"[SERVER] Sending verification status back ({verify})")
            connection.sendall(str(verify).encode("utf8"))

        if " has successfully logged into the quiz!" in client_message:
            print(f"[CLIENT] " + client_message)

        if "extract_results" in client_message:
            print("[CLIENT] Requested to call function extract_results")
            time.sleep(1)
            print("[SERVER] Extracting results from server database...")
            results_list = extract_results()
            send_list = pickle.dumps(results_list)
            time.sleep(1)
            print("[SERVER] Results extracted. Sending them back!")
            connection.sendall(send_list)

        if "append" in client_message:
            print("[CLIENT] Requested to append file")
            time.sleep(1)
            print("[SERVER] Appending to selected file...")
            time.sleep(1)
            append(client_message)
            print("[SERVER] Contents written!")

        if "extract_quizzes" in client_message:
            print("[CLIENT] Requested to call function extract_quizzes")
            time.sleep(1)
            print("[SERVER] Extracting list of quizzes...")
            time.sleep(1)
            quiz_list = extract_quizzes()
            send_list = pickle.dumps(quiz_list)
            print("[SERVER] Sending the quiz list back!")
            connection.sendall(send_list)

        if "check_username" in client_message:
            print("[CLIENT] Requested to call function check_username")
            time.sleep(1)
            print("[SERVER] Checking username... ")
            received_list = client_message.split("-")
            username = received_list[1]
            boolean = check_username(username)
            time.sleep(1)
            print(f"[SERVER] Sending verification status back! ({str(boolean)})")
            connection.sendall(str(boolean).encode("utf8"))
        
        if "adduser" in client_message:
            print("[CLIENT] Requested to perform action: add_user")
            time.sleep(1)
            print("[SERVER] Writing user to database...")
            time.sleep(1)
            received = client_message.split("§")
            userid = received[1]
            with open("./Data/userid_pswd.txt", "a") as file:
                file.write(userid + "\n")
            print("[SERVER] User successfully written!")

        if "get_user_list" in client_message:
            print("[CLIENT] Requested to perform action: get_user_list")
            time.sleep(1)
            print("[SERVER] Retrieving user lists from server database...")
            time.sleep(1)
            with open("./Data/userid_pswd.txt", "r") as file:
                user_list = file.readlines()
            send_list = pickle.dumps(user_list)
            connection.sendall(send_list)
            print("[SERVER] Sent the user list back!")
        
        if "update_user_list" in client_message:
            print("[CLIENT] Requested to perform action: update_user_list")
            time.sleep(1)
            received_list = client_message.split('-')
            new_user_list = eval(received_list[1])
            with open("./Data/userid_pswd.txt", "w") as file:
                for line in new_user_list:
                    file.write(str(line))

        if "get_settings" in client_message:
            print("[CLIENT] Requested to perform action: get_settings")
            with open("./Data/quiz_settings.txt", "r") as file:
                settings_list = file.readlines()

            send_list = pickle.dumps(settings_list)
            connection.sendall(send_list)
        
        if "extract_questions" in client_message:
            print("[CLIENT-ADMIN] Requested to perform action: extract_questions")
            time.sleep(1)
            question_list = extract_questions()
            print("[SERVER] Extracting questions from server database...")
            time.sleep(1)
            send_list = pickle.dumps(question_list)
            connection.sendall(send_list)
            print("[SERVER] Sent the questions back!")

        if "check_admin" in client_message:
            print("[CLIENT-ADMIN] Sending login credentials to server for admin verification...")
            time.sleep(1)
            print("[SERVER] Checking privileges...")
            time.sleep(1)
            received_list = client_message.split("-")
            username = received_list[1]
            password = received_list[2]
            verify = check_privileges(username, password)
            print(f"[SERVER] Sent back verification status ({verify})")
            connection.sendall(str(verify).encode("utf8"))

        if "extract_modules" in client_message:
            print("[CLIENT-ADMIN] Requested to call function extract_modules")
            time.sleep(1)
            module_dictionary_list = extract_modules()
            send_list = pickle.dumps(module_dictionary_list)
            print("[SERVER] Sent modules back to client!")
            connection.sendall(send_list)
        
        if "write_modules" in client_message:
            print("[CLIENT-ADMIN] Requested to call function write_modules")
            print("[SERVER] Updating modules...")
            time.sleep(1)
            received_list = client_message.split("§")
            module_dictionary_list = eval(received_list[1])
            with open("./Data/modules.txt", "w") as file:
                for module_dictionary in module_dictionary_list:
                    file.write(str(module_dictionary) + "\n")
            print("[SERVER] Modules updated")

        if "write_quizzes" in client_message:
            print("[CLIENT-ADMIN] Requested to perform action write_quizzes")
            time.sleep(1)
            print("[SERVER] Writing quizzes...")
            time.sleep(1)
            received_list = client_message.split("§")
            quiz_list = eval(received_list[1])
            with open("./Data/quizzes.txt", "w") as file:
                for quiz in quiz_list:
                    file.write(str(quiz) + "\n")
            print("[SERVER] Quizzes updated!")

        if "update_user_list" in client_message:
            print("[CLIENT-ADMIN] Requested to perform action update_user_list")
            time.sleep(1)
            print("[SERVER] Updating user list...")
            time.sleep(1)
            received_list = client_message.split("-")
            users = eval(received_list[1])
            # Rewrites the updated list into the file
            with open("./Data/userid_pswd.txt", "w") as file:
                for line in users:
                    file.write(str(line))
            print("[SERVER] User list updated!")
        
        if "clear" in client_message:
            print("[CLIENT-ADMIN] Requested to perform action clear")
            time.sleep(1)
            if "question_pool" in client_message:
                print("[SERVER] Clearing question pool...")
                with open("./Data/question_pool.txt", "w") as file:
                    file.write("")
                time.sleep(1)
                print("[SERVER] Question Pool cleared!")
            elif "results" in client_message:
                print("[SERVER] Clearing quiz attempts...")
                with open("./Data/quiz_results.txt", "w") as file:
                    file.write("")
                time.sleep(1)
                print("[SERVER] Quiz Attempts cleared!")
        
        if "update_question_list" in client_message:
            print("[CLIENT-ADMIN] Requested to perform action update_question_list")
            time.sleep(1)
            print("[SERVER] Updating the question pool...")
            time.sleep(1)
            received_list = client_message.split("§")
            question_list = eval(received_list[1])
            with open("./Data/question_pool.txt", "w") as file:
                for question in question_list:
                    file.write(str(question) + "\n")
            print("[SERVER] Question Pool updated!")
        
        if "update_settings" in client_message:
            print("[CLIENT-ADMIN] Requested to perform action update_settings")
            time.sleep(1)
            received_list = client_message.split("§")
            settings_dictionary = eval(received_list[1])
            with open("./Data/quiz_settings.txt", "w") as file:
                for key in settings_dictionary:
                    file.write(str(key)+":"+str(settings_dictionary[key])+"\n")
        
        if "export_user_csv_headers" in client_message:
            print("[CLIENT-ADMIN] Requested to perform the action export_user_csv_headers")
            time.sleep(1)
            received_list = client_message.split("§")
            data = received_list[1]
            print("[SERVER] Writing data to CSV file...")
            with open("./Data/quiz_report.csv", "w") as csv_file:
                csv_file.write(data + "\n")
            print("[SERVER] Exported CSV.")
        
        if "export_user_csv_data" in client_message:
            print("[CLIENT-ADMIN] Requested to perform action export_user_csv_data")
            time.sleep(1)
            received_list = client_message.split("§")
            data = received_list[1]
            print("[SERVER] Writing data to CSV file...")
            with open("./Data/quiz_report.csv", "a") as csv_file:
                csv_file.write(data + "\n")
            time.sleep(1)
            print('[SERVER] Exported CSV.')


                
# Function receive and validate the packets received from the client
def receive_input(connection, max_buffer_size):
    client_message = connection.recv(max_buffer_size)
    client_message_size = sys.getsizeof(client_message)
    if client_message_size > max_buffer_size:
        print(f"The input size is greater than expected {client_message_size}")
    
    decoded_message = client_message.decode("utf8").rstrip()
    return decoded_message

host = '127.0.0.1'  # Server IP
port = 8000         # Server Port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print("[SERVER] Socket Created")
try:
    # Bind server socket
    server_socket.bind((host, port))
    
    # Outputs server error message if socket bind failed
except:
    print("[SERVER] ERROR: Socket Bind failed!")
    sys.exit()  # Terminates the program if bind failed

server_socket.listen()     # queue up to 6 requests
print("[SERVER] Socket Now Listening...")   # Outputs message that server is listening for connections

# Multithreading
while True:
    # Accept connections from clients
    connection, client_address = server_socket.accept()     
    client_ip, client_port = str(client_address[0]), str(client_address[1])

    # Output client IP and Port connected
    print(f"[CLIENT] Connected to IP: {client_ip} Port: {client_port}")
    print(f"[CONNECTION COUNT] >>> {threading.active_count()}")     # Keeps track of how many threads are active (aka how many connected clients)
    
    try:
        Thread(target=client_thread, args=(connection, client_ip, client_port)).start()

    except:
        # Outputs if client did not start
        print("[CLIENT] ERROR: Client Thread did not start")
        traceback.print_exc()

server_socket.close()
