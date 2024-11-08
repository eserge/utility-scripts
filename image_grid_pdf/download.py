import sys
import os
import urllib.request
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


# get URL from the first argument
URL = sys.argv[1]

if not URL:
    print("Usage: python download.py <URL> <target_dir>")
    sys.exit(1)

target_dir = sys.argv[2]
if not target_dir:
    print("Usage: python download.py <URL> <target_dir>")
    sys.exit(1)

if not os.path.exists(target_dir):
    print(f"Creating directory: {target_dir}")
    os.makedirs(target_dir)


# URL = "https://pdd.by/pdd/ru/a2-p1/"

def download_images(url):
    # Send a GET request to the specified URL
    response = requests.get(url)
    
    # Check if request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return

    # Parse the webpage content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all image tags
    img_tags = soup.find_all('img')

    for img in img_tags:
        img_url = img.get('src')
        
        # Skip if no URL is found
        if not img_url:
            continue
        
        # Join the base URL with the image URL (in case it's relative)
        img_url = urljoin(url, img_url)
        
        # Check if the image URL ends with .png
        if img_url.lower().endswith('.png'):
            # Extract image filename

            img_name = os.path.join(target_dir, os.path.basename(img_url))
            print(f"Saving image to: {img_name}")
            
            # Download and save the image
            try:
                print(f"Downloading {img_name}...")
                urllib.request.urlretrieve(img_url, img_name)
                print(f"{img_name} downloaded successfully.")
            except Exception as e:
                print(f"Failed to download {img_name}. Error: {e}")

# Usage
print("Downloading images from: ", URL)
download_images(URL)
