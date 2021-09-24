from urllib import parse
import json
import requests
import simulatorTester
import random


class Methods:

    # parse the post request
    @staticmethod
    def parse_post_path(path):
        print('Inside parsePostPath:' + '\n')

        path_parse = parse.urlparse(path)
        i = 0
        while path_parse[i]:
            print('Result of path parse at i: ' + path_parse[i] + ' ' + i.__str__() + '\n')
            i += 1
        path = path_parse[2]
        print('Path of url: ' + path + '\n\n')
        if path != "/mapping/postTest":
            raise Exception("Not a valid request path.")
        return path
    
    # parse the get request
    @staticmethod
    def parse_get_path(path):
        print('Inside parseGetPath:' + '\n')

        path_parse = parse.urlparse(path)
        i = 0
        while path_parse[i]:
            print('Result of path parse at i: ' + path_parse[i] + ' ' + i.__str__() + '\n')
            i += 1
        path = path_parse[2]
        print('Path of url: ' + path + '\n\n')
        if path != "/mapping/requestV_Route" and path != "/mapping/requestSimDispatch_V" and path != "/mapping/requestDispatch_V":
            raise Exception("Not a valid request path.")
        return path

    # returns dispatch route open record
    # testDispatch, does not require any input, looks for open dispatch record,
    # returns the vin of vehicle in record as well as the record route
    @staticmethod
    def get_route_and_vin():
        http = "https://team12.supply.softwareengineeringii.com/supply/testDispatch"
        r = requests.get(url=http)
        binary = r.content
        dispatch_info = json.loads(binary)
        VIN = dispatch_info.get('vin')
        route = dispatch_info.get('route')
        return VIN, route

    # create open record in dispatch to test dispatch vehicle simulating with vin and route record given.
    @staticmethod
    def request_v_dispatch_open_record():
        # randrange only output integers
        order_id = random.randrange(100, 1001)
        dloc = "2706 east 22nd st, Austin,TX 78722"

        open_record = {
            'orderID': order_id,
            'ptype': 'clothes',
            'dloc': dloc,
            'ploc': '9500 S IH 35 Frontage Rd Ste H, Austin',
            'username': 'VehicleRestApi'
        }

        url = "https://team12.supply.softwareengineeringii.com/supply/requestv"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(open_record), headers=headers)
        # print(r.status_code)

    # get the vin and route from dispatch request
    @staticmethod
    def get_v_route():
        vin, route = Methods.get_route_and_vin()
        return vin, route

    # dispatch vehicle simulator
    @staticmethod
    def dispatch_vehicle(vin, route):
        print("Vehicle assigned route, Dispatching Vehicle")
        car = simulatorTester.Vehicle(vin, route)
        car.get_dispatched_vehicle_route_steps()

