#!/bin/bash

# Check if lexer binary exists, if not compile
if [ ! -f ../bin/lexer ]; then
  echo "Compiling lexer..."
  gcc ../src/lexer.c -o ../bin/lexer
else
  echo "Lexer binary already exists, skipping compilation."
fi

# Check if parser binary exists, if not compile
if [ ! -f ../bin/parser ]; then
  echo "Compiling parser..."
  gcc ../src/parser.c -o ../bin/parser
else
  echo "Parser binary already exists, skipping compilation."
fi

cd ../data

if [ -z "$1" ]; then
  echo "Usage: $0 file (under data directory)"
  exit 1
fi

while [ ! -f "$1" ]; do
  echo "Waiting for file '$1' to exist. Press Ctrl+C to cancel."
  sleep 2
done

cd ../bin

./lexer "../data/$1"
./parser
echo "Lexer and parser executed successfully."