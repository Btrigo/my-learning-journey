#!/bin/bash

# get the file name from the first argument or use today's date 
FILENAME="${1:-$(date +%Y-%m-%d).md}"

# get script directory and build relative path to template
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE="$SCRIPT_DIR/../templates/daily-log-template.md"

# create in daily-logs directory
OUTPUT_DIR="$SCRIPT_DIR/../daily-logs"
mkdir -p "$OUTPUT_DIR"  # Creates directory if it doesn't exist

# copy template to daily-logs directory
cp "$TEMPLATE" "$OUTPUT_DIR/$FILENAME"
echo "✅ Created $OUTPUT_DIR/$FILENAME"