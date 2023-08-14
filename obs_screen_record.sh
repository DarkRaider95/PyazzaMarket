#!/bin/bash

# Start OBS screen recording
obs --startrecording >> /dev/null 2>&1 & 

# Get the OBS process ID
obs_pid=$!

# Wait for the Python script to finish
python main.py -t

# Stop OBS screen recording by killing the OBS process
kill -s INT $obs_pid