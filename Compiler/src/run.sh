#!/bin/bash

ls
# Go to the source directory and compile
gcc lexer.c -o ../bin/lexer
gcc parser.c -o ../bin/parser

# Check if a file path is provided
cd ../data

if [ -z "$1" ]; then
  echo "Usage: $0 file (under data directory)"
  exit 1
fi

# Wait until the file exists
while [ ! -f "$1" ]; do
  echo "Waiting for file '$1' to exist. Press Ctrl+C to cancel."
  sleep 2
done


# Go to the bin directory and run the programs
cd ../bin
./lexer "../data/$1" 
./parser
