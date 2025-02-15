#!/bin/bash
cd /home/leopard/development/blogs/reports || exit
npm_config_yes=true npx pagefind --source "public" --bundle-dir ../static/_pagefind
hugo
cp ads.txt public/ads.txt
git add .
current_date=$(date +"%Y-%m-%d")
# commit_message=${1:-"release $current_date"}
git commit -m "release $current_date"
git push