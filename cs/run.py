import vehicleAPI
import http.server
import json
import fmLoginMethods

from http.server import BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print(self.path)
        
        if self.path == "/cs/registerVehicle":
            length = int(self.headers['content-length'])
            body = self.rfile.read(length)
            
            # BONUS: How to convert the body from a JSON string representation of a map to a python dictionary
            dictionary = json.loads(body)
            
            vin = dictionary.get("vin")
            license_plate = dictionary.get("license_plate")
            model = dictionary.get("model")
            make = dictionary.get("make")
            year = dictionary.get("year")
            color = dictionary.get("color")
            lat = dictionary.get("lat")
            lng = dictionary.get("long")
            status = dictionary.get("status")
            
            databaseresult = vehicleAPI.registerVehicle(vin, license_plate, model, make, year, color, lat, lng, status)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            s = databaseresult
            
            # Finally, the body! The body receives bytes, so if you have a string, this is how to convert it to a bytes!
            # s = 'Success!!!!!'
            bytes = s.encode('utf-8')
            self.wfile.write(bytes)

        if self.path == "/cs/tableview":
            length = int(self.headers['content-length'])
            
            body = self.rfile.read(length)
                # print('Body:', body)
                
                # BONUS: How to convert the body from a JSON string representation of a map to a python dictionary
                
                
            databaseresult = vehicleAPI.getAll()
            
            
            vehicle_string = json.dumps(databaseresult)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(vehicle_string.encode(encoding='utf_8'))
        
        if self.path == "/cs/mapview":
            length = int(self.headers['content-length'])
            
            body = self.rfile.read(length)
            # print('Body:', body)
            
            # BONUS: How to convert the body from a JSON string representation of a map to a python dictionary
            
            
            databaseresult = vehicleAPI.getAllVehicleLocations()
            
            
            map_string = json.dumps(databaseresult)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(map_string.encode(encoding='utf_8'))

        if self.path == "/cs/register":
            length = int(self.headers['content-length'])
            body = self.rfile.read(length)

            # BONUS: How to convert the body from a JSON string representation of a map to a python dictionary
            dictionary = json.loads(body)

            companyEmail = dictionary.get("companyEmail")
            companyName = dictionary.get("companyName")
            password = dictionary.get("password")

            databaseresult = fmLoginMethods.registerUser(companyEmail, companyName, password)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            if databaseresult is not None:
                s = databaseresult
                bytes = s.encode('utf-8')
                self.wfile.write(bytes)
            else:
                s = "Could not register the user"
                bytes = s.encode('utf-8')
                self.wfile.write(bytes)

        if self.path == "/cs/login":
            length = int(self.headers['content-length'])
            body = self.rfile.read(length)
            # print('Body:', body)

            # BONUS: How to convert the body from a JSON string representation of a map to a python dictionary
            dictionary = json.loads(body)

            email = dictionary.get("companyEmail")
            password = dictionary.get("password")

            databaseresult = fmLoginMethods.loginUser(email, password)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            print(databaseresult)

            if databaseresult is not None:
                s = str(databaseresult)
                bytes = s.encode('utf-8')
                print(bytes)
                self.wfile.write(bytes)
            else:
                s = "Big Error"
                bytes = s.encode('utf-8')
                self.wfile.write(bytes)


httpd = http.server.HTTPServer(('', 1202), SimpleHTTPRequestHandler)
httpd.serve_forever()
