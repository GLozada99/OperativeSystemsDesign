import socket 
import time
import os 

class Client:
    def __init__(self):
        self.sock = None
        self.port = 0
        self.host = ""
        self._CONNECT = bytearray()
        self._PUBLISH = bytearray()
        self._SUBSCRIBE = bytearray()
        self._DISC = bytearray([224,0])
        self._SUBACK = b'\x90\x03\x00\x01\x00'#x90 por defecto, x03 porque faltan 3, x00 porque si, x01 porque falta 1, x00 porque qos maximo es 0
        self._PINGREQ = bytearray([0xC0,0x00])
        self.last_time = 0.0 
    
    def count_for_ping(self):
        if self.last_time == 0.0:
            self.last_time = time.time()
        else:
            time_elapsed = time.time() - self.last_time
            if time_elapsed > 55.0:
                self.sock.send(self._PINGREQ)
                self.last_time = time.time()   


    def connect(self, host='localhost',port=1883):
        self.port = port  # Reserve a port for your service every new transfer wants a new port or you must wait.
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.sock.send(self._CONNECT)
        return self.sock.recv(4)
    
    def disconnect(self):
        self.sock.send(self._DISC)
        self.sock.close()

    def set_connect_packet(self,id):
        id_len = len(id)
        
        total_len = id_len + 12
        
        CONNECT = [16,total_len,0,4,77,81,84,84,4,2,0,60,0,id_len]
        
        for ch in id:
            CONNECT.append(ord(ch))

        B_CONNECT = bytearray(CONNECT)
        
        self._CONNECT = B_CONNECT

class Publisher(Client):
    def set_publish_packet(self,topic,payload):
        payload_len = len(payload)
        topic_len = len(topic)
        total_len = 2 + payload_len + topic_len +2
        PUBLISH = [0x32, total_len, 0, topic_len]
        
        for ch in topic:
            PUBLISH.append(ord(ch))

        PUBLISH.append(0xAB)
        PUBLISH.append(0xCD)
           
        for ch in payload:
            PUBLISH.append(ord(ch))
        
        B_PUBLISH = bytearray(PUBLISH)
        self._PUBLISH = B_PUBLISH
    
    def publish(self):
        self.sock.send(self._PUBLISH)
        return self.sock.recv(4)

class Subscriber(Client):
    def set_subscribe_packquet(self,topic,qos=0):
        total_len = 5 + len(topic)
        SUBSCRIBE = [0x82, total_len]
        
        SUBSCRIBE.append(0)
        SUBSCRIBE.append(1)
        SUBSCRIBE.append(0)
        SUBSCRIBE.append(len(topic))
        for ch in topic:
            SUBSCRIBE.append(ord(ch))
        SUBSCRIBE.append(qos)
        

        B_SUBSCRIBE = bytearray(SUBSCRIBE)
        self._SUBSCRIBE = B_SUBSCRIBE
    
    def send_PINGREQ(self):
        self.sock.send(self._SUBSCRIBE)
        return self.sock.recv(4)
    def subscribe(self):
        self.sock.send(self._SUBSCRIBE)
        msg = self.sock.recv(10)
        if msg == self._SUBACK:
            if os.fork() > 0:
                while True:
                    try:
                        fixed_header = list(self.sock.recv(2))#getting fixed header
                        variable_size= fixed_header[1]#seccond byte of fh contains length of variable header
                        topic_message = list(self.sock.recv(variable_size))#getting vh
                        message_place = 2 + topic_message[1] #getting where in the vh is the message, the seccond byte contains it, adding 2
                        message = topic_message[message_place:] #getting the m&t
                        final_message = ''
                        for ch in message:
                            final_message += chr(ch)#the char function turn numbers into ascii characters
                        print(final_message)    
                    except:
                        pass
            else:
                while True: 
                    self.count_for_ping()
                    time.sleep(4.0)        


