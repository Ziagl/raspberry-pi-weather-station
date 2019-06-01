# Raspberry Pi Weather Station

This Source Code is used to get sensor data from
* DS18B20 temperature sensor
* DHT11 humitity sensor
* BMP085 air pressure sensor
from connected sensors on your Raspberry Pi.

The measure.py script also gets live data from openweathermap.org and send it as JSON
to a web hosted database.

api.php is used as REST interface endpoint to get this data and store it into a MySQL database.

database.sql contains CREATE statement for single table to store sensor data.

All details about hardware and software for this project can be found on my blog:
https://developer-blog.net/raspberry-pi-diy-wetterstation/