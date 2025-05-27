import socket, threading, json, select

'''A socket connection class to be used as a server'''
class Connection():
    def __init__(self):
        #Create a socket, bind, and listen
        self.HOST_IP = socket.gethostbyname(socket.gethostname())
        self.HOST_PORT = 12345
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.HOST_IP, self.HOST_PORT))
        self.server_socket.listen()

'''Server class that runs the whole server'''
class RunServer():
    def __init__(self, connection):
        #Assign internal variables
        self.ENCODER = 'utf-8'
        self.BYTESIZE = 10
        self.connection = connection
        self.pi_socket_list = []
        self.pi_address_list = []
        self.pi_connected_list = []
        self.piCount = 0
        self.recieving = True
        self.recieve_thread = None
        self.startGame = False

    '''Connects a pi to the server'''
    def connectPi(self, state):
        print("Listening for a new connection")
        #Connect the incoming pi and start a listening thread for incoming messages
        while len(self.pi_socket_list) < 2:
            pi_socket, pi_address = self.connection.server_socket.accept()
            print(pi_address, " connected.")
            pi_data = self.get_message(pi_socket)
            self.pi_socket_list.append(pi_socket)
            self.pi_address_list.append(pi_address)
            self.pi_connected_list.append({'socket': pi_socket, 'address': pi_address, 'client': pi_data["ID"]})
            self.pi_connected_list = sorted(self.pi_connected_list, key=lambda x: x['client'])
            self.piCount = len(self.pi_socket_list)
            if pi_data["ID"][:-1] == "player":
                state.addPlayer({'socket': pi_socket, 'address': pi_address, 'client': pi_data["ID"]}, self.send_message)
            elif pi_data["ID"] == "board":
                state.board = True

            self.recieve_thread = threading.Thread(target=self.recieve_message, args=(pi_socket, pi_address, state))
            self.recieve_thread.daemon = True
            self.recieve_thread.start()

    '''Removes a pi connected to the server'''
    def disconnectPi(self, pi_socket):
        index = self.pi_socket_list.index(pi_socket)
        print("Disconnecting: ", self.pi_address_list[index])
        self.piCount -= 1
        self.pi_socket_list.remove(pi_socket)
        self.pi_address_list.pop(index)
        pi_socket.close()
    
    def close(self):
        self.connection.server_socket.shutdown(socket.SHUT_RDWR)
        self.connection.server_socket.close()
        print ("closed")

    '''Send a message to ALL pis connected to the server'''
    def broadcast_message(self, message):
        message_json = json.dumps(message)
        header = str(len(message_json))
        while len(header) < self.BYTESIZE:
            header += " "
        for p in self.pi_connected_list:
            p['socket'].send(header.encode(self.ENCODER))
            p['socket'].send(message_json.encode(self.ENCODER))

    def send_message(self, client, message):
        message_json = json.dumps(message)
        header = str(len(message_json))
        while len(header) < self.BYTESIZE:
            header += " "
        for p in self.pi_connected_list:
            if p['client'] == client:
                p['socket'].send(header.encode(self.ENCODER))
                p['socket'].send(message_json.encode(self.ENCODER))

    def getHeader(self, message):
        message_json = json.dumps(message)
        header = str(len(message_json))
        while len(header) < self.BYTESIZE:
            header += " "
        return header, message_json

    def get_message(self, pi_socket):
        packet_size = pi_socket.recv(self.BYTESIZE).decode(self.ENCODER)
        pi_json = pi_socket.recv(int(packet_size))
        return json.loads(pi_json)

    '''Recive an incoming message from a pi'''
    def recieve_message(self, pi_socket, pi_address, state):
        while True:
            #Get a message_json from a pi
            packet_size = pi_socket.recv(self.BYTESIZE).decode(self.ENCODER)
            pi_json = pi_socket.recv(int(packet_size))
            pi_data = json.loads(pi_json)
            self.handle_message(pi_socket, pi_data,  state)
            '''try:
                
            except Exception:
                print("Message Revieving Error from: ", pi_address)
                self.recieving = False
                # press ctrl+c to exit
                for idx, player in enumerate(state.players):
                    if pi_socket == player.pi_socket:
                        del state.players[idx]
                if pi_socket in self.pi_socket_list:
                    self.pi_socket_list.remove(pi_socket)
                if pi_address in self.pi_address_list:
                    self.pi_address_list.remove(pi_address)
                self.piCount = len(self.pi_socket_list)
                self.connectPi(state)
                break
                '''
    '''Routes the message to the intended function'''
    def handle_message(self, pi_socket, message_json,  state):    
        #Get the message flag
        messageType = message_json["messageType"]
        print(message_json)
        #Disconnect pi from the server
        match messageType:
            case "DISCONNECT":
                self.disconnectPi(pi_socket)

            case "CHARACTER":
                print(message_json)

            case "MOVE":
                self.send_message('board', message_json)
                for idx, s in enumerate(self.pi_connected_list):
                    if s['socket'] == pi_socket:
                        state.activePlayer = int(message_json['player'][-1::])-1 
                        state.movePlayer(state.activePlayer, message_json)