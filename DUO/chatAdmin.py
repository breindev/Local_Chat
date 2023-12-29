from tkinter import*
from tkinter import ttk
import socket
import threading
class AppChat:
    def __init__(self) -> None:
        self.clients = []
        self.usernames = []
        self.window()

        Thread_server = threading.Thread(target=self.server)
        Thread_server.setDaemon(True)
        Thread_server.start()
    def window(self):
        root.title("Server - by Breindev | 2024")
        root.resizable(0,0)
        root.geometry(f"{int(root.winfo_screenwidth()/3)}x{int(root.winfo_screenheight()/2)}")
        self.active()
        self.chat()

    def active(self):
        # FRAME CONECTADO
        F_conectados = Frame(root,width=50)
        F_conectados.pack(expand=True,side=LEFT,fill=BOTH)
        Label(F_conectados,text="ACTIVO AHORA:",font=("arial",12,"bold"),bg="greenyellow",anchor=CENTER).pack(fill=BOTH)
        self.treeActive = ttk.Treeview(F_conectados, columns=("port","ip","username"),show="headings")
        self.treeActive.pack(expand=True,fill=BOTH)
        
        self.treeActive.column("port",width=40)
        self.treeActive.column("ip",width=60)
        self.treeActive.column("username",width=100)

        self.treeActive.heading("port", text = "PUERTO")
        self.treeActive.heading("ip", text = "IP")
        self.treeActive.heading("username", text = "USUARIO")

        def update_active():
            self.treeActive.delete(*self.treeActive.get_children())
            for i in self.usernames:
                self.treeActive.insert("", "end", text="", values=(i[1][1],i[1][0],i[0]))
                print(i[0],i[1],"")
            F_conectados.after(1000,update_active)    
        update_active()
    def chat(self):
        # FRAME CHAT
        self.icono = PhotoImage(file="DUO/send_icono.png")
        F_chat = Frame(root)
        F_chat.pack(expand=True,side=RIGHT,fill=BOTH)
        
        #----------------------------------------------------------------------------------
        Ftop = Frame(F_chat)
        Ftop.pack(side=TOP,fill=BOTH)
        
        self.L_user = Label(Ftop,text="",bg="turquoise",font=("arial",12,"bold"),anchor=CENTER)
        self.L_user.pack(expand=True,side=RIGHT,fill=BOTH)
        #----------------------------------------------------------------------------------

        self.treeChat = ttk.Treeview(F_chat, columns=("friend","yo"),show="")
        self.treeChat.pack(expand=True,fill=BOTH,side=TOP)
        self.treeChat.column("friend",width=120, anchor=W)
        self.treeChat.column("yo",width=120, anchor=E)

        #----------------------------------------------------------------------------------
        F_bottom_chat = Frame(F_chat)
        F_bottom_chat.pack(expand=True, fill=BOTH)
        self.messageText = Text(F_bottom_chat,width=20,height=1)
        self.messageText.pack(expand=True, fill=BOTH, side=LEFT)
        Button(F_bottom_chat,text="Enviar",bg="greenyellow",cursor="hand2",font=("arial",12,"bold"),image=self.icono,compound=TOP, command=lambda:(self.write_message(self.messageText.get("1.0","end-1c")),
                                                            self.messageText.delete("1.0","end"),
                                                            self.messageText.focus_set())).pack(side=RIGHT,expand=True,fill=BOTH)
        def update_label():
            try:
                self.L_user.config(text=self.usernames[0][0])
            except:
                pass    
            F_chat.after(1000,update_label)
        update_label()
        #----------------------------------------------------------------------------------
    def server(self):
        hostname = socket.gethostname()
        
        host = socket.gethostbyname(hostname)
        print(host)
        port = 5009
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()
        print("\n-------------------------------------------------")
        print(f"""    • SERVIDOR ACTIVADO • 
                            IP  : {host} 
                            PORT: {port}""")
        print("-------------------------------------------------\n")

        def handle_messages(client):
            while True:
                try :
                    message = client.recv(1024)
                    message_print = message.decode('utf-8') # DECODIFICAMOS PARA MOSTRAR INDEPENDIENTE A LA VARIABLE PASAJERA DE ARRIBA
                    
                    index = self.clients.index(client)
                    username = self.usernames[index]
                    if message_print == f"exit":
                        print(f"Admin: {username} se desconecto")
                        self.clients.remove(client)
                        self.usernames.remove(username)
                        client.close()
                        break
                    else:
                        self.treeChat.insert("", "end", text="", values=(message_print,""))
                        print(message_print)
                except:
                    break

        def receive_connections():
            while True:
                client, address = server.accept()

                client.send("@username".encode("utf-8")) # PIDE EL USUARIO AL CLIENTE CONECTADO
                username = client.recv(1024).decode('utf-8') # ESPERA LA RESPUESTA
                #GUARDA LOS DATOS RECIBIDOS:
                self.clients.append(client)
                self.usernames.append([username,address])

                print(f"{username} se conectó {str(address)}")
                thread = threading.Thread(target=handle_messages, args=(client,))
                thread.start()
        receive_connections()
    # ENVIA EL MESAJE AL CLIENTE CONECTADO AMBOS DATOS RECIBIDOS COMO PARÁMETRO
    def broadcast(self,message, _client): 
        _client.send(message)
        self.treeChat.insert("", "end", text="", values=("",message.decode('utf-8')))
    def write_message(self,message):
        # si existe un mensaje y un cliente conectado
        if len(message.replace(" ","")) != 0 and len(self.clients) != 0:
            self.broadcast(message.encode('utf-8'),self.clients[0])
        else:
            print("No ha escrito un mensaje o nadie está conectado")
if __name__ == "__main__":
    root = Tk()
    window = AppChat()
    root.mainloop()