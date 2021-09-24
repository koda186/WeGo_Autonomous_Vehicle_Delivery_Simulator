import http.server
from http.server import BaseHTTPRequestHandler
import VehicleDispatch_Methods
import json

PORT_NUMBER = 1203

# This class will handle any incoming request from a browser

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # Any and all OPTIONS requests will reach here.
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    # Any and all POST requests will reach here.
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        #Parsing and checking POST request path.

        print(self.path)
        path = VehicleDispatch_Methods.methods.parsePostPath(self.path)

        if path == "/supply/requestv":

            #Path is valid. Parsing request.

            content_len = int(self.headers['content-length'])
            post_body = self.rfile.read(content_len)
            order_json = VehicleDispatch_Methods.methods.getOrderJSON(post_body)

            #JSON file parsed.

            orderID = VehicleDispatch_Methods.methods.getOrderID(order_json)
            ptype = VehicleDispatch_Methods.methods.getPayload(order_json)
            dloc = VehicleDispatch_Methods.methods.getDeliveryLocation(order_json)
            ploc = VehicleDispatch_Methods.methods.getPayloadLocation(order_json)
            username = VehicleDispatch_Methods.methods.getUsername(order_json)

            #Delivery Location and Payload Location obtained. Sending info to dispatch method.

            dispatch_made = VehicleDispatch_Methods.methods.executeDispatch(orderID, ptype, dloc, ploc, username)

            if dispatch_made == 200:
                self.wfile.write(b'Dispatch complete. Dispatch Record table updated in database.')
            # self.wfile.write(orderID.encode(encoding='utf_8'))

            else:
                self.wfile.write(b'Dispatch execution failed.\n\n')

        elif path == "/supply/testRoute":
            #Path is valid. Parsing request for route from Google.

            content_len = int(self.headers['content-length'])
            post_body = self.rfile.read(content_len)
            map_json = VehicleDispatch_Methods.methods.getMapJSON(post_body)

            #JSON file parsed. Creating route from given information.

            origin = VehicleDispatch_Methods.methods.getOrigin(map_json)
            dloc = VehicleDispatch_Methods.methods.getDeliveryLocation(map_json)
            ploc = VehicleDispatch_Methods.methods.getPayloadLocation(map_json)
            route = VehicleDispatch_Methods.methods.createRoute(origin, ploc, dloc)

            # Route created. Returning result now.
            route_string = json.dumps(route)
            self.wfile.write(route_string.encode(encoding='utf_8'))

        elif path == "/supply/updateV_Complete_Route_Distance":
            content_len = int(self.headers['content-length'])
            post_body = self.rfile.read(content_len)
            distance_json = VehicleDispatch_Methods.methods.getDistanceJSON(post_body)
            distance = VehicleDispatch_Methods.methods.getDistance(distance_json)
            self.wfile.write(b'Data received and processed.')

        elif path == "/supply/updateV_Location":
            content_len = int(self.headers['content-length'])
            post_body = self.rfile.read(content_len)
            location_json = VehicleDispatch_Methods.methods.getLocationJSON(post_body)
            VIN = VehicleDispatch_Methods.methods.getVIN(location_json)
            lat = VehicleDispatch_Methods.methods.getVLat(location_json)
            long = VehicleDispatch_Methods.methods.getVLong(location_json)
            VehicleDispatch_Methods.methods.updateVehicleLatLong(VIN, lat, long)
            self.wfile.write(b'Data received and processed.')

        elif path == "/supply/updateV_Complete_Route_ETA":
            content_len = int(self.headers['content-length'])
            post_body = self.rfile.read(content_len)
            compETA_json = VehicleDispatch_Methods.methods.getCompETAJSON(post_body)
            VIN = VehicleDispatch_Methods.methods.getVIN(compETA_json)
            compETA = VehicleDispatch_Methods.methods.getCompETA(compETA_json)
            VehicleDispatch_Methods.methods.updateDispatchStatusInProgress(VIN)
            VehicleDispatch_Methods.methods.updateDispatchETA(VIN, compETA)
            self.wfile.write(b'Data received and processed.')

        elif path == "/supply/updateV_Real_Time_ETA":
            content_len = int(self.headers['content-length'])
            post_body = self.rfile.read(content_len)
            currETA_json = VehicleDispatch_Methods.methods.getCurrETAJSON(post_body)
            VIN = VehicleDispatch_Methods.methods.getVIN(currETA_json)
            currETA = VehicleDispatch_Methods.methods.getCurrETA(currETA_json)
            VehicleDispatch_Methods.methods.updateRealTimeDispatchETA(VIN, currETA)
            self.wfile.write(b'Data received and processed.')

        elif path == "/supply/updateV_Is_Route_Complete":
            content_len = int(self.headers['content-length'])
            post_body = self.rfile.read(content_len)
            routeBool_json = VehicleDispatch_Methods.methods.getRouteBoolJSON(post_body)
            VIN = VehicleDispatch_Methods.methods.getVIN(routeBool_json)
            routeBool = VehicleDispatch_Methods.methods.getRouteBool(routeBool_json)
            if routeBool == "True":
                VehicleDispatch_Methods.methods.updateDispatchStatusComplete(VIN)
                VehicleDispatch_Methods.methods.updateVehicleStatus(VIN)
            self.wfile.write(b'Data received and processed.')

        else:
            self.send_response(400)
            self.wfile.write(b'Not a valid POST request path.\n\n')

    # Any and all GET requests will reach here.
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        #Parsing and checking GET request Path.

        print(self.path)
        path = VehicleDispatch_Methods.methods.parseGetPath(self.path)

        if path == "/supply/testDispatch":

            #Path is valid. Fetching an open route from database.

            VIN, route = VehicleDispatch_Methods.methods.getRoute()
            dispatch_info = {
                'vin':VIN,
                'route':route
            }
            #Fetched route and assigned vehicle VIN. Returning values now.
            dispatch_string = json.dumps(dispatch_info)

            self.wfile.write(dispatch_string.encode(encoding='utf_8'))

        elif path == "/supply/getRealTimeETA":

            #Path is valid. Fetching ETA.
            content_len = int(self.headers['content-length'])
            post_body = self.rfile.read(content_len)
            orderIDJSON = VehicleDispatch_Methods.methods.getOrderIDJSON(post_body)
            orderID = VehicleDispatch_Methods.methods.getOrderID(orderIDJSON)
            realTimeETA = VehicleDispatch_Methods.methods.getRealTimeETA(orderID)

            self.wfile.write(str(realTimeETA).encode(encoding='utf_8'))



        else:
            self.send_response(400)
            self.wfile.write(b'Not a valid GET request path.\n\n')


httpd = http.server.HTTPServer(('', 1203), SimpleHTTPRequestHandler)
httpd.serve_forever()
