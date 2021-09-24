# simulator python terminal design:
import requests
# http requests library, e.g. requests.get(API_Call).json()
import time
import json
import random


class Vehicle:

    # init method or constructor
    def __init__(self, vin, route):
        leg_counter = 0
        leg_route_eta = 0
        leg_route_distance = 0
        complete_route_distance = 0
        complete_route_eta = 0
        step_eta_total = 0
        calculated_eta_to_destination = 0
        route_step_eta = " "
        eta_duration = " "
        veh_lat = " "
        veh_lng = " "
        veh_loc = " "
        dloc = "905 E 41st St Austin TX"
        origin = "30.2330728,-97.7580753"
        #simulator route vars
        self.vin = vin
        self.origin = origin
        self.dloc = dloc
        self.json_route = route
        #calculated vars
        self.eta_duration = eta_duration
        self.calculated_eta_to_destination = calculated_eta_to_destination
        self.step_eta_total = step_eta_total
        self.route_complete = False
        #complete route vars
        self.complete_route_eta = complete_route_eta
        self.complete_route_distance = complete_route_distance
        #leg vars
        self.leg_counter = leg_counter
        self.leg_route_eta = leg_route_eta
        self.leg_route_distance = leg_route_distance
        #step vars
        self.route_step_eta = route_step_eta
        #veh location vars
        self.veh_lat = veh_lat
        self.veh_lng = veh_lng
        self.vehicle_location = veh_loc

