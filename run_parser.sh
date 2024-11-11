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

INPUT_DIR="Parser_Input_Programs/"

# Combine the directory path with the provided file name
INPUT_FILE="${INPUT_DIR}$1"

# Check if the file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "File not found: $INPUT_FILE"
    exit 1
fi

# Run the parser (assuming ast_parser.py takes the input file as an argument)
echo "Running the parser..."
python3 ast_parser.py "$INPUT_FILE"

# Notify the user if the execution was successful
if [ $? -eq 0 ]; then
    echo "Parser executed successfully."
else
    echo "Parser encountered an error."
fi
