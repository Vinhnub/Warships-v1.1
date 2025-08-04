from Player import *

class Data():

    def __init__(self, type, idRoom, data):
        self.__type = type # findmatch, isready, shooting, waiting, changeturn
        self.__idRoom = idRoom 
        self.__data = data

    def __str__(self):
        return str(self.__type) + " " + str(self.__idRoom) + " " + str(self.__data)

    def getData(self):
        return self.__data
    
    def getId(self):
        if self.__idRoom == None: return None
        return int(self.__idRoom)
    
    def setId(self, id):
        self.__idRoom = id
    
    def setData(self, data):
        self.__data = data

    def setType(self, type):
        self.__type = type

    def getType(self):
        return self.__type