# -----------------------------------------Vehicle functions----------------------------------------------
    # get total distance from origin to destination
    def get_V_Complete_Route_Distance(self):
        json_route = self.json_route
        if json_route['status'] == 'NOT_FOUND':
            print("Please enter a valid delivery address!\n")
        else:
            # JSON_response comes from the database dispatch api request
            for route in json_route['routes']:
                for leg in route['legs']:
                    route_distance = (leg['distance']['text'])
                    route_distance = route_distance.replace(',', '')  # remove comma separation
                    distance = float(route_distance.split()[0])
                    self.complete_route_distance += distance
                    self.complete_route_distance = float(format(self.complete_route_distance, '.2f'))
            if self.complete_route_distance is 0:
                raise Exception('Error: Vehicle has not received route!')
            return self.complete_route_distance

    # Calculate the real time eta for vehicle based on location(step) in route
    def get_V_real_time_eta(self):
        step_eta = int(self.eta_duration.split()[0])
        self.step_eta_total += step_eta
        vehicle_step_eta_total = self.step_eta_total
        self.calculated_eta_to_destination = self.complete_route_eta - vehicle_step_eta_total
        return self.calculated_eta_to_destination

    #get total eta from origin to destination
    def get_V_total_Route_ETA(self):
        json_response = self.json_route
        if json_response['status'] == 'NOT_FOUND':
            print("Please enter a valid delivery address!\n")
        else:
            # JSON_response comes from the database dispatch api request
            for route in json_response['routes']:
                for leg in route['legs']:
                    for step in leg['steps']:
                        self.route_step_eta = (step['duration']['text'])
                        route_step_eta = self.route_step_eta
                        step_eta = int(route_step_eta.split()[0])
                        self.complete_route_eta += step_eta
                        self.complete_route_eta = int(format(self.complete_route_eta))
            if self.complete_route_eta is 0:
                raise Exception('Error: Vehicle has not received route!')
            return self.complete_route_eta

    #checks is Vehicle route complete;true or false
    def is_V_route_complete(self):
        route_completed = self.route_complete
        real_time_eta = self.calculated_eta_to_destination
        if real_time_eta == 0:
            route_completed = True
        return route_completed

    # get route from the dispatch API response for vehicle simulation
    def get_dispatched_vehicle_route_steps(self):
        #Count legs to get item pickup location
        leg_counter = self.leg_counter
        json_response = self.json_route

        # JSON_response comes from the database dispatch api request
        for route in json_response['routes']:
            # ---------------Print Vehicle simulator route updates------------------------
            Vehicle.print_simulator_updates(self)
            # Vehicle sends route total distance and total eta to Dispatch if vehicle assigned to route
            if self.vin != "NO VEHICLE ASSIGNED":
                Vehicle.update_dispatch_total_eta_distance(self)

            for leg in route['legs']:
                leg_counter += 1
                self.leg_route_eta = (leg['duration']['text'])
                self.leg_route_distance = (leg['distance']['text'])
                if leg_counter == 1:
                    print('First Leg of trip (Origin to Warehouse(Payload Pickup)) ETA: ' + str(Vehicle.send_leg_eta(self))
                          + ' and Distance: ' + Vehicle.send_leg_distance(self) + '\n'
                            + 'Vehicle: ' + self.vin + ' En Route' + '\n\n')
                else:
                    print('Vehicle Receiving Payload -- Vehicle Enroute: Second leg of trip (Warehouse to Destination(Delivery Address)) ETA: '
                            + str(Vehicle.send_leg_eta(self))
                            + ' and Distance: ' + str(Vehicle.send_leg_distance(self)))
                    # simulate vehicle stopped for item pickup from warehouse
                    time.sleep(5)
                    print('Vehicle: ' + self.vin + ' En Route' + '\n\n')
                for step in leg['steps']:
                    self.eta_duration = str(step['duration']['text'])
                    self.dloc = (step['end_location'])
                    self.origin = (step['start_location'])
                    # update vehicle location
                    self.veh_lat = str(step['end_location']['lat'])
                    self.veh_lng = str(step['end_location']['lng'])
                    time.sleep(7)

                    # Print route to console to simulate vehicle traversing route
                    Vehicle.print_dispatched_vehicle_route(self)
                    # send real time updates and confirmation route ended  to dispatch if vehicle assigned to route:
                    if self.vin != "NO VEHICLE ASSIGNED":
                        Vehicle.update_dispatch(self)

    # Vehicle sends route total distance and total eta to Dispatch
    def update_dispatch_total_eta_distance(self):
        # ---------------Vehicle sends route total distance to Dispatch---------------
        Vehicle.send_V_Complete_Route_Distance(self)
        # --------------Vehicle sends total route eta to Dispatch -------------------
        Vehicle.send_V_Complete_Route_ETA(self)


    # send real time updates and confirmation route ended  to dispatch
    def update_dispatch(self):
        # --------------Vehicle sends location update to Dispatch---------------
        Vehicle.send_V_location_update(self)
        #--------------Vehicle sends real time eta update to Dispatch---------------
        Vehicle.send_real_time_eta(self)
        #--------------Vehicle sends "is route complete" comfirmation to Dispatch---------------
        Vehicle.send_dispatch_route_ended(self)

    # get each leg of route eta
    #legs for "RENT'D AND Farm to Home" are "Origin to Payload pickup" and "Payload pickup to destination"
    def send_leg_eta(self):
        leg_route_eta = self.leg_route_eta
        leg_route_eta = json.dumps(leg_route_eta)
        return leg_route_eta

    # get each leg of route distance
    # legs for "RENT'D AND Farm to Home" are "Origin to Payload pickup" and "Payload pickup to destination"
    def send_leg_distance(self):
        leg_route_distance = self.leg_route_distance
        leg_route_distance = json.dumps(leg_route_distance)
        return leg_route_distance

    #get address from route that google maps api auto-corrected from user input
    def reverse_geocode(self):
        #Count legs to get item pickup location
        leg_counter = 0
        json_response = self.json_route
        # test to see if the request was valid
        if json_response['status'] == 'NOT_FOUND':
            print("Please enter a valid delivery address!\n")
        else:
            for route in json_response['routes']:
                for leg in route['legs']:
                    leg_counter += 1
                    end_address = (leg['end_address'])
                    if leg_counter == 2:
                        return str(end_address)

    # get vehicle location during route simulation for dispatch
    def get_V_location(self):
        veh_lat = self.veh_lat
        veh_lng = self.veh_lng
        veh_vin = self.vin

        veh_location = {
            'vin': veh_vin,
            'lat': veh_lat,
            'long': veh_lng
        }

        return veh_location

