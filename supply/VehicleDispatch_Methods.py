from urllib import parse
import json
import pymysql
import requests

# Print statements are made within the API methods to aid in debugging
# with the use of the command console.
class methods:

    @staticmethod
    def parsePostPath(path):
        print('Inside parsePostPath:' + '\n')

        path_parse = parse.urlparse(path)
        i = 0
        while path_parse[i]:
            print('Result of path parse at i: ' + path_parse[i] + ' ' + i.__str__() + '\n')
            i += 1
        path = path_parse[2]
        print('Path of url: ' + path + '\n\n')
        if path != "/supply/requestv" and path != "/supply/testRoute" and path != "/supply/updateV_Complete_Route_Distance" and path != "/supply/updateV_Location" and path != "/supply/updateV_Complete_Route_ETA" and path != "/supply/updateV_Real_Time_ETA" and path != "/supply/updateV_Is_Route_Complete" and path != "/home/supplyside/dashboard/register":
            raise Exception("Not a valid POST request path.")
        return path

    @staticmethod
    def parseGetPath(path):
        print('Inside parseGetPath:' + '\n')

        path_parse = parse.urlparse(path)
        i = 0
        while path_parse[i]:
            print('Result of path parse at i: ' + path_parse[i] + ' ' + i.__str__() + '\n')
            i += 1
        path = path_parse[2]
        print('Path of url: ' + path + '\n\n')
        if path != "/supply/testDispatch" and path != "/supply/getRealTimeETA" and path != "/home/supplyside/dashboard/tableview" and path != "/home/supplyside/dashboard/mapview":
            raise Exception("Not a valid GET request path.")
        return path

    @staticmethod
    def getOrderJSON(post_body):

        post_dict = json.loads(post_body)
        order_id = post_dict.get("orderID")
        ptype = post_dict.get("ptype")
        dloc = post_dict.get("dloc")
        ploc = post_dict.get("ploc")
        username = post_dict.get("username")
        print(order_id)
        print(ptype)
        print(dloc)
        print(ploc)
        print(username)

        return post_dict

    @staticmethod
    def getMapJSON(post_body):

        print(str(post_body))
        post_dict = json.loads(post_body)
        origin = post_dict.get("origin")
        dloc = post_dict.get("dloc")
        ploc = post_dict.get("ploc")
        print(origin)
        print(dloc)
        print(ploc)

        return post_dict

    @staticmethod
    def getDistanceJSON(post_body):
        print(str(post_body))
        post_dict = json.loads(post_body)
        distance = post_dict.get("distance")
        print(distance)

        return post_dict

    @staticmethod
    def getLocationJSON(post_body):
        print(str(post_body))
        post_dict = json.loads(post_body)
        lat = post_dict.get("lat")
        long = post_dict.get("long")
        print(lat)
        print(long)

        return post_dict

    @staticmethod
    def getCompETAJSON(post_body):
        print(str(post_body))
        post_dict = json.loads(post_body)
        compETA = post_dict.get("compETA")
        print(compETA)

        return post_dict

    @staticmethod
    def getCurrETAJSON(post_body):
        print(str(post_body))
        post_dict = json.loads(post_body)
        currETA = post_dict.get("currETA")
        print(currETA)

        return post_dict

    @staticmethod
    def getRouteBoolJSON(post_body):
        print(str(post_body))
        post_dict = json.loads(post_body)
        routeBool = post_dict.get("routeBool")
        print(routeBool)

        return post_dict

    @staticmethod
    def getOrderIDJSON(post_body):
        print(str(post_body))
        post_dict = json.loads(post_body)
        orderID = post_dict.get("orderID")
        print(orderID)

        return post_dict

    @staticmethod
    def getOrigin(map_json):
        print('Inside getOrigin:' + '\n')
        origin = map_json.get("origin")
        print('Origin: ' + origin + '\n\n')
        return origin

    @staticmethod
    def getDistance(distance_json):
        print('Inside getDistance:' + '\n')
        distance = distance_json.get("distance")
        print('Distance: ' + distance + '\n\n')
        return distance

    @staticmethod
    def getVIN(location_json):
        print('Inside getVIN:' + '\n')
        VIN = str(location_json.get("vin"))
        print('Vehicle VIN: ' + str(VIN) + '\n\n')
        return VIN

    @staticmethod
    def getVLat(location_json):
        print('Inside getVLat:' + '\n')
        lat = location_json.get("lat")
        print('Vehicle lat: ' + lat + '\n\n')
        return lat

    @staticmethod
    def getVLong(location_json):
        print('Inside getVLong:' + '\n')
        long = location_json.get("long")
        print('Vehicle long: ' + long + '\n\n')
        return long

    @staticmethod
    def getCompETA(compETA_json):
        print('Inside getCompETA:' + '\n')
        compETA = compETA_json.get("compETA")
        print('Complete ETA: ' + compETA + '\n\n')
        return compETA

    @staticmethod
    def getCurrETA(currETA_json):
        print('Inside getCurrETA:' + '\n')
        currETA = currETA_json.get("currETA")
        print('Current ETA: ' + currETA + '\n\n')
        return currETA

    @staticmethod
    def getRouteBool(routeBool_json):
        print('Inside getRouteBool:' + '\n')
        routeBool = routeBool_json.get("routeBool")
        print('Route Complete: ' + routeBool + '\n\n')
        return routeBool

    # Returns Delivery Location stored in JSON dict
    @staticmethod
    def getOrderID(json):
        print('Inside getOrderID:' + '\n')
        orderID = json.get("orderID")

        if not isinstance(orderID, int):
            raise Exception("orderID must be an int.")

        print('Order ID: ' + str(orderID) + '\n\n')
        return orderID


    # Gets payload type from JSON dict
    # Only accepts a value of 'veg' or 'clothes'
    @staticmethod
    def getPayload(json):
        print('Inside getPayload:' + '\n')
        # Get ptype from json dict
        ptype = json.get("ptype")

        if ptype != "veg" and ptype != "clothes":
            raise Exception("Not a valid parameter for vehicle request.")

        print('Payload type: ' + ptype + '\n\n')
        return ptype

    # Returns Delivery Location stored in JSON dict
    @staticmethod
    def getDeliveryLocation(json):
        print('Inside getDeliveryLocation:' + '\n')
        dloc = json.get("dloc")
        print('Delivery location: ' + dloc + '\n\n')
        return dloc

    # Returns Payload Location stored in JSON dict
    @staticmethod
    def getPayloadLocation(json):
        print('Inside getPayloadLocation:' + '\n')
        ploc = json.get("ploc")
        print('Payload location: ' + ploc + '\n\n')
        return ploc

    # Returns Payload Location stored in JSON dict
    @staticmethod
    def getUsername(json):
        print('Inside getUsername:' + '\n')
        username = json.get("username")
        print('Username: ' + username + '\n\n')
        return username

    @staticmethod
    def getRealTimeETA(orderID):
        print('Inside getRealTimeETA:' + '\n')

        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='team12',
                                     password='pandapanda',
                                     db='team12_wego',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Read a single record for test purposes
                sql = "SELECT `real_time_ETA` FROM `Dispatch_Records` WHERE `orderID`=%s"
                cursor.execute(sql, (orderID))
                result = cursor.fetchone()

        finally:
            cursor.close()
            connection.close()
        realTimeETA = result["real_time_ETA"]
        print('Real time ETA: ' + str(realTimeETA) + '\n\n')
        return realTimeETA

    @staticmethod
    def createRoute(origin, ploc, dloc):
        print('Inside createRoute:' + '\n')
        http = 'https://maps.googleapis.com/maps/api/directions/json?'

        params = dict(
            origin=origin,
            destination=dloc,
            waypoints=ploc,
            key='?'
        )

        data = requests.get(url=http, params=params)

        binary = data.content
        route = json.loads(binary)

        if route.get('status') != "NOT_FOUND":
            print(str(route))
        else:
            print('INVALID ADDRESS ENTERED!')
        return route

    @staticmethod
    def updateDispatchETA(VIN, compETA):
        print('Inside updateDispatchETA:' + '\n')
        compETA = int(compETA, 10)
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='team12',
                                     password='pandapanda',
                                     db='team12_wego',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Read a single record for test purposes
                sql = "UPDATE `Dispatch_Records` SET `ETA`=%s WHERE `VIN`=%s AND `status`=%s"
                cursor.execute(sql, (compETA, VIN, 'IN PROGRESS'))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            with connection.cursor() as cursor:
                # Read a single record for test purposes
                sql = "SELECT `ETA` FROM `Dispatch_Records` WHERE `VIN`=%s AND `status`=%s"
                cursor.execute(sql, (VIN, 'IN PROGRESS'))
                result = cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

        print('Updated Dispatch ETA with VIN:' + str(VIN) + ', to ' + str(compETA) + ' minutes.')
        print('Result: ETA = ' + str(result['ETA']))

    @staticmethod
    def updateRealTimeDispatchETA(VIN, currETA):
        print('Inside updateRealTimeDispatchETA:' + '\n')
        currETA = int(currETA, 10)
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='team12',
                                     password='pandapanda',
                                     db='team12_wego',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Read a single record for test purposes
                sql = "UPDATE `Dispatch_Records` SET `real_time_ETA`=%s WHERE `VIN`=%s AND `status`=%s"
                cursor.execute(sql, (currETA, VIN, 'IN PROGRESS'))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            with connection.cursor() as cursor:
                # Read a single record for test purposes
                sql = "SELECT `real_time_ETA` FROM `Dispatch_Records` WHERE `VIN`=%s AND `status`=%s"
                cursor.execute(sql, (VIN, 'IN PROGRESS'))
                result = cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

        print('Updated Dispatch Real Time ETA with VIN:' + str(VIN) + ', to ' + str(currETA) + ' minutes.')
        print('Result: real_time_ETA = ' + str(result['real_time_ETA']))

    @staticmethod
    def updateDispatchStatusComplete(VIN):
        print('Inside updateDispatchStatusComplete:' + '\n')
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='team12',
                                     password='pandapanda',
                                     db='team12_wego',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Read a single record for test purposes
                sql = "UPDATE `Dispatch_Records` SET `status`=%s WHERE `VIN`=%s AND `status`=%s AND `real_time_ETA`=%s"
                cursor.execute(sql, ('COMPLETE', VIN, 'IN PROGRESS', 0))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            with connection.cursor() as cursor:
                # Read a single record for test purposes
                sql = "SELECT `status` FROM `Dispatch_Records` WHERE `VIN`=%s AND `status`=%s"
                cursor.execute(sql, (VIN, 'COMPLETE'))
                result = cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

        print('Updated Dispatch status with VIN:' + str(VIN) + ', to COMPLETE')
        print('Result: Ststus = ' + str(result['status']))


    @staticmethod
    def updateDispatchStatusInProgress(VIN):
        print('Inside updateDispatchStatusInProgress:' + '\n')
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='team12',
                                     password='pandapanda',
                                     db='team12_wego',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Read a single record for test purposes
                sql = "UPDATE `Dispatch_Records` SET `status`=%s WHERE `VIN`=%s AND `status`=%s"
                cursor.execute(sql, ('IN PROGRESS', VIN, 'OPEN'))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            with connection.cursor() as cursor:
                # Read a single record for test purposes
                sql = "SELECT `status` FROM `Dispatch_Records` WHERE `VIN`=%s AND `status`=%s"
                cursor.execute(sql, (VIN, 'IN PROGRESS'))
                result = cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

        print('Updated Dispatch status with VIN:' + str(VIN) + ', to IN PROGRESS')
        print('Result: Status = ' + str(result['status']))

    @staticmethod
    def updateVehicleStatus(VIN):
        print('Inside updateVehicleStatus:' + '\n')
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='team12',
                                     password='pandapanda',
                                     db='team12_wego',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Read a single record for test purposes
                sql = "UPDATE `Vehicles` SET `status`=%s WHERE `VIN`=%s"
                cursor.execute(sql, ('AVAILABLE', VIN))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            with connection.cursor() as cursor:
                # Read a single record for test purposes
                sql = "SELECT `status` FROM `Vehicles` WHERE `VIN`=%s AND `status`=%s"
                cursor.execute(sql, (VIN, 'AVAILABLE'))
                result = cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

        print('Updated Vehicle status with VIN:' + str(VIN) + ', to AVAILABLE')
        print('Result: Status = ' + str(result['status']))

    @staticmethod
    def updateVehicleLatLong(VIN, lat, long):
        print('Inside updateVehicleLatLong:' + '\n')
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='team12',
                                     password='pandapanda',
                                     db='team12_wego',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Read a single record for test purposes
                sql = "UPDATE `Vehicles` SET `lat`=%s, `lng`=%s WHERE `VIN`=%s"
                cursor.execute(sql, (lat, long, VIN))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            with connection.cursor() as cursor:
                # Read a single record for test purposes
                sql = "SELECT `lat`,`lng` FROM `Vehicles` WHERE `VIN`=%s AND `status`=%s"
                cursor.execute(sql, (VIN, 'BUSY'))
                result = cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

        updatedLat = result['lat']
        updatedLng = result['lng']

        print('Updated Vehicle lat,lng with VIN:' + str(VIN) + ', to ' + str(lat) + ',' + str(long))
        print('Result: lat = ' + str(updatedLat) + ' lng = ' + str(updatedLng))

    @staticmethod
    def getRoute():
        print('Inside getRoute:' + '\n')
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='team12',
                                     password='pandapanda',
                                     db='team12_wego',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Read a single record for test purposes
                sql = "SELECT * FROM `Dispatch_Records` WHERE `status`=%s"
                cursor.execute(sql, ('OPEN'))
                result = cursor.fetchone()
                VIN = result['VIN']

                #Should convert the dumped JSON to an actual JSON

                route = result['route']
                route = json.loads(route)
                print(result)

        finally:
            cursor.close()
            connection.close()
        return VIN, route

    # Will handle dispatch of vehicle given delivery and payload location variables.
    @staticmethod
    def executeDispatch(orderID, ptype, dloc, ploc, username):
        print('Inside dispatch:' + '\n')
        # This data would come from the database that holds cars and their info,
        # but here are hardcoded variable for now.

        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='team12',
                                     password='pandapanda',
                                     db='team12_wego',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Find an available vehicle
                sql = "SELECT * FROM `Vehicles` WHERE `status`=%s"
                cursor.execute(sql, ('AVAILABLE'))
                result = cursor.fetchone()
                print(result)
                car_VIN = result['VIN']
                car_license = result['plateNumber']
                car_make = result['make']
                car_model = result['model']
                car_year = result['year']
                car_color = result['color']
                car_lat = result['lat']
                car_long = result['lng']
                car_status = result['status']

            with connection.cursor() as cursor:
                # Update selected vehicle to BUSY
                sql = "UPDATE `Vehicles` SET `status`=%s WHERE `vin`=%s AND `status`=%s"
                cursor.execute(sql, ('BUSY', car_VIN, 'AVAILABLE'))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()

        finally:
            cursor.close()
            connection.close()

        # Should convert the JSON route from Google to a string to be stored in database table
        origin = str(car_lat) + "," + str(car_long)
        route = methods.createRoute(origin, ploc, dloc)
        route = json.dumps(route)

        delivery_location = dloc
        payload_location = ploc

        print('Destination: ' + delivery_location + '\n'
              + 'Pickup: ' + payload_location + '\n'
              + 'Car Make: ' + car_make + '\n'
              + 'Car Model: ' + car_model + '\n'
              + 'License Plate: ' + car_license + '\n'
              + 'Car Status: ' + car_status + '\n'
              + '\n\n')

        # THIS IS WHERE DISPATCH RECORD NEEDS TO BE ADDED TO DATABASE USING dloc AND ploc
        # AND ALTERING INFORMATION FOR AVAILABLE CARS

        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='team12',
                                     password='pandapanda',
                                     db='team12_wego',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Create a new dispatch record
                sql = "INSERT INTO `Dispatch_Records` (`orderID`, `deliveryAddress`, `payloadType`, `payloadAddress`, `userID`, `VIN`, `route`, `status`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (orderID, delivery_location, ptype, payload_location, username, car_VIN, route, 'OPEN'))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
            print('Successfully updated Dispatch Record table' + '\n\n')

            with connection.cursor() as cursor:
                # Read a single record for test purposes
                sql = "SELECT * FROM `Dispatch_Records` WHERE `VIN`=%s AND `status`=%s"
                cursor.execute(sql, (car_VIN, 'OPEN'))
                result = cursor.fetchone()
                print(result)
        finally:
            cursor.close()
            connection.close()

        return 200
