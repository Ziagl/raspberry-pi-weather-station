<?php 
// database connection variables
$db_host="localhost";
$db_name="NAMEDERDATENBANK";			# replace with your database name
$db_user="DATENBANKBENUTZERNAME";		# replace with your database user name
$db_passwd="DATENBANKBENUTZERPASSWORT";	# replace with your datapase user password
// REST API security token
$app_token = "SECURITYTOKEN";			# use same security token as defined in measure.py
 
// database functions
function getDBConnection($db_host, $db_name, $db_user, $db_passwd)
{
	try{
		$con = new PDO("mysql:host=$db_host;dbname=$db_name", $db_user, $db_passwd, array(
				  PDO::ATTR_PERSISTENT => true
				));
		$con->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
		$con->exec("SET CHARACTER SET utf8");
	}catch(PDOException $e)
	{
		return 1;
	}
	return $con;
}

function saveSensorData($params, $data)
{
try{
	$con = $params["con"];

	$sql = "INSERT INTO sensor_data (script_time, api_pressure, api_humidity, api_temperature, sensor_18b20_temperature, sensor_dht11_temperature, sensor_dht11_humidity, sensor_bmp085_temperature, sensor_bmp085_pressure) VALUES (:script_time, :api_pressure, :api_humidity, :api_temperature, :sensor_18b20_temperature, :sensor_dht11_temperature, :sensor_dht11_humidity, :sensor_bmp085_temperature, :sensor_bmp085_pressure)";
	$ps = $con->prepare($sql);
	$ps->bindValue('script_time', $data['script_time']);
	$ps->bindValue('api_pressure', $data['api_pressure']);
	$ps->bindValue('api_humidity', $data['api_humidity']);
	$ps->bindValue('api_temperature', $data['api_temperature']);
	$ps->bindValue('sensor_18b20_temperature', $data['sensor_18b20_temperature']);
	$ps->bindValue('sensor_dht11_temperature', $data['sensor_dht11_temperature']);
	$ps->bindValue('sensor_dht11_humidity', $data['sensor_dht11_humidity']);
	$ps->bindValue('sensor_bmp085_temperature', $data['sensor_bmp085_temperature']);
	$ps->bindValue('sensor_bmp085_pressure', $data['sensor_bmp085_pressure']);
	$ps->execute();
	return "ok";
}catch(Exception $e)
{
	return "Error";
}
}; 

header('Content-type: text/html; charset=utf-8'); 
$con = getDBConnection($db_host, $db_name, $db_user, $db_passwd); 
if(!$con) { echo "Error"; die(); } 

// get the HTTP method, path and body of the request 
$method = $_SERVER['REQUEST_METHOD']; 
$ip = $_SERVER['REMOTE_ADDR']; 
$request = explode('/', trim($_SERVER['PATH_INFO'],'/')); 
$input = json_decode(file_get_contents('php://input'),true); //base64 decoding of $input 
if($input) { 
        foreach($input as $key=>$value) {
	        $input[$key] = base64_decode($value);
        }
}

// get uri details
$token = preg_replace('/[^a-z0-9_]+/i','',array_shift($request));

// check if token is valid
if($token!=$app_token)
{
	echo json_encode(array("response" => "Service currently not available!"));
	die();
}

$params = array("con" => $con, "ip" => $ip);

echo saveSensorData($params, $input);

$con = null;	//close DB Connection
die();