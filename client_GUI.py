import warnings
from sklearn.base import InconsistentVersionWarning

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

import socket
import tkinter as tk
from tkinter import filedialog
import time
import threading
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer

class GUI:
    
    def __init__(self, ip_address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip_address, port))

        self.Window = tk.Tk()
        self.Window.withdraw()

        self.login = tk.Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=350)

        self.pls = tk.Label(self.login, text="Please Login to a chatroom", justify=tk.CENTER, font="Arial 16 bold")
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.userLabelName = tk.Label(self.login, text="Username: ", font="Helvetica 14")
        self.userLabelName.place(relheight=0.2, relx=0.1, rely=0.25)

        self.userEntryName = tk.Entry(self.login, font="Helvetica 12")
        self.userEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.35, rely=0.30)
        self.userEntryName.focus()

        self.roomLabelName = tk.Label(self.login, text="Room Id: ", font="Helvetica 14")
        self.roomLabelName.place(relheight=0.2, relx=0.1, rely=0.40)

        self.roomEntryName = tk.Entry(self.login, font="Helvetica 11", show="*")
        self.roomEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.35, rely=0.45)
        
        self.go = tk.Button(self.login, text="CONTINUE", font="Helvetica 14 bold", command=lambda: self.goAhead(self.userEntryName.get(), self.roomEntryName.get()))
        self.go.place(relx=0.35, rely=0.62)

        self.Window.mainloop()

    def goAhead(self, username, room_id=0):
        self.name = username
        self.server.send(str.encode(username))
        time.sleep(0.1)
        self.server.send(str.encode(room_id))
        
        self.login.destroy()
        self.layout()

        rcv = threading.Thread(target=self.receive) 
        rcv.start()

    def layout(self):
        self.Window.deiconify()
        self.Window.title("ChatGuard")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg="#17202A")
        self.chatBoxHead = tk.Label(self.Window, bg="#D2E0FB", fg="#181C14", text=self.name, font="Helvetica 20 bold", pady=6)
        self.chatBoxHead.place(relwidth=1)

        self.line = tk.Label(self.Window, width=450, height=1, bg="#ABB2B9") 
        self.line.place(relwidth=1, rely=0.07, relheight=0.012) 

        self.textCons = tk.Text(self.Window, width=20, height=2, bg="#ECDFCC", fg="#181C14", font="Helvetica 14", padx=5, pady=5) 
        self.textCons.place(relheight=0.845, relwidth=1, rely=0.08) 
# 0.745
        self.labelBottom = tk.Label(self.Window, bg="#ABB2B9", height=80) 
        self.labelBottom.place(relwidth=1, rely=0.88) 
# 0.8
        self.entryMsg = tk.Entry(self.labelBottom, bg="#D2E0FB", fg="#181C14", font="Helvetica 16")
        self.entryMsg.place(relwidth=0.74, relheight=0.03, rely=0.008, relx=0.011) 
        self.entryMsg.focus()

        # Bind the Enter key to send the message
        self.entryMsg.bind("<Return>", lambda event: self.sendButton(self.entryMsg.get()))

        self.buttonMsg = tk.Button(self.labelBottom, text="Send", font="Helvetica 14 bold", width=20, bg="#ABB2B9", command=lambda: self.sendButton(self.entryMsg.get())) 
        self.buttonMsg.place(relx=0.77, rely=0.008, relheight=0.03, relwidth=0.22) 

        self.textCons.config(cursor="arrow")
        scrollbar = tk.Scrollbar(self.textCons) 
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=tk.DISABLED)

    def sendButton(self, msg):
        self.textCons.config(state=tk.DISABLED) 
        self.msg = msg 
        self.entryMsg.delete(0, tk.END) 
        snd = threading.Thread(target=self.sendMessage) 
        snd.start() 

    def receive(self):
        while True:
            try:
                message = self.server.recv(1024).decode()

                if str(message) == "FILE":
                    file_name = self.server.recv(1024).decode()
                    lenOfFile = self.server.recv(1024).decode()
                    send_user = self.server.recv(1024).decode()

                    if os.path.exists(file_name):
                        os.remove(file_name)

                    total = 0
                    with open(file_name, 'wb') as file:
                        while str(total) != lenOfFile:
                            data = self.server.recv(1024)
                            total += len(data)     
                            file.write(data)
                    
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state=tk.NORMAL)
                    self.textCons.insert(tk.END, "<" + str(send_user) + "> " + file_name + " Received\n\n")
                    self.textCons.config(state=tk.DISABLED) 
                    self.textCons.see(tk.END)

                else:
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state=tk.NORMAL)
                    self.textCons.insert(tk.END, message + "\n\n") 
                    self.textCons.config(state=tk.DISABLED) 
                    self.textCons.see(tk.END)

            except: 
                print("An error occurred!") 
                self.server.close() 
                break

    def sendMessage(self):
        self.textCons.config(state=tk.DISABLED) 
        while True:  
            self.server.send(self.msg.encode())
            self.textCons.config(state=tk.NORMAL)
            self.msg = self.prettyPrinter(self.msg)
            self.textCons.insert(tk.END, "<You> " + self.msg + "\n\n") 
            self.textCons.config(state=tk.DISABLED) 
            self.textCons.see(tk.END)
            break

    def prettyPrinter(self, data_1):
        # Load stopwords
        my_file = open("/Users/suhailsaifi/Downloads/CBDA/Safe_Chat/stopwords.txt", "r")
        content = my_file.read()
        content_list = content.split("\n")
        my_file.close()
        
        tfidf_vector = TfidfVectorizer(stop_words=content_list, lowercase=True, vocabulary=pickle.load(open("/Users/suhailsaifi/Downloads/CBDA/Safe_Chat/tfidf_vector_vocabulary.pkl", "rb")))
        data_2 = tfidf_vector.fit_transform([data_1])
        
        # Print sparse matrix and shape
        print(data_2)  # Sparse matrix output
        print(data_2.shape)  # Shape of the matrix

        model = pickle.load(open("/Users/suhailsaifi/Downloads/CBDA/Safe_Chat/LinearSVC.pkl", 'rb'))
        pred = model.predict(data_2)
        
        if pred == 0:
            print("Non bullying")  # Print to terminal
            return data_1
        else:
            print("Bullying detected")  # Print to terminal
            return "Stop bullying people and behave decently."

if __name__ == "__main__":
    ip_address = "127.0.0.1"
    port = 12345
    g = GUI(ip_address, port)
