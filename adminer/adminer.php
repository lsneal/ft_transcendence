<?php
if(!count($_GET)) {
  $_POST['auth'] = [
    'server' => 'WORDPRESS_DB_HOSTNAME',
    'username' => 'MYSQL_USER_NAME',
    'password' => 'MYSQL_USER_PASSWORD',
    'driver' => 'server',
    'db'    => 'MYSQL_DATABASE_NAME'
  ];
}

include "./adminer-4.8.1.php";
