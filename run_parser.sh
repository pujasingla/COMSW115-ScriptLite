#!/bin/bash

# Shell script to run the lexer for ScriptLite

#Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install it and try again."
    exit 1
fi

#Run the parser
# Check if an input file was provided as an argument
if [ -z "$1" ]; then
    echo "No input file provided. Usage: ./run_parser.sh <input_file>"
    exit 1
fi

# Run the parser (assuming ast_parser.py takes the input file as an argument)
echo "Running the parser..."
python3 ast_parser.py "$1"

# Notify the user if the execution was successful
if [ $? -eq 0 ]; then
    echo "Parser executed successfully."
else
    echo "Parser encountered an error."
fi
