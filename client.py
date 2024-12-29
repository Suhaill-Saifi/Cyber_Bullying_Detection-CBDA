import socket
import select
import sys
import time
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer

model = pickle.load(open("/Users/suhailsaifi/Downloads/CBDA/Safe_Chat/LinearSVC.pkl", 'rb'))
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = "127.0.0.1"
port = 12345

server.connect((IP_address, port))
print("Connected To server")

user_id = input("Type user id: ")
room_id = input("Type room id: ")

server.send(str.encode(user_id))
time.sleep(0.1)
server.send(str.encode(room_id))

def prettyPrinter(data_1):
    # Load stopwords
    with open("/Users/suhailsaifi/Downloads/CBDA/Safe_Chat/stopwords.txt", "r") as my_file:
        content = my_file.read()
        content_list = content.split("\n")

    tfidf_vector = TfidfVectorizer(stop_words=content_list, lowercase=True,
                                     vocabulary=pickle.load(open("/Users/suhailsaifi/Downloads/CBDA/Safe_Chat/tfidf_vector_vocabulary.pkl", "rb")))
    data_2 = tfidf_vector.fit_transform([data_1])
    pred = model.predict(data_2)

    if pred == 0:
        return data_1, False  # Not bullying
    else:
        return None, True  # Bullying detected

while True:
    socket_list = [sys.stdin, server]
    read_socket, write_socket, error_socket = select.select(socket_list, [], [])

    for socks in read_socket:
        if socks == server:
            message = socks.recv(1024).decode()

            if message == "Bullying message detected. It has been hidden.":
                print(message)
            else:
                print(message)

        else:
            message = sys.stdin.readline().strip()

            if message == "FILE":
                file_name = input("Enter the file name: ")
                server.send("FILE".encode())
                time.sleep(0.1)
                server.send(str("client_" + file_name).encode())
                time.sleep(0.1)
                server.send(str(os.path.getsize(file_name)).encode())
                time.sleep(0.1)

                with open(file_name, "rb") as file:
                    data = file.read(1024)
                    while data:
                        server.send(data)
                        data = file.read(1024)
                sys.stdout.write("<You> File sent successfully\n")
                sys.stdout.flush()
            else:
                processed_message, is_bullying = prettyPrinter(message)

                if is_bullying:
                    server.send("Bullying message detected. It has been hidden.".encode())
                    print("Stop bullying people and behave decently.")
                else:
                    server.send(processed_message.encode())
                    sys.stdout.write("<You> " + processed_message + "\n")
                    sys.stdout.flush()

server.close()
