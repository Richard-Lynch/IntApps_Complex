#!/bin/bash


json_template='{
    stop: $s
}'

address="http://127.0.0.1:8080"

jq -n --arg s "True" "$json_template" |
    curl -sS -X POST \
    -H "Content-Type: application/json" \
    -d@- \
    "$address"/start
