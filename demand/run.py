import storeServiceRequest
import http.server
from http.server import BaseHTTPRequestHandler
import json


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # def do_OPTIONS(self):
    #
    #     self.send_response(200)
    #     self.end_headers()
    #     self.wfile.write(b'Hello, World! OPTIONS')

    def do_POST(self):
        # self.send_response(200)
        # self.end_headers()
        # self.wfile.write(b'Hello, world! GET')

        # Getting the path of the request
        # print('Path:', self.path)

        # You can get all headers via self.headers
        # or identify which header you want to get!
        # print('Headers: " ', self.headers, ' " ')
        # print('Header1:', self.headers['header1'])

        # This is how you can read the body, its a couple steps so maybe make a helper function.
        length = int(self.headers['content-length'])
        body = self.rfile.read(length)
        # print('Body:', body)

        # BONUS: How to convert the body from a JSON string representation of a map to a python dictionary
        dictionary = json.loads(body)
        databaseresult = "No response"

        sType = dictionary.get("serviceType")
        dAddress = dictionary.get("destinationAddress")
        uName = dictionary.get("username")

        databaseresult = storeServiceRequest.insertOrderIntoDB(sType, dAddress, uName)

        self.send_response(200)

        # Very important or your response will be SLOW
        self.end_headers()
        s = databaseresult

        # Finally, the body! The body receives bytes, so if you have a string, this is how to convert it to a bytes!
        # s = 'Success!!!!!'
        bytes = s.encode('utf-8')
        self.wfile.write(bytes)


httpd = http.server.HTTPServer(('', 1201), SimpleHTTPRequestHandler)
httpd.serve_forever()
