#Start ssh for Docker container, created on 29 sept 2021
#tested work on ubuntu
#/bin/bash

service ssh status > /tmp/ssh.status
result=$(cat /tmp/ssh.status | awk '{print$4}')
ssh="not"

if [[ "$ssh" == "$result" ]]
then
	/etc/init.d/ssh start
fi

