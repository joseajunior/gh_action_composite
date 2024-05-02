#!/bin/sh -l

report_path=$1
github_token=$2
pr=$3
only_summary=$4
passed=$5
owner="$(echo "$6" | awk -F / '{print $1}' | sed -e "s/:refs//")"
repo="$(echo "$6" | awk -F / '{print $2}' | sed -e "s/:refs//")"

python /report.py -r "$report_path" -p "$passed" -o "/report.md"

# If not only summary, run post.py
if [ "$only_summary" = false ]; then
    python /post.py -gt "$github_token" -pr "$pr" -o "$owner" -rp "$repo" -f "/report.md"
fi
