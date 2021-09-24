# import json
# import requests
# import random

# smaple_vehicle = {
# 	'make': 'Honda',
# 	'model': 'Accord',
# 	'eta': '10 min'
# }


# todo: change the destination parameter to longitude and latitude (des_lat, des_long)
def get_vehicle_response(order_id, destination):
	
	# return str(order_id) + "  " + str(destination)
	# res = "got it order Id and Destination!!!!!!"
	# response = {'Response': res}
	# return response
	
	# working uncoment.
	# return "got it order Id and Destination!!!!!!"
	
	re = "Vehicle (Honda Accord) will be arriving in 35 minutes" + " " + "to your location. <br>Location:" + str(destination)
	dic = {
		'response': re
	}
	return str(dic['response'])

def getAvailableVehicle():
	pass