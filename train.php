<?php
header("Access-Control-Allow-Origin: *");

if(isset($_GET['project_name']) && isset($_GET['dataset-location']) && isset($_GET['dataset-size']) && isset($_GET['algorithm']) && isset($_GET['type']) && isset($_GET['value']) && isset($_GET['meta-component']))
{
	$meta_component = $_GET['meta-component'];
	$project_name = explode("--In Project : ", $meta_component)[1];
	$project_path = str_replace(" ","\ ",$project_name);
	$dataset_location = "/var/www/html/winifier/server/projects/".$project_path."/__data__/".$_GET['dataset-location'];
	$dataset_size = $_GET['dataset-size'];
	$algorithm = $_GET['algorithm'];
	$train_type = $_GET['type'];
	$train_value = $_GET['value'];

	if($train_type == "Percentage Split"){
		$train_type = "percentage_split";
	}
	else if($train_type == "Cross Validation"){
		$train_type = "cross_validation";
	}
	mkdir("/var/www/html/winifier/server/projects/".$project_name."/__preprocess__/", 0777, true);
	mkdir("/var/www/html/winifier/server/projects/".$project_name."/__train__/", 0777, true);
	mkdir("/var/www/html/winifier/server/projects/".$project_name."/__model__/generated/", 0777, true);
	exec("chmod 777 -R projects/".$project_name);
	//echo '/home/ubuntu/anaconda3/envs/tensorflow_p36/bin/python Winifier.py "'.$project_name.'" train "'.$dataset_location.'" '.$dataset_size.' '.$algorithm.' '.$train_type.' '.$train_value.' 2>&1';
	$output = shell_exec('/home/ubuntu/anaconda3/envs/tensorflow_p36/bin/python Winifier.py "'.$project_name.'" train '.$dataset_location.' '.$dataset_size.' '.$algorithm.' '.$train_type.' '.$train_value.' 2>&1');
	echo "<pre>".$output."</pre>";
}
?>