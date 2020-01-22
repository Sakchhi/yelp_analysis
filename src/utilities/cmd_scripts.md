### Exclude large files from tracking by adding to gitignore
find . -size +90M | sed 's|^\./||g' | cat >> .gitignore; awk '!NF || !seen[$0]++' .gitignore