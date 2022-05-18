#!/bin/bash

myhost=$(hostname)
ip_addr=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1')
sleep 30
echo "this is my script 2" > $myhost.txt
