import socket
from _thread import start_new_thread
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import time


model = pickle.load(open("/Users/suhailsaifi/Downloads/CBDA/Safe_Chat/LinearSVC.pkl", 'rb'))

class Server:
    def __init__(self):
        self.rooms = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def accept_connections(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.server.bind((self.ip_address, int(self.port)))
        self.server.listen(100)

        print(f"Server started on {self.ip_address}:{self.port}")

        while True:
            connection, address = self.server.accept()
            print(f"{address[0]}:{address[1]} Connected")
            start_new_thread(self.clientThread, (connection,))

    def clientThread(self, connection):
        try:
            user_id = connection.recv(1024).decode().replace("User ", "")
            room_id = connection.recv(1024).decode().replace("Join ", "")

            if room_id not in self.rooms:
                self.rooms[room_id] = []
                connection.send("New Group created".encode())
            else:
                connection.send("Welcome to chat room".encode())

            self.rooms[room_id].append(connection)

            while True:
                try:
                    message = connection.recv(1024)
                    if message:
                        if message.decode() == "FILE":
                            self.broadcastFile(connection, room_id, user_id)
                        else:
                            pred = self.prettyPrinter(message.decode())
                            message_to_send = f"<{user_id}> {message.decode()}"
                            self.broadcast(message_to_send, connection, room_id, pred)
                    else:
                        self.remove(connection, room_id)
                except (BrokenPipeError, ConnectionResetError) as e:
                    print(f"Connection error: {e}")
                    self.remove(connection, room_id)
                    break
                except Exception as e:
                    print(repr(e))
                    print("Client disconnected earlier")
                    break
        finally:
            connection.close()

    def broadcastFile(self, connection, room_id, user_id):
        file_name = connection.recv(1024).decode()
        lenOfFile = connection.recv(1024).decode()

        for client in self.rooms[room_id]:
            if client != connection:
                try:
                    client.send("FILE".encode())
                    time.sleep(0.1)
                    client.send(file_name.encode())
                    time.sleep(0.1)
                    client.send(lenOfFile.encode())
                    time.sleep(0.1)
                    client.send(user_id.encode())
                except:
                    client.close()
                    self.remove(client, room_id)

        total = 0
        while str(total) != lenOfFile:
            data = connection.recv(1024)
            total += len(data)
            for client in self.rooms[room_id]:
                if client != connection:
                    try:
                        client.send(data)
                        time.sleep(0.1)
                    except:
                        client.close()
                        self.remove(client, room_id)

    def prettyPrinter(self, data_1):
        try:
            with open("/Users/suhailsaifi/Downloads/CBDA/Safe_Chat/stopwords.txt", "r") as my_file:
                content = my_file.read()
                content_list = content.split("\n")
            
            tfidf_vector = TfidfVectorizer(stop_words=content_list, lowercase=True, vocabulary=pickle.load(open("/Users/suhailsaifi/Downloads/CBDA/Safe_Chat/tfidf_vector_vocabulary.pkl", "rb")))
            data_2 = tfidf_vector.fit_transform([data_1])
            pred = model.predict(data_2)
            
            if pred == 0:
                print('Non-bullying')
            else:
                print("Stop bullying people and behave decently.")
            
            return pred
        except Exception as e:
            print(f"Error in prettyPrinter: {e}")
            return -1  # Default to an invalid prediction

    def broadcast(self, message_to_send, connection, room_id, pred):
        for client in self.rooms[room_id]:
            if client != connection:
                try:
                    if pred == 0:
                        client.send(message_to_send.encode())
                    else:
                        client.send("Bullying message detected it has been hidden".encode())
                except:
                    client.close()
                    self.remove(client, room_id)

    def remove(self, connection, room_id):
        if connection in self.rooms.get(room_id, []):
            self.rooms[room_id].remove(connection)
            connection.close()

if __name__ == "__main__":
    ip_address = "127.0.0.1"
    port = 12345

    server = Server()
    server.accept_connections(ip_address, port)
