import socket
from _thread import *
import pickle
from Signal import *


server = str(input("Enter ip:"))
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(10)
print("=========================================")
print("Server started. Waiting for connection!")

playerId = 0
dictData = {}

def printDict(dict):
    for id in dict:
        for playerid in dict[id]:
            print("id:", id, "playerid:", playerid, "data:", dict[id][playerid])

def getDataFromEnermy(roomId, playerId):
    global dictData
    for player in dictData[roomId]:
        if player != playerId:
            return dictData[roomId][player]


def threaded_client(conn, playerId):
    global dictData
    conn.send(str.encode("hello"))
    reply = Signal("", None, None)
    while True:
        try:
            data = pickle.loads(conn.recv(2048)) 
            if not data:
                print("Disconnected")
                break
            else: 
                # a condition data.getId() != None to advoid case player join match but not fill idroom in input field
                if data.getType() == "findmatch" and data.getId() != None:
                    if data.getId() not in dictData:
                        if data.getData() == True: dictData[data.getId()] = {playerId : data}
                    else:
                        dictData[data.getId()][playerId] = data
                    if data.getId() in dictData:
                        if len(dictData[data.getId()]) == 2:
                            reply = getDataFromEnermy(data.getId(), playerId)
                            
                # this condition to check enermy is ready to start game
                elif data.getType() == "isready":
                    dictData[data.getId()][playerId] = data
                    reply = getDataFromEnermy(data.getId(), playerId)

                elif data.getId() != None and data.getType() != "findmatch":
                    dictData[data.getId()][playerId] = data
                    reply = getDataFromEnermy(data.getId(), playerId)


            conn.send(pickle.dumps(reply))
        except:
            break
    print("Close connection")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to", addr)
    
    start_new_thread(threaded_client, (conn, playerId))
    playerId += 1

