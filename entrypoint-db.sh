#!/usr/bin/bash
name=$("select user from mysql.user where user = 'bit'" | mysql -uroot -pbit mysql)
bit="bit"

until ($name == $bit); do
    echo $name
    name = $("select user from mysql.user where user = 'bit'" | mysql -uroot -pbit mysql)
    sleep 20
done
echo $name

