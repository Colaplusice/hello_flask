#!/usr/bin/env bash

#  docker exec mysql mysql -u root -h 127.0.0.1 -e "create database $1 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
docker exec -i mysql mysql -uroot -h 127.0.0.1 hello_flask < hello_flask.sql


