#!/bin/bash

# Directory where you want to save the downloaded files
download_dir="figshare_downloads"

# Create the download directory if it doesn't exist
mkdir -p "$download_dir"

# Initialize page counter
page=1

# Loop to handle pagination
while : ; do
  # Figshare collection URL with pagination
  collection_url="https://api.figshare.com/v2/collections/3917698/articles?page=$page"

  # Fetch the list of articles in the collection
  articles=$(curl -s "$collection_url")

  # Check if the articles list is empty, then break
  if [ -z "$articles" ] || [ "$articles" == "[]" ]; then
    break
  fi

  # Loop through each article
  echo "$articles" | jq -r '.[] | .id' | while read -r article_id; do
    echo "Processing article ID: $article_id"

    # Fetch the list of files for this article
    files_url="https://api.figshare.com/v2/articles/$article_id/files"
    files=$(curl -s "$files_url")

    # Download each file
    echo "$files" | jq -r '.[] | "\(.id) \(.name)"' | while read -r file_id file_name; do
      echo "Downloading file: $file_name"

      file_url="https://api.figshare.com/v2/articles/$article_id/files/$file_id/download"
      curl -o "$download_dir/$file_name" "$file_url"

      if [ $? -ne 0 ]; then
        echo "Failed to download file $file_name"
      fi
    done
  done

  # Increment page counter
  ((page++))
done

echo "Download complete."

