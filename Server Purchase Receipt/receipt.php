<!DOCTYPE html>
<html>
<head>
<Title>Purchase/Receipt Server</Title>
<meta charset="UTF-8">
<link href="styles.css" type="text/css" rel="stylesheet" />
</head>
<body>
<!--  author: Andrew deBerardinis -->
<body>
<div class="receipt">
<h3>Receipt</h3>

<?php
$fname = ($_POST ["firstName"]);
$lname = ($_POST ["lastName"]);
$city = ($_POST ["city"]);
$state = ($_POST ["state"]);
$zip = ($_POST ["zip"]);
$howMany = intVal ( ($_POST ["quantity"]) );
$index = strrpos ( $_POST ["size"], ' ' );
$size = substr ( $_POST ['size'], 0, $index );
$cost = 1.0 * (substr ( $_POST ['size'], $index ));
date_default_timezone_set('America/Phoenix');
$date = date ( "d-F-Y" );
echo "Purchase date: " . $date . "<br>";

// TODO: Complete the receipt to replace the purchase form.
// The following three echos represent a test that we can
// access the values of some of the the input fields.
echo "Purchased " . $howMany . " item(s) of size '" . $size . "' at " . $cost . " each<br>";
echo "Total Cost: $" . 1.0 * $cost*$howMany . "<br><br>";
echo "<fieldset><legend>Ship to</legend>" . $fname . " " . $lname . "<br>" . $city . ", " . $state;
echo "<br>" . $zip . "</fieldset>";
?>

</div>
</body>
</html>