# --------------------------Vehicle - Pycharm Console updates:-----------------------------------------------
    # Printing for Simulator Tester via pycharm console
    def print_simulator_updates(self):
        veh_vin = self.vin
        print('\n\n' + 'You chose Destination Address: ' + str(Vehicle.reverse_geocode(self)))
        print('Vehicle Dispatched: VIN of Vehicle IN SERVICE: ' + veh_vin)
        print('Route Calculated: Distance of Trip: ' + str(Vehicle.get_V_Complete_Route_Distance(self)) + ' miles')
        print('ETA to destination: ' + str(Vehicle.get_V_total_Route_ETA(self)) + ' minutes')

    # Printing for Simulator Tester via pycharm console
    # Simulated vehicle taking route steps: origin, ploc=Payload pickup location, dloc=destination
    def print_dispatched_vehicle_route(self):
        origin = self.origin
        dloc = self.dloc
        veh_vin = self.vin
        # print route steps
        print('Inside Dispatch -- VEHICLE DISPATCH REPORT FOLLOWS: ' + '\n'
              + 'CURRENT vehicle VIN: ' + veh_vin + '\n' + 'Vehicle origin: ' + str(origin)
              + ' TRAVELLING to next step of Vehicle destination: ' + str(dloc)
              + '\n' + 'Updated Vehicle location in Dispatch: ' + str(Vehicle.get_V_location(self))
              + '\n' + 'Vehicle Real Time ETA to destination: ' + str(Vehicle.get_V_real_time_eta(self)) + ' minutes away'
              + '\n' + 'Vehicle Reports Route Complete: ' + str(Vehicle.is_V_route_complete(self))
              + '\n\n')
        if Vehicle.is_V_route_complete(self):
            print('Vehicle Arrived at Destination: Dispatch confirmation sent')
        else:
            print('Vehicle: ' + veh_vin + ' En Route')

# ----------------------------Vehicle - Send Vehicle Updates:----------------------------------------
    # send complete route distance for dispatch
    def send_V_Complete_Route_Distance(self):
        complete_route_distance = self.complete_route_distance

        total_distance = {
            'distance': str(complete_route_distance)
        }

        url = "https://team12.supply.softwareengineeringii.com/supply/updateV_Complete_Route_Distance"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(total_distance), headers=headers)

    # send Vin of Vehicle with location updates during route simulation for dispatch
    def send_V_location_update(self):
        vehicle_location = Vehicle.get_V_location(self)
        url = "https://team12.supply.softwareengineeringii.com/supply/updateV_Location"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(vehicle_location), headers=headers)

    # send (total) complete route eta for dispatch
    def send_V_Complete_Route_ETA(self):
        complete_route_eta = self.complete_route_eta
        veh_vin = self.vin

        total_eta = {
            'vin': veh_vin,
            'compETA': str(complete_route_eta)
        }

        url = "https://team12.supply.softwareengineeringii.com/supply/updateV_Complete_Route_ETA"
        #complete_route_eta = self.complete_route_eta
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(total_eta), headers=headers)

    # send dispatch real time eta updates from vehicle as it routes to destination
    def send_real_time_eta(self):
        vehicle_real_time_eta = self.calculated_eta_to_destination
        vin = self.vin

        current_ETA = {
            'vin': vin,
            'currETA': str(vehicle_real_time_eta)
        }
        url = "https://team12.supply.softwareengineeringii.com/supply/updateV_Real_Time_ETA"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(current_ETA), headers=headers)

    # send dispatch update on whether "is route complete"
    def send_dispatch_route_ended(self):
        vin = self.vin
        dispatch_conf = {
            'vin': vin,
            'routeBool': str(Vehicle.is_V_route_complete(self))
        }
        url = "https://team12.supply.softwareengineeringii.com/supply/updateV_Is_Route_Complete"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(dispatch_conf), headers=headers)


    # So I can send vehicle route from dispatch to front end
    # returns dispatch route open record
    # testDispatch, does not require any input, looks for open dispatch record, returns the vin of vehicle in record as well as the record route
    @staticmethod
    def get_vin_and_route():
        http = "https://team12.supply.softwareengineeringii.com/supply/testDispatch"
        r = requests.get(url=http)
        binary = r.content
        dispatch_Info = json.loads(binary)
        VIN = dispatch_Info.get('vin')
        route = dispatch_Info.get('route')
        return VIN, route


# ---------------------------------Main() - Simulator Tester:------------------------------------------------

