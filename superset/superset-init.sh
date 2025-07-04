#!/bin/bash

#create the superset user
echo $ADMIN_USERNAME
superset fab create-admin --username $ADMIN_USERNAME --firstname Admin --lastname User --email $ADMIN_EMAIL --password $ADMIN_PASSWORD

# Initialize the database
superset db upgrade

#setup roles and permissions
superset superset init

#start the superset server
/bin/sh -c /usr/bin/run-server.sh
