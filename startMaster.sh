#!/bin/bash

user="Richard-Lynch"
repo="flask_test"

if [[ $# == 2 ]] ; then
    user="$1"
    repo="$2"
fi

json_template='{
    user: $u,
    repo: $r
}'

address="http://127.0.0.1:8080"

jq -n --arg u "$user" \
    --arg r "$repo" "$json_template" |
    curl -sS -X POST \
    -H "Content-Type: application/json" \
    -d@- \
    "$address"/start
