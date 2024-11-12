#!/bin/bash

# Check for Python 3
if ! command -v python3 &>/dev/null; then
    echo "Python3 not installed. Please install."
    exit 1
fi

# Define filenames correctly without spaces around "="
PARSER_FILENAME="parser.py"
LEXER_FILENAME="lexer.py"

# Check if parser and lexer files exist
if [ ! -f "$PARSER_FILENAME" ]; then
    echo "Parser file $PARSER_FILENAME not found!"
    exit 1
fi

if [ ! -f "$LEXER_FILENAME" ]; then
    echo "Lexer file $LEXER_FILENAME not found!"
    exit 1
fi

# Check if a program filename was provided as an argument
if [ $# -eq 0 ]; then
    echo "Usage: ./exec_parser.sh <program_filename>"
    exit 1
fi

PROGRAM_FILENAME="$1"
if [ ! -f "$PROGRAM_FILENAME" ]; then
    echo "File $PROGRAM_FILENAME not found!"
    exit 1
fi

# Run the lexer on the program file and capture output
echo "Running $LEXER_FILENAME on $PROGRAM_FILENAME"
TOKENS=$(python3 "$LEXER_FILENAME" "$PROGRAM_FILENAME")  # Assuming lexer outputs tokens to stdout

# Check if tokens were generated successfully
if [ -z "$TOKENS" ]; then
    echo "Lexer did not produce any tokens. Check lexer output for errors."
    exit 1
fi

# Run the parser with the generated tokens
echo "Running $PARSER_FILENAME on tokens"
python3 "$PARSER_FILENAME" "$TOKENS"
