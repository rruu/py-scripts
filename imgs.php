<?php
//path to directory to scan. i have included a wildcard for a subdirectory
$directory = "./*";

//get all image files with a .jpg extension.
$images = glob("" . $directory . "*.jpg");

$imgs = '';
// create array
foreach($images as $image){ $imgs[] = "$image"; }

foreach ($imgs as $img) {
    echo "<img src='$img' /> ";
}
?>
