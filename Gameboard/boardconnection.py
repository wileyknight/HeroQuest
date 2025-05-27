import socket, threading, json

class Connection():
    #Define constants to be used
    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        self.DEST_IP = socket.gethostbyname(socket.gethostname())
        self.DEST_PORT = 12345
        self.ENCODER = 'utf-8'
        self.BYTESIZE = 10
        self.running = False
        self.connected = False
        self.connCount = 0
        self.currentData = ""
        self.recieve_thread = None
        self.state = None
        
        #Create a client socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    '''Send a message to the server to be broadcast'''
    def send_message(self, message_packet):
        msg_json = json.dumps(message_packet)
        header = str(len(msg_json))
        while len(header) < self.BYTESIZE:
                header += " "
        self.client_socket.send(header.encode(self.ENCODER))
        self.client_socket.send(msg_json.encode(self.ENCODER))
    
    '''Disconnect the client from the server'''
    def disconnect(self):
        message_packet = {
            "messageType": "DISCONNECT",
        }
        self.send_message(message_packet)

    '''Recieve an incoming message from the server'''
    def recieve_message(self, state):
        while True:
            try:
                #Recieve data from the server.
                packet_size = self.client_socket.recv(self.BYTESIZE).decode(self.ENCODER)
                message_bytes = self.client_socket.recv(int(packet_size)).decode(self.ENCODER)
                message_json = json.loads(message_bytes)
                self.handle_message(message_json, state)
            except KeyboardInterrupt:
                print("Disconnecting from server")
                self.client_socket.close()
                self.running = False
                self.connected = False
                self.connCount = 0
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                break
            except:
                #An error occured, close the connection
                print("Server connection lost")
                self.client_socket.close()
                self.running = False
                self.connected = False
                self.connCount = 0
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                break
    
    '''Routes the message to the intended function'''
    def handle_message(self, message_json, state):
        #Find the message type
        messageType = message_json["messageType"]
        #Update the telemetry data
        print(message_json)
        match messageType:
            case 'PLAYERS':
                for p in message_json['players']:
                    state.addPlayer()

            case 'MAP':
                pass

            case 'INTRO':
                state.showSplash = False
                state.showIntro = True

            case 'START':
                state.showIntro = False
                state.showGame = True

            case 'MOVE':
                state.activePlayer = int(message_json['player'][-1::])-1 
                state.movePlayer(state.activePlayer, message_json)

            case 'OPEN':
                state.openDoor(message_json['door'])

    '''Start listening for incoming iRacing telemetry'''
    def on_enter(self, state):
        #Create a client socket
        try:
            self.client_socket.connect((self.DEST_IP, self.DEST_PORT))
            self.connected = True
            print('connection successful')
            self.send_message({'messageType':'ID', 'ID': 'board'})
            # Start the server data listener thread
            self.recieve_thread = threading.Thread(target=self.recieve_message, args=(state,))
            self.recieve_thread.daemon = True
            self.recieve_thread.start()
            print('Listening for game data')
        except KeyboardInterrupt:
            self.recieve_thread.join()
            self.connected = False
            self.disconnect()
        except:
            print('Did not connect')