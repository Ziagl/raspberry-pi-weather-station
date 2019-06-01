# this script collects data from 3 sensors connected to a Raspberry Pi
# additionally it requests weather data from an API
# all this data is computed and sent to a storage cloud for further usage

import requests
import json
import re
import os
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT
import time
import base64

debug = 0

api_current_pressure = "";
api_current_temperature = "";
api_current_humidity = "";
sensor_18B20_temperature = "";
sensor_dht11_temperature = "";
sensor_dht11_humidity = "";
sensor_bmp085_temperature = "";
sensor_bmp085_pressure = "";

start = time.time()

########################################################################
# temperature from connected 18B20 sensor
directory = "/sys/bus/w1/devices/"

# find all connected 1-wire devices
devices = os.listdir(directory)

for f in devices:
	if f != "w1_bus_master1":
		file = open(directory+f+"/w1_slave")
		line = file.readline()
		if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES",line):
			line = file.readline()
			m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)",line)
			if m:
				sensor_18B20_temperature = str(float(m.group(2)) / 1000.0)
########################################################################

########################################################################
# humidity and temperature from connected DHT11 sensor
pin = 4		# GPIO Pin number
sensor = Adafruit_DHT.DHT11

h, t = Adafruit_DHT.read_retry(sensor, pin)

sensor_dht11_temperature = str(t)
sensor_dht11_humidity = str(h)
########################################################################

########################################################################
# pressure and humidity from bmp085 sensor
sensor = BMP085.BMP085()
sensor_bmp085_temperature = format(sensor.read_temperature())
sensor_bmp085_pressure = format(sensor.read_pressure() * 0.01)	# Pa to hPa
########################################################################

########################################################################
# weather api code
# hard coded API params
appid = "INSERTAPIKEYHERE"	# create your own at openweathermap.org
city = "Mank"				# name of your city (weather station)
state = "at"				# country code

# create API Url string
url = "https://api.openweathermap.org/data/2.5/weather?q="+city+","+state+"&APPID="+appid

# get weather information by calling REST API interface
r = requests.get(url);

# convert to JSON object
js = r.json()

# print needed values
api_current_pressure = str(js['main']['pressure'])
api_current_temperature = str(js['main']['temp'] - 273.15)	# Kelvin to Celsius
api_current_humidity = str(js['main']['humidity'])
########################################################################

end = time.time()

# debug output
if debug:
	print "API current pressure:      "+api_current_pressure
	print "API current temperature:   "+api_current_temperature
	print "API current humidity:      "+api_current_humidity
	print "18B20 sensor temperature:  "+sensor_18B20_temperature
	print "DHT11 sensor temperature:  "+sensor_dht11_temperature
	print "DHT11 sensor humidity:     "+sensor_dht11_humidity
	print "BMP085 sensor temperature: "+sensor_bmp085_temperature
	print "BMP085 sensor pressure:    "+sensor_bmp085_pressure
	print "{:5.3f}s".format(end-start)

data = {}
data["api_pressure"] = base64.b64encode(api_current_pressure)
data["api_humidity"] = base64.b64encode(api_current_humidity)
data["api_temperature"] = base64.b64encode(api_current_temperature)
data["sensor_18b20_temperature"] = base64.b64encode(sensor_18B20_temperature)
data["sensor_dht11_temperature"] = base64.b64encode(sensor_dht11_temperature)
data["sensor_dht11_humidity"] = base64.b64encode(sensor_dht11_humidity)
data["sensor_bmp085_temperature"] = base64.b64encode(sensor_bmp085_temperature)
data["sensor_bmp085_pressure"] = base64.b64encode(sensor_bmp085_pressure)
data["script_time"] = base64.b64encode("{:5.3f}".format(end-start))
json_data = json.dumps(data)

########################################################################
# send values as json file to webserver

url = "https://domain.com/api.php/"			# replace with your api.php endpoint
token = "SECURITYTOKEN"						# replace with your security token string

r = requests.post(url+token, data=json_data)
if debug:
	print r.text

########################################################################
