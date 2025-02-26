#!/bin/bash
set -e  # Exit on any error

cd /home/leopard/development/blogs/reports || exit 1
echo "Running pagefind..."
npm_config_yes=true npx pagefind --source "public" --bundle-dir ../static/_pagefind
echo "Building site with Hugo..."
hugo
echo "Copying ads.txt..."
cp ads.txt public/ads.txt
git add .
current_date=$(date +"%Y-%m-%d")
commit_message=${1:-"Release $current_date"}
git commit -m "$commit_message"
git push
echo "Deployment completed successfully!"