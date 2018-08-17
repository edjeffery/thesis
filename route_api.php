<html>
<body>
<h1>Inserting route air quality data</h1>
<?php
require_once "DB.php";
$host="mysql5host.bath.ac.uk";
$user="ej301";
$password="Aesoh8oWPu1xohMu";
$database="ej301";
$dsn="mysql://$user:$password@$host/$database";
$db = DB::connect($dsn);
if (DB::isError($db)) {
die ($db->getMessage());
}

echo $_FILES['file']['size'];
var_dump($_POST);

$uploaddir = "";
$uploadfile = $uploaddir . basename( $_FILES['file']['name']);
echo $uploadfile;
echo "<br>";

if(move_uploaded_file($_FILES['file']['tmp_name'], $uploadfile))
{
  echo "The file has been uploaded successfully";
  echo "<br>";
}
else
{
  echo "There was an error uploading the file";
  echo "<br>";
}

//$fileContent = file_get_contents($uploadfile);
//echo $fileContent;
//echo "<br>";
//echo "<br>";

$data_upload_success = False;

$serial_num = 0;
$time = 0;
$rows_inserted = -1; // -1 as counter iterates one more than necessary
$file_size = filesize($uploadfile);
$csv_string = "";

$CSVfp = fopen($uploadfile, "r");
$CSVfp2 = fopen($uploadfile, "r");
if($CSVfp !== FALSE) {
 while(! feof($CSVfp)) {
  $csv_string .= fgets($CSVfp2);
  $data = fgetcsv($CSVfp, 1000, ",");
  print_r($data);
  echo "<br>";
  $rows_inserted++;
  if(is_array($data)) {
    $DataArr = array();
    $serial_num = $data[0];
    $time = $data[1];
    // longitude = 2
    // latitude = 3
    // pm_raw = 4
    // mq131 = 5
    // mq135 = 6
    // altitude = 7
    // horizontal_speed = 8
    // temp = 9
    // humidity = 10
    $DataArr[] = "('$data[0]', '$data[1]', '$data[2]', '$data[3]', '$data[4]', '$data[5]', '$data[6]', '$data[7]', '$data[8]', '$data[9]', '$data[10]')";
    //echo implode(',', $DataArr);
    //echo "<br>";
    //echo "<br>";

    $query = "INSERT INTO route_air_quality (serial_num, time, latitude, longitude, pm_raw, mq131, mq135, altitude, horizontal_speed, temp, humidity) VALUES ";
    $query .= implode(',', $DataArr);
    //echo $query;

    $result = $db->query($query);
    if (DB::isError($result)) {
    echo "<p>Not successful: " . $result->getMessage() .
    		"</p>";
    }
    else {
      echo "<p>Done</p>\n";
      $data_upload_success = $data_upload_success;
    }
  }
 }
 if ($data_upload_success == True) {
   // Store monitoring data
   $SystemData = array();
   $SystemData[] = "('$serial_num', '$time', '$rows_inserted', '$file_size', '$csv_string')";
   $monitoring_query = "INSERT INTO system_monitoring (serial_num, time, rows_inserted, file_size, csv) VALUES ";
   $monitoring_query .= implode(',', $SystemData);
   $result = $db->query($monitoring_query);
   if (DB::isError($result)) {
     echo "<p>System monitoring upload not successful: " . $result->getMessage() .
         "</p>";
   }
 }
}
fclose($CSVfp);

$db->disconnect();
?>
<p>Finished</p>
</body>
</html>
