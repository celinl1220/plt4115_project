#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Please install it."
    exit 1
fi

# Check if parser.py exists
PARSER_FILENAME="parser1.py"
TOKENS_FILE="tokens.txt"
OUTPUT_FILE="parsed_output.txt"

if [ ! -f "$PARSER_FILENAME" ]; then
    echo "Parser file $PARSER_FILENAME not found!"
    exit 1
fi

# Check if tokens.txt exists and has content
if [ ! -s "$TOKENS_FILE" ]; then
    echo "Tokens file $TOKENS_FILE not found or is empty! Run exec_lexer.sh first."
    exit 1
fi

# Run the parser with the generated tokens file and redirect output to parsed_output.txt
echo "Running $PARSER_FILENAME with tokens from $TOKENS_FILE"
python3 "$PARSER_FILENAME" "$TOKENS_FILE" > "$OUTPUT_FILE"

# Check if the parser executed successfully
if [ $? -ne 0 ]; then
    echo "Parser failed. Check for errors in $TOKENS_FILE or $PARSER_FILENAME."
    exit 1
fi

# Confirm output
if [ -s "$OUTPUT_FILE" ]; then
    echo "Parsing completed successfully! Output written to $OUTPUT_FILE"
else
    echo "Parsing failed. Output file $OUTPUT_FILE is empty."
    exit 1
fi