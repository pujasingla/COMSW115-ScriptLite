#!/bin/bash

mkdir -p dir1 dir2 dir3

# Function to generate random files in a directory
generate_random_files() {
  local dir=$1
  local extensions=("docx" "pdf" "jpg" "log")
  
  # Create 5 random files for each extension in the given directory
  for ext in "${extensions[@]}"; do
    for i in {1..5}; do
      # Create a random file name and touch it in the given directory
      touch "$dir/$(openssl rand -hex 5).$ext"
    done
  done
}

# Generate files in each directory
generate_random_files "dir1"
generate_random_files "dir2"
generate_random_files "dir3"

echo "Directories and files have been created successfully!"