# Initialize variables, console loop
def main():

    # Console loop
    print('\nWelcome to the Vehicle Web Services API Simulator\n')
    print('\nPlease enter your choice below:\n')
    # input('Please press ENTER to continue!\n')

    test_cases = {1: 'To test the ROUTE of a vehicle simulator to Destination Address of: 3001 Congress St, Austin TX 78704',
                  2: 'To test the ROUTE of a vehicle simulator to destination of your choice. Please use following format: 3001 Congress St, Austin TX 78704',
                  3: 'To test the ROUTE of a vehicle simulator to Destination Address of Invalid Input: dddd yyry',
                  4: 'To SIMULATE VEHICLE DRIVING to following Destination Address while also updating Dispatch: 905 E 41st St Austin TX 78751',
                  5: 'To SIMULATE VEHICLE DRIVING to Destination Address of your choice while also updating Dispatch. Please enter address with following format: 3001 Congress St, Austin TX 78704',
                  6: 'To SIMULATE VEHICLE DRIVING to Destination Address of Invalid Input: 223 Djak Sdsf',
                  7: 'Simulate Dispatch connection: Show Vin and Route of open record',
                  8: 'Future',
                  9: 'Future',
                  10: 'Exit this menu'}

    # Map user console input to a test case
    # userChoices is a dictionary, key points to test case
    # Includes user input exception handling
    # Loop until user input is '10'
    def user_input(user_choices):
        while True:
            print(' your choices'.upper(), '\t\t\tTest Case\n'.upper(), '-' * 55)

            for key, value in user_choices.items():
                print('\t', key, ' \t\t\t\t', value)
            try:
                choice = int(input("\nPlease enter the numeric choice for a Test Case \n\t --> ".upper()))
            except:
                print("\nSomething went wrong, please enter a numeric value!!!\n")
                continue

            if choice == 10:
                break

            menu_except(choice)

    # "Please enter the numeric choice for a Test Case"
    # Map user menu selection (parameter) to module (function call)
    def menu_except(choice):
        # testCases
        test_route_only_empty_veh_vin = "NO VEHICLE ASSIGNED"
        test_route_dloc = "3001 Congress St, Austin TX 78704"
        test_route_invalid_addr = "dddd yyry"
        test_V_dloc = "905 E 41st St Austin TX"
        test_V_invalid_addr = "223 Djak Sdsf"

        if choice == 1:
            # print('You chose: ' + str(test_route_dloc))
            response = dispatch_vehicle(test_route_dloc)
            # give vehicle route and empty vin
            car = Vehicle(test_route_only_empty_veh_vin, response)
            car.get_dispatched_vehicle_route_steps()
        elif choice == 2:
            test_route_dloc_input = input('\tPlease enter a Delivery Address --> ')
            print('You chose: ' + str(test_route_dloc_input))
            response = dispatch_vehicle(test_route_dloc_input)
            # give vehicle route and empty vin
            car = Vehicle(test_route_only_empty_veh_vin, response)
            car.get_dispatched_vehicle_route_steps()
        elif choice == 3:
            print('You chose: ' + str(test_route_invalid_addr))
            response = dispatch_vehicle(test_route_invalid_addr)
            # give vehicle route and empty vin
            car = Vehicle(test_route_only_empty_veh_vin, response)
            car.get_dispatched_vehicle_route_steps()
        elif choice == 4:
            print('You chose: ' + str(test_V_dloc))
            response = dispatch_vehicle(test_V_dloc)
            if response['status'] != 'NOT_FOUND':
                # request open dispatch record order
                request_V_dispatch_open_record(test_V_dloc)
                vin = get_vin()
                # assign vehicle route
                car = Vehicle(vin, response)
                car.get_dispatched_vehicle_route_steps()
        elif choice == 5:
            test_V_dloc_input = input('\tPlease enter a Delivery Address --> ')
            print('You chose: ' + str(test_V_dloc_input))
            response = dispatch_vehicle(test_V_dloc_input)
            # request open dispatch record order
            if response['status'] != 'NOT_FOUND':
                request_V_dispatch_open_record(test_V_dloc_input)
                vin = get_vin()
                # assign vehicle route
                car = Vehicle(vin, response)
                car.get_dispatched_vehicle_route_steps()
        elif choice == 6:
            print('You chose: ' + str(test_V_invalid_addr))
            response = dispatch_vehicle(test_V_invalid_addr)
            # request open dispatch record order
            if response['status'] != 'NOT_FOUND':
                request_V_dispatch_open_record(test_V_invalid_addr)
                vin = get_vin()
                # assign vehicle route
                car = Vehicle(vin, response)
                car.get_dispatched_vehicle_route_steps()
        elif choice == 7:
            print('Retrieving Dispatch open record: Vehicle vin and route follows:')
            vin, response = get_route_and_vin()
            car = Vehicle(vin, response)
            car.get_dispatched_vehicle_route_steps()
        elif choice == 8:
            print('You are testing the a Rest Api for the vehicle')
            test_vehicle_api()
            # print('test case construction underway, come back soon!')
        elif choice == 9:
            print('test case construction underway, come back soon!')
        else:
            print('Whatchu talking about Willis? Please try a valid choice!')

        input('*************** Press Enter to continue ******************\n\n'.upper())

