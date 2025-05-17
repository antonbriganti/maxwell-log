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

# add to index 
newline="                <li><a href=\"$file\">$entrytitle</a></li>"

# Use printf to insert actual newline and feed into sed
sed -i '' "/<ol id=\"toc\">/,/<\/ol>/ {
    /<\/ol>/ {
        s/<\/ol>/PLACEHOLDER/
    }
}" index.html

# Now replace placeholder with proper HTML using printf
printf "%s\n%s\n" "$newline" "                </ol>" | sed -i '' -e '/PLACEHOLDER/{
    r /dev/stdin
    d
}' index.html



# display blog post details
echo
echo "File: $file"
cat "$file"
