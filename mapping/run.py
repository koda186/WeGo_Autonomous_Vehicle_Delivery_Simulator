import http.server
from http.server import BaseHTTPRequestHandler
import vehicle_methods
import json

PORT_NUMBER = 1201


# This class will handle any incoming request from
# a browser
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    # Any and all OPTIONS requests will reach here.
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    # Any and all POST requests will reach here.
    def do_POST(self):
        self.send_response(200)
        self.end_headers()

        # Parsing and checking POST request path.
        print(self.path)
        path = vehicle_methods.Methods.parse_post_path(self.path)

        if path == "/mapping/postTest":
            self.wfile.write(b'Path is valid. Parsing request.\n\n')
        else:
            self.send_response(400)
            self.wfile.write(b'Not a valid POST request path.\n\n')

    # Any and all GET requests will reach here.
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        # Parsing and checking GET request Path.

        print(self.path)
        path = vehicle_methods.Methods.parse_get_path(self.path)

        if path == "/mapping/requestV_Route":

            # Path is valid. Parsing request To get Vehicle Route.
            vin, route = vehicle_methods.Methods.get_v_route()
            dispatch_info = {
                'vin': vin,
                'route': route
            }
            # Fetched route and assigned vehicle VIN. Returning values now.
            dispatch_string = json.dumps(dispatch_info)
            self.wfile.write(dispatch_string.encode(encoding='utf_8'))
        elif path == "/mapping/requestSimDispatch_V":
            # This creates an open record in dispatch so we can simulate dispatching vehicle

            # create open record for vehicle simulation
            vehicle_methods.Methods.request_v_dispatch_open_record()
            # get the vin and route from open record from dispatch
            vin, route = vehicle_methods.Methods.get_v_route()
            # JSON file parsed. Simulate Dispatching Vehicle with route.
            vehicle_methods.Methods.dispatch_vehicle(vin, route)
            # Vehicle Dispatch Complete. See Database for route Info.\n\n')
            #self.wfile.write(b'Route Completed.')
        elif path == "/mapping/requestDispatch_V":
            # This takes an already created open record from dispatch and dispatches vehicle
            # get the vin and route from open record from dispatch
            vin, route = vehicle_methods.Methods.get_v_route()
            # JSON file parsed. Simulate Dispatching Vehicle with route.
            vehicle_methods.Methods.dispatch_vehicle(vin, route)
            # Vehicle Dispatch Complete. See Database for route Info.\n\n')
            #self.wfile.write(b'Route Completed.')
        else:
            self.send_response(400)
            self.wfile.write(b'Not a valid POST request path.\n\n')


httpd = http.server.HTTPServer(('', 1201), SimpleHTTPRequestHandler)
httpd.serve_forever()