#------------------------------------------Main() - get Dispatch Info for Vehicle:-----------------------------------------
    # for simulation purposes, dispatch needs route so vehicle can be dispatched
    # origin = vehicle location
    # ploc = payload pickup location
    # dloc = destination delivery address
    def send_dispatch_route(dloc):
        # a Python object (dict):
        dispatch_info = {
            'origin': '30.23001039999999, -97.75471589999999',
            'ploc': '314 West 11th St Austin TX 78701',
            'dloc': dloc
        }
        return dispatch_info

    # testRoute is sending the dispach api 3 paramaters and vehicle receives 'step by step' route so we can run testcases,
    # returns valid route to be tested
    # build the dispatch API Request
    def dispatch_vehicle(dloc):

        url = "https://team12.supply.softwareengineeringii.com/supply/testRoute"
        dispatch_info = send_dispatch_route(dloc)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(dispatch_info), headers=headers)

        #print(r.status_code)
        output = r.json()
        if r.status_code == 200:
            output = r.json()
        else:
            print('Not a valid request path.\n')

        #if r.status_code == 200:
            #output = r.json()
            ## return output
       # else:
            #print('Not a valid request path.\n')
            #user_input(test_cases)

        # test to see if the request was valid
        if output['status'] == 'NOT_FOUND':
            print("Invalid delivery address input: " + dloc + "\n" + "Please try again! \n")
            user_input(test_cases)
        else:
            return output

    #create open record in dispatch to test vehicle simulating route given
    def request_V_dispatch_open_record(dloc):
        # randrange only output integers
        order_id = random.randrange(100, 1001)

        open_record = {
            'orderID': order_id,
            'ptype': 'clothes',
            'dloc': dloc,
            'ploc': '9500 S IH 35 Frontage Rd Ste H, Austin',
            'username': 'simulatorTester'
        }

        url = "https://team12.supply.softwareengineeringii.com/supply/requestv"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(open_record), headers=headers)
        print(r.status_code)


    # returns vin of vehicle
    # testDispatch, does not require any input, looks for open dispatch record,
    # returns the vin of vehicle in record as well as the record route
    def get_vin():
        http = "https://team12.supply.softwareengineeringii.com/supply/testDispatch"
        r = requests.get(url=http)
        binary = r.content
        dispatch_Info = json.loads(binary)
        VIN = dispatch_Info.get('vin')
        return VIN

    # returns dispatch route open record
    # testDispatch, does not require any input, looks for open dispatch record,
    # returns the vin of vehicle in record as well as the record route
    def get_route_and_vin():
        http = "https://team12.supply.softwareengineeringii.com/supply/testDispatch"
        r = requests.get(url=http)
        binary = r.content
        dispatch_Info = json.loads(binary)
        VIN = dispatch_Info.get('vin')
        route = dispatch_Info.get('route')
        return VIN, route

    # test Vehicle api
    def test_vehicle_api():
        http = "https://team12.supply.softwareengineeringii.com/mapping/requestDispatch_V"
        r = requests.get(url=http)
        print(r.status_code)

    user_input(test_cases)
    input('\n\nSay Bye-bye'.upper())


main()

