from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import os
import time
import random

def get_random_ua():
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    ]
    return random.choice(user_agents)

def get_random_proxy():
    return None  # Placeholder, this function should return a random proxy

def get_headers():
    headers = {
        'user-agent': get_random_ua(),
        'referer': 'https://google.com'  # General-purpose referer
    }
    return headers

def random_delay():
    delays = [7, 4, 6, 2, 10, 19]
    time.sleep(random.choice(delays))

def scrape_images(url):
    print(f"Scraping images from {url}...")
    headers = get_headers()
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        print(f"Failed to fetch {url}. Error: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    images_data = []
    for img_tag in soup.find_all('img'):
        img_url = img_tag.get('src')
        alt_text = img_tag.get('alt', '')
        images_data.append((img_url, alt_text))
    
    print(f"Found {len(images_data)} images on {url}.")
    return images_data

def save_images(images_data, base_url, folder_name="scraped_img_5"):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for img_url, alt_text in images_data:
        # Convert relative URLs to absolute URLs
        absolute_img_url = urljoin(base_url, img_url)
        
        try:
            print(f"Downloading {absolute_img_url}...")
            response = requests.get(absolute_img_url, headers=get_headers(), timeout=10)
            response.raise_for_status()

            # Handle filenames with potential invalid characters
            sanitized_alt_text = "".join([c if c.isalnum() else "_" for c in alt_text])
            file_name = os.path.join(folder_name, sanitized_alt_text + ".jpg" if sanitized_alt_text else "unnamed.jpg")
            
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Saved as {file_name}.")
        except requests.RequestException as e:
            print(f"Failed to download {absolute_img_url}. Error: {e}")
        
        random_delay()

images_data = scrape_images("https://www.spriters-resource.com/pc_computer/stardewvalley/")  # Replace with target URL
save_images(images_data, "https://www.spriters-resource.com")

