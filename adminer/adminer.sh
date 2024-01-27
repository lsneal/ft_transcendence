#!/bin/sh

wget https://github.com/vrana/adminer/releases/download/v4.8.1/adminer-4.8.1.php -P /lib/adminer

mv /lib/adminer/adminer-4.8.1.php /lib/adminer/adminer.php

exec php-fpm81 -F
