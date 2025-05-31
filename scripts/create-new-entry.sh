#!/bin/sh

# create new post
file_number=$(($(ls md/| grep -E '^[0-9]+-' | sed -E 's/^([0-9]+)-.*/\1/' | sort -n | tail -n 1)+ 1))
read -p "Enter mission (e.g. mission-01): " mission
read -p "Enter article filename (e.g. session-01): " article
mdfile="./md/0$file_number-$mission-$article.md"
cp ./_templates/template.md $mdfile


# fill in info
read -p "Enter title: " entrytitle
sed -i "" "s/!!!TITLE!!!/$entrytitle/g" "$mdfile"
echo "0. [$entrytitle](entry/$mission-$article)" >> ./md/index.md