from tkinter import*
from tkinter import ttk
import socket
import threading

class AppChat:
    def __init__(self) -> None:
        self.username = "BREINDEV"
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # SOCKET PARA LADO DEL CLIENTE
        self.widget()
        self.server()
        root.protocol("WM_DELETE_WINDOW",lambda:self.delete_window()) # PROTOCOLO QUE FINALIZA LA CONEXIÓN AL CERRAR LA VENTANA
    def delete_window(self):
        try:
            self.write_message("exit")
            root.quit()
        except:
            root.quit()
    def widget(self):
        root.title("Client - by Breindev | 2024")
        root.resizable(0,0)
        root.geometry(f"{int(root.winfo_screenwidth()/3)}x{int(root.winfo_screenheight()/2)}")
        self.chat()

    def chat(self):
        # FRAME CHAT
        self.icono = PhotoImage(file="DUO/send_icono.png")
        F_chat = Frame(root)
        F_chat.pack(expand=True,side=RIGHT,fill=BOTH)
        
        #----------------------------------------------------------------------------------
        Ftop = Frame(F_chat)
        Ftop.pack(side=TOP,fill=BOTH)
        
        L_user = Label(Ftop,text=self.username,bg="greenyellow",font=("arial",12,"bold"),anchor=W)
        L_user.pack(expand=True,side=RIGHT,fill=BOTH)
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
        Button(F_bottom_chat,text="Enviar",bg="greenyellow",font=("arial",12,"bold"),image=self.icono,compound=TOP,
               command=lambda:(self.write_message(self.messageText.get("1.0","end-1c")),
                                                           self.messageText.delete("1.0","end"),
                                                           self.messageText.focus_set())).pack(side=RIGHT,expand=True,fill=BOTH)
        #----------------------------------------------------------------------------------
    def server(self):
        # IP Y PUERTO DEL SERVIDOR  A CONECTAR
        host = "192.168.229.32"
        port = 5009
        self.client.connect((host,port)) # DATOS A DONDE SE CONECTARA EL CLIENTE
        def recive_message():
            while True:    # PARA QUE ESTE SIEMPRE A LA ESCUCHA DE NUEVOS MENSAJES DEL SERVIDOR
                try:
                    # RECIBE EL MENSAJE DEL SERVIDOR
                    message = self.client.recv(1024).decode('utf-8')
                    # CONFIRMAR SI EL SERVIDOR NOS PIDE EL USURARIO
                    if message == "@username": # SI EL MENSAJE QUE ENVIO EL SERVIDOR ES IGUAL A @username ENVIAMOS NUESTRO USERNAME
                        self.client.send(self.username.encode('utf-8'))
                    else: # DE LO CONTRARIO MUESTRA EL MENSAJE EN CONSOLA E INTERFAZ
                        print(message) 
                        self.treeChat.insert("", "end", text="", values=(message,""))
                except:
                    print("ocurrió un error")
                    self.client.close()
                    break
        recive_Thread = threading.Thread(target=recive_message)
        recive_Thread.setDaemon(True)
        recive_Thread.start()
    # FUNCION PARA ENVUAR LOS MENSAJES AL SERVIDOR
    def broadcast(self,message, _client):
        _client.send(message)
        self.treeChat.insert("", "end", text="", values=("",message.decode('utf-8')))
    def write_message(self,message):
        self.broadcast(message.encode('utf-8'), self.client)

if __name__ == "__main__":
    root = Tk()
    window = AppChat()
    root.mainloop()