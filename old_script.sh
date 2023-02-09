#!/bin/bash

set -o nounset
set -o errexit
set -o pipefail

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

function get_names() {
    curl -s "https://api.twitter.com/1.1/followers/list.json?screen_name=${TWITTER_USER}&count=200" -H "Authorization: Bearer ${TWITTER_TOKEN}" | \
        jq '.users | map({id: .id_str, screen_name: .screen_name, name: .name}) | sort'
}

function write_diff() {
    echo "${2}:" | tr '_' '/' >> "${__dir}/diff.json"
    diff <(jq -r '.[].id' "${__dir}/${1}.json") <(jq -r '.[].id' "${__dir}/${2}.json") | grep -E "^[<>]" >> "${__dir}/diff.json" || true
}

today=$(date +%Y_%m_%d)

get_names > "${__dir}/${today}.json"

write_diff "latest" "${today}"
rm "${__dir}/latest.json"
mv "${__dir}/${today}.json" "${__dir}/latest.json"
