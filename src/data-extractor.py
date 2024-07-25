import requests
from bs4 import BeautifulSoup
import os

def remove_empty_lines(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Filter out empty lines
        non_empty_lines = [line for line in lines if line.strip()]

        with open(filename, 'w', encoding='utf-8') as file:
            file.writelines(non_empty_lines)
        
        print(f"Empty lines removed from {filename}")

    except Exception as e:
        print(f"Error processing the file: {e}")

def fetch_page_content(url):
    try:
        # Set custom headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Fetch the web page
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def parse_links(content, base_url):
    soup = BeautifulSoup(content, 'html.parser')
    links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('http'):
            links.append(href)
        else:
            links.append(base_url + href)
    return links

def save_content(filename, content):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Content saved to {filename}")
        remove_empty_lines(filename)
    except Exception as e:
        print(f"Error saving the file: {e}")

def crawl_and_save(url, filename_prefix):
    content = fetch_page_content(url)
    if content:
        main_filename = f"{filename_prefix}_main.txt"
        save_content(main_filename, content)

        links = parse_links(content, url)
        for i, link in enumerate(links):
            link_content = fetch_page_content(link)
            if link_content:
                link_filename = f"{filename_prefix}_link_{i+1}.txt"
                save_content(link_filename, link_content)

if __name__ == "__main__":
    url = "https://darksouls.fandom.com/pt-br/wiki/Wiki_Dark_Souls"
    filename_prefix = "site_content"
    crawl_and_save(url, filename_prefix)
