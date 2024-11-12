#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Please install it."
    exit 1
fi

# Check if parser.py exists
PARSER_FILENAME="parser1.py"
TOKENS_FILE="tokens.txt"

if [ ! -f "$PARSER_FILENAME" ]; then
    echo "Parser file $PARSER_FILENAME not found!"
    exit 1
fi

# Check if tokens.txt exists and has content
if [ ! -s "$TOKENS_FILE" ]; then
    echo "Tokens file $TOKENS_FILE not found or is empty! Run exec_lexer.sh first."
    exit 1
fi

# Run the parser with the generated tokens file
echo "Running $PARSER_FILENAME with tokens from $TOKENS_FILE"
python3 "$PARSER_FILENAME" "$TOKENS_FILE"
