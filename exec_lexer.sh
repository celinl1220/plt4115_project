#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Please install it."
    exit 1
fi

# Check if lexer.py exists
LEXER_FILENAME="lexer.py"
if [ ! -f "$LEXER_FILENAME" ]; then
    echo "Lexer file $LEXER_FILENAME not found!"
    exit 1
fi

# Check if a program filename was provided as an argument
if [ $# -eq 0 ]; then
    echo "Usage: ./exec_lexer.sh <program_filename>"
    exit 1
fi

PROGRAM_FILENAME="$1"
TOKENS_FILE="tokens.txt"

# Check if the program file exists
if [ ! -f "$PROGRAM_FILENAME" ]; then
    echo "File $PROGRAM_FILENAME not found!"
    exit 1
fi

# Run the lexer on the program file and save output to tokens.txt
echo "Running $LEXER_FILENAME on $PROGRAM_FILENAME"
python3 "$LEXER_FILENAME" "$PROGRAM_FILENAME" > "$TOKENS_FILE"

# Check if tokens were generated successfully
if [ ! -s "$TOKENS_FILE" ]; then
    echo "Lexer did not produce any tokens. Check lexer output for errors."
    exit 1
fi

echo "Tokens saved to $TOKENS_FILE"
