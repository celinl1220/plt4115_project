#!/bin/bash

if [ ! command -v python3 &>/dev/null ]
then
    echo "Python3 not installed. Please install."
    exit 1
fi

PARSER_FILENAME = "parser.py"
if [ ! -f "$(PARSER_FILENAME)" ]
then
    echo "Parser file $(LEXER_FILENAME) not found!"
    exit 1
fi

if [ $# -eq 0 ]
then
    echo "Usage: ./exec_parser.sh <program_filename>"
    exit 1
fi

PROGRAM_FILENAME = "$1"
if [ ! -f "$(PROGRAM_FILENAME)" ]
then
    echo "File $(PROGRAM_FILENAME) not found!"
    exit 1
fi

echo "Running $(LEXER_FILENAME) on $(PROGRAM_FILENAME)"
python3 "$(LEXER_FILENAME)" "$(PROGRAM_FILENAME)"
