#!/bin/bash

# Ensure the script is executable
# chmod +x run_generator.sh

#Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install it and try again."
    exit 1
fi

#Run the parser
# Check if an input file was provided as an argument
if [ -z "$1" ]; then
    echo "No input file provided. Usage: ./run_generator.sh <input_file>"
    exit 1
fi

# Run the Python generator
echo "Running code generator for file: $input_file"
python3 generator.py "$1"
