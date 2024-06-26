import sys
import Server
import time

#######   BANKING PROJECT    #######'

STRING_LIST = ["create_account@222222",
               "deposit_cash@1320",
               "deposit_cash@1500",
               "open_app",
               "open_app",
               "log_in@2023123456@111111#1",
               "log_in@id@123456#2",
               "log_in@id@222222#2",
               "transfer_money@2023123456@1000#2",
               "withdraw_cash@1000@222222",
               "withdraw_cash@500@222222",
               "log_out#2",
               "log_in@2023123456@111111#2",
               "query#2",
               "query#1",
               "log_out#2",
               "close_app#2",
               "return_card",
               "insert_card@2023123456",
               "close_account",
               "transfer_money@id@1500",
               "close_account"
               ]




def testing(server:Server.ZmqServerThread):
    def is_received_new_message(oldTimeStamp:int, oldServerMessage:str, Msgunprocessed:bool = False)->bool:
        if(Msgunprocessed):
            return True
        else:
            if(oldTimeStamp == server.messageTimeStamp and 
            oldServerMessage == server.receivedMessage):
                return False
            else:
                return True
    
    ############ Initialize Passengers ############
    
    timeStamp = -1 #default time stamp is -1
    clientMessage = "" #default received message is ""
    messageUnprocessed = False #Used when receiving new message 
    count = 0

    
    ############ Send Message ############
    cardID = ""

    for i in range(len(STRING_LIST)):
        stringToSend = STRING_LIST[i]
        
        if("id" in stringToSend):
            stringToSend = stringToSend.replace("id",cardID)
        server.send_string(server.bindedClient,stringToSend)

        time.sleep(5)

        if (STRING_LIST[i].startswith("create_account")):
            if(is_received_new_message(timeStamp, clientMessage, messageUnprocessed)):
                clientMessage = server.receivedMessage
                cardID = clientMessage.split("@")[1]




if __name__ == "__main__":
    my_server = Server.ZmqServerThread()
    while(True):
        if(len(my_server.clients_addr) == 0):
            continue
        elif(len(my_server.clients_addr) >=2 ):
            print('more than 1 client address stored. server will exit')
            sys.exit()
        else:
            addr = list(my_server.clients_addr)[0]
            msg = input(f"start judging for {addr}?: (y/n)\n")
            if msg == 'y':
                my_server.bindedClient = addr
                testing(my_server)
            else:
                continue
