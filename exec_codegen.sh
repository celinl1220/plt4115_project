#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Please install it."
    exit 1
fi

# Check if Node.js and npm are installed (for Tone.js installation)
if ! command -v node &>/dev/null || ! command -v npm &>/dev/null; then
    echo "Node.js and npm are required for Tone.js. Please install them."
    exit 1
fi

# Ensure Tone.js is installed or available
if [ ! -d "node_modules/tone" ]; then
    echo "Tone.js not found in node_modules. Installing Tone.js..."
    npm install tone
    if [ $? -ne 0 ]; then
        echo "Failed to install Tone.js. Check your npm setup."
        exit 1
    fi
fi

# Check if codegen.py exists
CODEGEN_FILENAME="codegen.py"
AST_FILE="ast.txt"

if [ ! -f "$CODEGEN_FILENAME" ]; then
    echo "Codegen file $CODEGEN_FILENAME not found!"
    exit 1
fi

# Check if ast.txt exists and has content
if [ ! -s "$AST_FILE" ]; then
    echo "AST file $AST_FILE not found or is empty! Run exec_parser.sh first."
    exit 1
fi

# Run the code generation script with the AST file
echo "Running $CODEGEN_FILENAME with AST from $AST_FILE"
python3 "$CODEGEN_FILENAME" "$AST_FILE"

# Provide feedback for running the generated JavaScript
GENERATED_JS="generated_script.js"
if [ -f "$GENERATED_JS" ]; then
    echo "Code generation completed. The JavaScript file $GENERATED_JS has been created."
    echo "You can run it in a browser or using Node.js with the Tone.js library."
else
    echo "Code generation failed. Please check the output of $CODEGEN_FILENAME."
    exit 1
fi
