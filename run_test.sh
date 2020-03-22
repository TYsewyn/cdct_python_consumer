#!/bin/bash

spring cloud stubrunner &
STUBRUNNER_PID=$!

echo "Waiting for 15 seconds for stubrunner to boot properly"
sleep 15

python -m unittest discover -p "*_it.py"

kill $STUBRUNNER_PID
