#!/bin/bash

# Start OBS screen recording
obs --startrecording &

# Get the OBS process ID
obs_pid=$!

# Wait for the Python script to finish
python main.py

# Stop OBS screen recording by killing the OBS process
kill -s INT $obs_pid