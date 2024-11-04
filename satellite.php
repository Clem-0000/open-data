<?php
$norad_id = $_GET['norad_id'];
header('Content-Type: application/json');
// $urlsatellite = "https://api.n2yo.com/rest/v1/satellite/tle/20436&apiKey=U9J3VY-5D8CUZ-7GNUDL-5CR1";
$urlsatellite = "https://api.n2yo.com/rest/v1/satellite/tle/" . $norad_id . "&apiKey=U9J3VY-5D8CUZ-7GNUDL-5CR1";
$contentsatellite = file_get_contents($urlsatellite);
$jsonsatellite = json_decode($contentsatellite, true);

echo json_encode($jsonsatellite);
