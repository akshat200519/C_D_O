# To deal with database

import random
import mysql.connector

from sub_files.classes import Model, Manufacturer, Car, Accessory, Sale, Upgrade


class Backend:

    def __init__(self):
        self.connection = None
        self.cursor = None

    def createConnection(self):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(host = 'localhost', database = 'database1', user = 'root', password = 'akshat')
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as e:
            print(e)

    def removeConnection(self):
        try:
            self.connection.close()
        except mysql.connector.Error as e:
            print(e)

    def createTables(self):
        try:
            self.cursor.execute("SET GLOBAL foreign_keys = ON")

            # Create the accessory table
            self.cursor.execute("""
            CREATE TABLE accessory (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10,2) NOT NULL
            )
            """)

            # Create the manufacturer table
            self.cursor.execute("""
            CREATE TABLE manufacturer (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )
            """)

            # Create the model table
            self.cursor.execute("""
            CREATE TABLE model (
                model_no VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                manufacturer VARCHAR(255) NOT NULL,
                CONSTRAINT fk_manufacturer FOREIGN KEY (manufacturer) REFERENCES Manufacturer(id) ON DELETE RESTRICT
            )
            """)

            # Create the car table
            self.cursor.execute("""
            CREATE TABLE car (
                reg_no VARCHAR(255) PRIMARY KEY,
                color VARCHAR(255) NOT NULL,
                no_of_doors INTEGER NOT NULL,
                model VARCHAR(255) NOT NULL,
                CONSTRAINT fk_model FOREIGN KEY (model) REFERENCES Model(model_no) ON DELETE RESTRICT
            )
            """)

            # Create the sale table
            self.cursor.execute("""
            CREATE TABLE sale (
                car_reg_no VARCHAR(255) PRIMARY KEY,
                timestamp DATETIME NOT NULL,
                final_amount DECIMAL(10,2) NOT NULL,
                CONSTRAINT fk_car FOREIGN KEY (car_reg_no) REFERENCES Car(reg_no)
            )
            """)

            # Create the upgrade table
            self.cursor.execute("""
            CREATE TABLE upgrade (
                car_reg_no VARCHAR(255),
                accessory_id VARCHAR(255) NOT NULL,
                quantity INT NOT NULL,
                PRIMARY KEY (car_reg_no, accessory_id),
                CONSTRAINT fk_accessory FOREIGN KEY (accessory_id) REFERENCES Accessory(id)
            )
            """)

            self.connection.commit()
            return "Done"
        except mysql.connector.Error as e:
            return e


    def removeTables(self):
        pass

    def viewModels(self, condition):
        models = []
        try:
            self.cursor.execute("SELECT * FROM model WHERE {}".format(condition))
            rows = self.cursor.fetchall()
            for row in rows:
                manufacturer = self.getManufacturer(row[3])
                models.append(Model(row[0], row[1], row[2], manufacturer))
        except mysql.connector.Error as e:
            return []
        return models


    def getModel(self, model_no):
        model = None
        try:
            self.cursor.execute("SELECT * FROM model WHERE model_no = '{}'".format(model_no))
            row = self.cursor.fetchone()
            if row is not None:
                manufacturer = self.getManufacturer(row[3])
                model = Model(row[0], row[1], row[2], manufacturer)
        except mysql.connector.Error as e:
            return None
        return model



    def addModel(self, model):
        con1 = model.getModelNo() == None or model.getModelNo().strip() == ""
        con2 = model.getName() == None or model.getName().strip() == ""
        con3 = model.getPrice() == None or model.getPrice() == 0
        con4 = model.getManufacturer() == None

        if con1 or con2 or con3 or con4:
            return "you have missed something"

        try:
            self.cursor.execute("INSERT INTO model VALUES ('{}', '{}', {}, '{}')".format(model.getModelNo(),
                                                                                    model.getName(),
                                                                                    model.getPrice(),
                                                                                    model.getManufacturer().getId()))
            self.connection.commit()
            return "Done"
        except mysql.connector.Error as e:
            return e

    def removeModel(self, model):
        con1 = model.getModelNo() == None or model.getModelNo().strip() == ""

        if con1:
            return "you have missed something"

        try:
            self.cursor.execute("DELETE FROM model WHERE model_no = '{}'".format(model.getModelNo()))
            self.connection.commit()
            return "Done"
        except mysql.connector.Error as e:
            return e

    def updateModel(self, model):
        con1 = model.getModelNo() == None or model.getModelNo().strip() == ""
        con2 = model.getName() == None or model.getName().strip() == ""
        con3 = model.getPrice() == None or model.getPrice() == 0
        con4 = model.getManufacturer() == None

        if con1 or con2 or con3 or con4:
            return "you have missed something"

        try:
            self.cursor.execute("UPDATE model SET name = '{}', price = {}, manufacturer = '{}' WHERE model_no = '{}'".format(model.getName(),
                                                                                                                    model.getPrice(),
                                                                                                                    model.getManufacturer().getId(),
                                                                                                                    model.getModelNo()))
            self.connection.commit()
            return "Done"
        except mysql.connector.Error as e:
            return e

    def viewManufacturers(self, condition):
        manufacturers = []
        try:
            self.cursor.execute("SELECT * FROM manufacturer WHERE {}".format(condition))
            rows = self.cursor.fetchall()
            for row in rows:
                manufacturers.append(Manufacturer(row[0], row[1]))
        except mysql.connector.Error as e:
            return manufacturers
        return manufacturers


    def getManufacturer(self, id):
        manufacturer = None
        try:
            self.cursor.execute("SELECT * FROM manufacturer WHERE id = '{}'".format(id))
            row = self.cursor.fetchone()
            if row is not None:
                manufacturer = Manufacturer(row[0], row[1])
        except mysql.connector.Error as e:
            return None
        return manufacturer

    def addManufacturer(self, manufacturer):
        con1 = manufacturer.getId() is None or manufacturer.getId().strip() == ""
        con2 = manufacturer.getName() is None or manufacturer.getName().strip() == ""
        if con1 or con2:
            return "you have missed something"

        try:
            self.cursor.execute("INSERT INTO manufacturer (id, name) VALUES (%s, %s)", (manufacturer.getId(), manufacturer.getName()))
            self.connection.commit()
            return "Done"
        except mysql.connector.Error as e:
            return e

    def removeManufacturer(self, manufacturer):
        con1 = manufacturer.getId() is None or manufacturer.getId().strip() == ""
        if con1:
            return "you have missed something"

        try:
            self.cursor.execute("DELETE FROM manufacturer WHERE id = %s", (manufacturer.getId()))
            self.connection.commit()
            return "Done"
        except mysql.connector.Error as e:
            return e

    def updateManufacturer(self, manufacturer):
        con1 = manufacturer.getId() is None or manufacturer.getId().strip() == ""
        con2 = manufacturer.getName() is None or manufacturer.getName().strip() == ""
        if con1 or con2:
            return "you have missed something"

        try:
            self.cursor.execute("UPDATE manufacturer SET name = %s WHERE id = %s", (manufacturer.getName(), manufacturer.getId()))
            self.connection.commit()
            return "Done"
        except mysql.connector.Error as e:
            return e

    def viewCars(self, condition):
        cars = []
        try:
            self.cursor.execute("SELECT * FROM car WHERE {}".format(condition))
            rows = self.cursor.fetchall()
            for row in rows:
                cars.append(Car(row[0], row[1], row[2], self.getModel(row[3])))
        except mysql.connector.Error as e:
            return cars
        return cars

    def addCar(self, car):
        con1 = car.getRegNo() is None or car.getRegNo().strip() == ""
        con2 = car.getColor() is None or car.getColor().strip() == ""
        con3 = car.getNoOfDoors() is None or car.getNoOfDoors() == 0
        con4 = car.getModel() is None

        if con1 or con2 or con3 or con4:
            return "you have missed something"

        try:
            self.cursor.execute("INSERT INTO car (reg_no, color, no_of_doors, model) VALUES (%s, %s, %s, %s)", (car.getRegNo(), car.getColor(), car.getNoOfDoors(), car.getModel().getModelNo()))
            self.connection.commit()
            return "Done"
        except mysql.connector.Error as e:
            return e


    def removeCar(self, car):
        con1 = car.getRegNo() is None or car.getRegNo().strip() == ""
        if con1:
            return "you have missed something"

        try:
            self.cursor.execute("DELETE FROM car WHERE reg_no = %s", (car.getRegNo(),))
            self.connection.commit()
            return "Done"
        except mysql.connector.Error as e:
            return e

    def viewAccessories(self, condition):
        accessories = []
        try:
            self.cursor.execute("SELECT * FROM accessory WHERE {}".format(condition))
            rows = self.cursor.fetchall()
            for row in rows:
                accessories.append(Accessory(row[0], row[1], row[2]))
        except mysql.connector.Error as e:
            return accessories
        return accessories

    def getAccessory(self, id):
        accessory = None
        try:
            self.cursor.execute("SELECT * FROM accessory WHERE id = '{}'".format(id))
            row = self.cursor.fetchone()
            if row is not None:
                accessory = Accessory(row[0], row[1], row[2])
        except mysql.connector.Error as e:
            return None
        return accessory

    def addAccessory(self, accessory):
        con1 = accessory.getId() is None or accessory.getId().strip() == ""
        con2 = accessory.getName() is None or accessory.getName().strip() == ""
        con3 = accessory.getPrice() is None or accessory.getPrice() == 0

        if con1 or con2 or con3:
            return "you have missed something"

        try:
            self.cursor.execute("INSERT INTO accessory (id, name, price) VALUES (%s, %s, %s)", (accessory.getId(), accessory.getName(), accessory.getPrice()))
            self.connection.commit()
            return "Done"
        except mysql.connector.Error as e:
            return e

    def removeAccessory(self, accessory):
        con1 = accessory.getId() is None or accessory.getId().strip() == ""

        if con1:
            return "you have missed something"

        try:
            self.cursor.execute("DELETE FROM accessory WHERE id = %s", (accessory.getId(),))
            self.connection.commit()
            return "Done"
        except mysql.connector.Error as e:
            return e

    def updateAccessory(self, accessory):
        con1 = accessory.getId() is None or accessory.getId().strip() == ""
        con2 = accessory.getName() is None or accessory.getName().strip() == ""
        con3 = accessory.getPrice() is None or accessory.getPrice() == 0

        if con1 or con2 or con3:
            return "you have missed something"

        try:
            self.cursor.execute("UPDATE accessory SET name = '%s', price = %s WHERE id = '%s'" % (accessory.getName(), accessory.getPrice(), accessory.getId()))
            self.connection.commit()
            return "Done"
        except mysql.connector.Error as e:
            return e

    def addSale(self, sale, upgrades):
        con1 = sale.getCarRegNo() is None or sale.getCarRegNo().strip() == ""
        con2 = sale.getTimestamp() is None
        con3 = sale.getFinalAmount() is None or sale.getFinalAmount() == 0

        if con1 or con2 or con3:
            return "you have missed something"

        try:
            self.cursor.execute("INSERT INTO sale (car_reg_no, timestamp, final_amount) VALUES (%s, %s, %s)", (sale.getCarRegNo(), sale.getTimestamp(), sale.getFinalAmount()))

            for up in upgrades:
                self.cursor.execute("INSERT INTO upgrade (car_reg_no, accessory_id, quantity) VALUES (%s, %s, %s)", (up.getCarRegNo(), up.getAccessoryId(), up.getQuantity()))

            self.cursor.execute("DELETE FROM car WHERE reg_no = %s", (sale.getCarRegNo()))
            self.connection.commit()
            return "Done"
        except mysql.connector.Error as e:
            return e

    def viewSale(self, condition):
        sales = []
        try:
            self.cursor.execute("SELECT * FROM sale WHERE {}".format(condition))
            rows = self.cursor.fetchall()
            for row in rows:
                sales.append(Sale(row[0], row[1], row[2]))
        except mysql.connector.Error as e:
            return sales
        return sales

    def getUpgrades(self, id):
        upgrades = []
        try:
            self.cursor.execute("SELECT * FROM upgrade WHERE car_reg_no = '%s'" % id)
            rows = self.cursor.fetchall()
            for row in rows:
                upgrades.append(Upgrade(row[0], row[1], row[2]))
        except mysql.connector.Error as e:
            return upgrades
        return upgrades


