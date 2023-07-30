#!/bin/bash
symbol="$1"
CDT="https://www.marketwatch.com/investing/stock/$symbol?mod=search_symbol"
output_file="${symbol}.html"
curl -o "$output_file" "$CDT"
java -jar tagsoup-1.2.1.jar --files "$output_file"
xhtml_file=$(echo "$output_file" | sed 's/\.html$/.xhtml/')
/usr/bin/python3 stock.py "$xhtml_file"
rm ".html"
rm ".xhtml"
rm "$output_file"