from typing import List, Any, Tuple

import pymysql

# Takes information from vehicle registration page and inserts information into database
def registerVehicle(vin, licensePlate, make, model, year, color, lat, lng, status):
    conn = pymysql.connect(host="localhost", user="team12", password="pandapanda", db="team12_wego")
    cursor = conn.cursor()
    query = ("""INSERT INTO Vehicles(VIN, plateNumber, make, model, year, color, lat, lng, status) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');""")
    query = query % (vin, licensePlate, make, model, year, color, lat, lng, status)
    print(query)
    cursor.execute(query)
    conn.commit()
    print("Vehicle added successfully")
    conn.close()
    return "Successfully added vehicle to database"

#returns thq available vehicles from database
def getAvailableCars():
    #needs to be worked on last since it needs a new table from database for availability
    conn = pymysql.connect(host="localhost", user="team12", password="pandapanda", db="team12_wego")
    cursor = conn.cursor()
    query = ("SELECT status from Vehicles where status='AVAILABLE'")
    print(query)
    cursor.execute(query)
    conn.commit()
    conn.close()

#returns the location of the car from the latitude and longitude in the database (vehicle table)
def getCarLocation(vin):
    ## has to get car information passed to it such as what car the user wants to check
    conn = pymysql.connect(host="localhost", user="team12", password="pandapanda", db="team12_wego")
    cursor = conn.cursor()
    query = ("SELECT lat, lng from Vehicles where VIN='%s'")
    query = query % (vin)
    cursor.execute(query)
    print(query)
    cursor.execute(query)
    conn.commit()


#array of arrays that has the vin, the lat, and long.
def getAllVehicleLocations():
    vehicleLocationList = []


    conn = pymysql.connect(host="localhost", user="team12", password="pandapanda", db="team12_wego")
    cursor = conn.cursor()
    query = ("SELECT VIN, lat, lng from Vehicles")
    cursor.execute(query)
    conn.commit()
    rows = cursor.fetchall()
    print("query")
    print(query)
    print("rows")
    print(rows)
    vehicles = []
    for i in rows:
        vehicle = []
        vehicle.append(i[0])
        vehicle.append(float(i[1]))
        vehicle.append(float(i[2]))
        vehicles.append(vehicle)
    print(vehicles)
    return vehicles



    #gets all car information
def getAll():

    conn = pymysql.connect(host="localhost", user="team12", password="pandapanda", db="team12_wego")
    cursor = conn.cursor()
    query = ("SELECT * from Vehicles")
    cursor.execute(query)
    conn.commit()
    rows = cursor.fetchall()
    vehicles = []
    for i in rows:

        vin = i[0]
        plateNumber = i[1]
        make = i[2]
        model = i[3]
        year = i[4]
        color = i[5]
        lat = float(i[6])
        lng = float(i[7])
        status = i[8]

        vehicleInfo = {
                'VIN': vin,
                'Plate Number': plateNumber,
                'Make' : make,
                'Model' : model,
                'Year' : year,
                'Color' : color,
                'Lat' : lat,
                'Long': lng,
                'Status': status
                }
        vehicles.append(vehicleInfo)

    return vehicles

#returns specified car information (vehicle table)
def getCarInfo(vin):
    #need to get vin information from FM to select info. Will change but VIN is used for now
    conn = pymysql.connect(host="localhost", user="team12", password="pandapanda", db="team12_wego")
    cursor = conn.cursor()
    query = ("SELECT VIN, lisense plate no, vehicle make, vehicle model, vehicle year, vehicle color from Vehicles where VIN='%s';")
    query = query %(vin)
    cursor.execute(query)
    print(query)
    cursor.execute(query)
    conn.commit()
    print(query)
    conn.close()


