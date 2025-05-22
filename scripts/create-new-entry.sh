#!/bin/sh

# create new draft
read -p "Enter html file name: " filename
file="./entries/$filename.html"
cp ./_templates/html.template $file

read -p "Enter markdown name: " md
mdfile="./md/$md.md"
cp ./_templates/markdown.template $mdfile


# fill in info
read -p "Enter title: " entrytitle
sed -i "" "s/!!!TITLE!!!/$entrytitle/g" "$file"
sed -i "" "s/!!!FILE!!!/$md/g" "$file"
echo "0. [$entrytitle]($file)" >> ./md/index.md

# # display blog post details
# echo
# echo "File: $file"
# cat "$file"
