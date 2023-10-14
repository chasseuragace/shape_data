#!/bin/zsh

# Replace 'your/directory/path' with the path to the directory you want to list
directory_path="h_data"

# List subdirectories and files in the specified directory
echo "Contents of directory: $directory_path"

# List subdirectories
echo "Subdirectories:"
find "$directory_path" -type d -exec du -sh {} \;

# List files
echo "Files:"
find "$directory_path" -type f -exec du -h {} \;
