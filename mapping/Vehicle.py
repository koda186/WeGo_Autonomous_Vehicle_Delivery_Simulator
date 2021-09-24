# requests, JSON library, and pretty print library
# Below I extracted step by step driving directions.
from urllib import parse
import json
import requests
import pprint
import time

# Notes:
# Simulator tester- run test cases on simulator
# tester looking at display with pycharm terminal. If i type '1', then it cause test case 1 to run in the simulator
# simulator does not pull a route through map services, vehicle simulator does not get route from mapping service.

class Vehicle(object):

    # init method or constructor
    def __init__(self, vin, origin, ploc, dloc):
        leg_counter = 0
        route_eta = 0
        step_distance = 0
        vehicle_status_available = True
        route_distance = 0
        self.leg_counter = leg_counter
        self.vin = vin
        self.origin = origin
        self.ploc = ploc
        self.dloc = dloc
        self.route_eta = route_eta
        self.step_distance = step_distance
        self.route_distance = route_distance
        self.vehicle_status_available = vehicle_status_available

        # Autonomous vehicle needs route info, this is accomplish with google maps api request
        # returns json
        http = 'https://maps.googleapis.com/maps/api/directions/json?'

        params = dict(
            origin=self.origin,
            destination=self.dloc,
            waypoints=self.ploc,
            key='?'
        )

        data = requests.get(url=http, params=params)

        if data.status_code == 200:
            binary = data.content
            output = json.loads(binary)
            self.output = output
            print(output)
        else:
            print('Not a valid request path.\n')

        # test to see if the request was valid
        print('Valid Request: ' + output['status'] + '\n')

    # parse request path
    @staticmethod
    def parsePath(path):
        print('Inside parsePath:' + '\n')

        path_parse = parse.urlparse(path)
        i = 0
        while path_parse[i]:
            print('Result of path parse at i: ' + path_parse[i] + ' ' + i.__str__() + '\n')
            i += 1
            path = path_parse[2]

        print('Path of url: ' + path + '\n\n')
        if path != "/supply/requestv" and path != "/supply/dispatchv":
            raise Exception("Not a valid request path.")
        return path

    # get the Json from request
    @staticmethod
    def getJSON(post_body):

        post_dict = json.loads(post_body)
        order_id = post_dict.get("orderID")
        ptype = post_dict.get("ptype")
        dloc = post_dict.get("dloc")
        ploc = post_dict.get("ploc")
        username = post_dict.get("username")
        #print(order_id)
        #print(ptype)
        #print(dloc)
        #print(ploc)
        #print(username)

        return post_dict

    # Returns Delivery Location stored in JSON dict
    @staticmethod
    def getOrderID(json):
        print('Inside getOrderID:' + '\n')
        orderID = json.get("orderID")
        print('Order ID: ' + orderID + '\n\n')
        return orderID

    # TODO
    # This will be sent to dispatch record
    def send_route(self):
        return self.origin, self.ploc, self.dloc

    # TODO
    # This will be sent to dispatch record
    def send_status(self):
        if self.vehicle_status_available:
            return 'AVAILABLE'
        else:
            return 'IN SERVICE'

    # TODO
    # This will be sent to dispatch record
    # for now vehicle location is the final destination of its last route
    # This needs some modifying
    def send_vehicle_location(self):
        return str(self.dloc)

    # TODO
    # This will be sent to dispatch record
    # This needs some modifying
    def send_eta(self):
        if self.route_eta == 0:
            return 'Unavailable'
        else:
            return str(self.route_eta)

    # TODO
    # This will be sent to dispatch record
    # This needs some modifying
    def send_distance(self):
        return str(self.route_distance)

    # TODO
    # This will be sent to dispatch record
    # This needs some modifying
    def send_vin(self):
        return str(self.vin)

    # step-by-step directions from start to end location.
    # This will be sent to dispatch record
    def send_dispatched_vehicle_route_steps(self):
        # write to dispatch report
        f = open("dispatchReport.txt", "w")
        for route in self.output['routes']:
            for leg in route['legs']:
                self.leg_counter += 1
                self.route_eta = (leg['duration']['text'])
                self.route_distance = (leg['distance']['text'])
                if self.leg_counter == 1:
                    f.write('First Leg of trip (Origin to Waypoint) ETA: ' + Vehicle.send_eta(self)
                            + ' and Distance:' + Vehicle.send_distance(self) + '\n\n')
                else:
                    f.write('Vehicle Recieved Payload -- Second leg of trip (Waypoint to Destination) ETA: '
                            + Vehicle.send_eta(self)
                            + ' and Distance:' + Vehicle.send_distance(self) + '\n\n')
                Vehicle.get_vehicle_simulator_eta_distance(self)
                for step in leg['steps']:
                    self.vehicle_status_available = False
                    self.dloc = (step['end_location'])
                    self.origin = (step['start_location'])
                    self.step_distance = (step['distance']['text'])
                    time.sleep(0)
                    f.write('Vehicle VIN: ' + Vehicle.send_vin(self) + '\n'
                            + 'Vehicle Status: ' + Vehicle.send_status(self) + '\n' + 'CURRENT vehicle origin: '
                            + str(self.origin)
                            + ' TRAVELLING to Vehicle destination: ' + str(self.dloc) + '\n'
                            + 'Distance between this leg: ' + str(self.step_distance)
                            + '\n\n')
                    # self.vehicle_status_available = True
                    Vehicle.get_simulator_vehicle_enroute(self)
        # set vehicle status to available once it is at end of route
        self.vehicle_status_available = True
        f.write('Vehicle VIN: ' + Vehicle.send_vin(self) + '\n'
                + 'Vehicle Status: ' + Vehicle.send_status(self) + '\n'
                + 'Vehicle Current Location: ' + Vehicle.send_vehicle_location(self)
                + '\n\n')
        # closing file object
        f.close()

    # function call only for printing dispatch of vehicle to console for testing!!
    # will be converted to txt file for dispatch record
    @staticmethod
    def get_simulator_vehicle_enroute(self):
        vehicle_enroute_origin = self.origin
        vehicle_enroute_destination = self.dloc
        distance = self.step_distance
        vehicle_vin = self.vin

        # printing dispatch record for testing purposes only!
        print('Inside dispatch -- VEHICLE DISPATCH REPORT FOLLOWS: ')

        print('Vehicle VIN: ' + str(vehicle_vin) + '\n'
              + 'Vehicle Status: ' + str(Vehicle.send_status(self)))

        print('Inside Dispatch -- VEHICLE DISPATCH REPORT FOLLOWS: ' + '\n'
              + 'CURRENT vehicle origin: ' + str(vehicle_enroute_origin)
              + ' TRAVELLING to Vehicle destination: ' + str(vehicle_enroute_destination) + '\n'
              + 'Distance between this leg: ' + str(distance)
              + '\n\n')

    # function call only for printing vehicle route eta and distance to console for testing!!
    # will be converted to txt file for dispatch record
    @staticmethod
    def get_vehicle_simulator_eta_distance(self):
        trip_eta = self.route_eta
        trip_distance = self.route_distance

        # printing dispatch for testing purposes only!
        if self.leg_counter == 1:
            print('First Leg of trip (Origin to Waypoint) ETA: ' + trip_eta
                  + ' Distance:' + trip_distance + '\n')
        else:
            print('Vehicle Recieved Payload -- Second leg of trip (Waypoint to Destination) ETA: ' + trip_eta
                  + ' Distance:' + trip_distance + '\n')


# execute route below (temporary function calls now, will be called from Vehicle Dispatch API)
# origin, ploc, dloc,and vin will come from dispatch api (need to be requested? run.py??)
# vin is for setting the status of vehicle from 'in service' to 'available only'
#-----------------------------------------------------------------
# origin = '905 E 41st St, Austin, TX 78751'
# dloc = '300 S Congress Ave, Austin, TX 78704'
# ploc = '2610 Manor Rd, Austin, TX 78722'
# vin = '15AX493HHJ238DA21'

# Vehicle
# car = Vehicle(vin, origin, ploc, dloc)
# print(car.send_eta())
# print('Get Vehicle Current Location: ' + car.send_vehicle_location() + '\n')
# print('Show vehicle status:' + car.send_status())
# print('Vehicle Received Route: ' + str(car.send_route()) + '\n')
# car.send_dispatched_vehicle_route_steps()
# print('Show vehicle status:' + car.send_status() + '\n')
# print('Get Vehicle Current Location: ' + car.send_vehicle_location() + '\n')

# SIMULATOR IS SIMULATING A CANNED ROUTE, LOAD TEST CASES TO STOP THE VEHICLE DURING ROUTE. ETC...
