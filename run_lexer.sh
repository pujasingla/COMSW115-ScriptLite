#!/bin/bash

# Shell script to run the lexer for ScriptLite

#Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install it and try again."
    exit 1
fi

#Run the lexer
# Check if an input file was provided as an argument
if [ -z "$1" ]; then
    echo "No input file provided. Usage: ./run_lexer.sh <input_file>"
    exit 1
fi

# Run the lexer (assuming scanner.py takes the input file as an argument)
echo "Running the lexer..."
python3 scanner.py "$1"

# Notify the user if the execution was successful
if [ $? -eq 0 ]; then
    echo "Lexer executed successfully."
else
    echo "Lexer encountered an error."
fi
