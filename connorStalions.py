import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def create_directory(path):
    """Helper function to create directories if they don't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")  # Debug: Indicate when a directory is created

def download_play_image(img_url, play_name, path):
    """Helper function to download and save the play image."""
    create_directory(path)  # Ensure the directory exists
    response = requests.get(img_url)
    if response.status_code == 200:
        img_path = os.path.join(path, f"{play_name}.png")
        with open(img_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded and saved image: {img_path}")  # Debug: Indicate when an image is downloaded and saved
    else:
        print(f"Failed to download image: {img_url}")  # Debug: Indicate if image download failed

def traverse_playbook(base_url, current_url, current_path, visited=set()):
    # Avoid revisiting the same page
    if current_url in visited:
        return
    visited.add(current_url)

    # Send a GET request to the current webpage
    try:
        response = requests.get(current_url)
        response.raise_for_status()  # Check that the request was successful
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {current_url}: {e}")
        return

    # Parse the webpage content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Look for all anchor tags with href attributes
    anchors = soup.find_all('a', href=True)

    # Track whether we find any more paths to follow
    found_sub_paths = False

    for anchor in anchors:
        href = anchor['href']
        full_url = urljoin(current_url, href)

        # Skip any URLs containing fragments or specific unwanted substrings
        if '#' in href or '/#' in href or 'jeg_' in href:
            continue

        # Check if the href is a sub-path of the current path (i.e., extends the current path)
        if full_url.startswith(base_url) and full_url not in visited:
            # Check if the sub-path ends with '/', if so, treat it as a directory
            if full_url.endswith('/'):
                # Calculate relative path only for non-final plays
                relative_path = os.path.relpath(urlparse(full_url).path, urlparse(base_url).path)
                sub_path = os.path.join(current_path, os.path.basename(urlparse(relative_path).path))
                traverse_playbook(base_url, full_url, sub_path, visited)
            found_sub_paths = True

    # If no sub-paths were found, check if it's a final play by looking for an image without an anchor tag
    if not found_sub_paths:
        play_images = soup.find_all('img', src=True)
        for img in play_images:
            img_src = img['src']
            # Check if the image source matches the pattern of a final play image
            if img_src.startswith("https://collegefootball.gg/wp-content/plugins/playbook/playbook_images_ncaa-25/"):
                # This is likely a final play, so download the image with the play name
                play_name = os.path.basename(urlparse(current_url).path.rstrip('/'))
                # Save the image in the current path's parent directory
                download_play_image(img_src, play_name, os.path.dirname(current_path))
                return

def main():
    # User input for the playbook school
    school = input("Enter the name of the school to steal from: ").strip().lower().replace(" ", "-")

    # Base URL for the school's offense playbook
    base_url = f'https://collegefootball.gg/playbooks/{school}/offense/'

    # Check if the school exists by attempting to access the base URL
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Could not find the school at {base_url}: {e}")
        return

    # If the school exists, proceed to create the playbook
    starting_path = f'{school.capitalize()}_Offense_Playbook'
    create_directory(starting_path)  # Ensure the base directory is created
    traverse_playbook(base_url, base_url, starting_path)

if __name__ == '__main__':
    main()