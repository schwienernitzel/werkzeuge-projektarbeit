#!/bin/bash

echo -e "\033[31mStart: Welcome to the random comment picker!\033[0m"

INPUT_FILE=$1
TEMP_FILE="out/hate-temp.csv"
OUTPUT_FILE="out/hate-random.csv"

mkdir -p "$(dirname "$TEMP_FILE")"
rm -rf "$TEMP_FILE"
touch "$TEMP_FILE"

if [ -z "$AMOUNT" ]; then
  echo "ERROR: AMOUNT is not set!"
  exit 1
fi

if [ -z "$INPUT_FILE" ]; then
  echo "ERROR: No input file defined!"
  exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
  echo "ERROR: $INPUT_FILE does not exist!"
  exit 1
fi

echo -e "\033[33mDebug:\033[0m AMOUNT=$AMOUNT"
echo -e "\033[33mDebug:\033[0m INPUT_FILE=$INPUT_FILE"
echo -e "\033[33mDebug:\033[0m TEMP_FILE=$TEMP_FILE"
echo -e "\033[33mDebug:\033[0m OUTPUT_FILE=$OUTPUT_FILE"

line_count=$(wc -l < "$INPUT_FILE")

echo -e "\033[33mDebug:\033[0m Number of total lines: $line_count"
awk 'BEGIN {srand()} {print rand() "\t" $0}' "$INPUT_FILE" | sort -k1,1n | cut -f2- | head -n "$AMOUNT" > "$TEMP_FILE"

if [ $? -ne 0 ]; then
  echo "ERROR: Failed to shuffle lines from $INPUT_FILE"
  exit 1
fi

if [ ! -s "$TEMP_FILE" ]; then
  echo "ERROR: Output file is empty!"
  exit 1
fi

touch $OUTPUT_FILE
sed -E 's/([0-9]+) ([0-9]+) ([0-9]+) ([0-9]{4}-[0-9]{2}-[0-9]{2}) ([0-9]{2}:[0-9]{2})/\1\t\2\t\3\t\4\t\5\t/' $TEMP_FILE > $OUTPUT_FILE
rm -rf $TEMP_FILE

echo -e "\033[32mCompleted: $AMOUNT lines of $INPUT_FILE were picked and copied to $OUTPUT_FILE\033[0m"