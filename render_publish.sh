#!/bin/bash

cd /home/leopard/development/blogs/reports || exit
hugo
cp ads.txt public/ads.txt
git add .
current_date=$(date +"%Y-%m-%d")
commit_message=${1:-"release $current_date"}
git commit -m "$commit_message"
git push
