# To create realworld objects

class Car:

    def __init__(self, regNo, color, noOfDoors, model):
        self.__regNo = regNo
        self.__color = color
        self.__noOfDoors = noOfDoors
        self.__model = model

    def getRegNo(self):
        return self.__regNo

    def getColor(self):
        return self.__color

    def getNoOfDoors(self):
        return self.__noOfDoors

    def getModel(self):
        return self.__model

class Manufacturer:

    def __init__(self, id, name):
        self.__name = name
        self.__id = id

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

class Model:

    def __init__(self, modelNo, name, price, manufacturer):
        self.__name = name
        self.__price = price
        self.__modelNo = modelNo
        self.__manufacturer = manufacturer

    def getModelNo(self):
        return self.__modelNo

    def getName(self):
        return self.__name

    def getPrice(self):
        return self.__price

    def getManufacturer(self):
        return self.__manufacturer

class Accessory:

    def __init__(self, id, name, price):
        self.__id = id
        self.__name = name
        self.__price = price

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getPrice(self):
        return self.__price

class Sale:

    def __init__(self, car_reg_no, timestamp, finalAmount):
        self.__car_reg_no = car_reg_no
        self.__timestamp = timestamp
        self.__finalAmount = finalAmount

    def getCarRegNo(self):
        return self.__car_reg_no

    def getTimestamp(self):
        return self.__timestamp

    def getFinalAmount(self):
        return self.__finalAmount

class Upgrade:

    def __init__(self, car_reg_no, accessory_id, quantity):
        self.__car_reg_no = car_reg_no
        self.__accessory_id = accessory_id
        self.__quantity = quantity

    def getCarRegNo(self):
        return self.__car_reg_no

    def getAccessoryId(self):
        return self.__accessory_id

    def getQuantity(self):
        return self.__quantity