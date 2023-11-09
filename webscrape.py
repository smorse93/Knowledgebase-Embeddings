import requests
from bs4 import BeautifulSoup
import csv
import time

# Define the base URL of the forum section
section_url = 'https://forum.dealerrefresh.com/forums/crm-ilm-chat-desking-emails-phone-sms.5/'

# Function to scrape a single page of the forum section
def scrape_section_page(url):
    threads = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # You would need to identify the correct class/tags for thread links
    for thread in soup.find_all('a', class_='thread-link-class'):
        thread_title = thread.text
        thread_url = thread['href']
        threads.append({'Title': thread_title, 'URL': thread_url})
    return threads

# Function to scrape comments from a single thread
def scrape_thread_comments(thread_url):
    comments = []
    response = requests.get(thread_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # You would need to identify the correct class/tags for comments
    for comment in soup.find_all('div', class_='message-class'):
        user = comment.find('a', class_='username-class').text
        timestamp = comment.find('time', class_='datetime-class')['datetime']
        comment_text = comment.find('article', class_='message-body-class').text
        comments.append({'User': user, 'Timestamp': timestamp, 'Comment': comment_text})
    return comments

# Function to iterate over all threads in the section
def scrape_forum_section(section_url):
    all_comments = []
    threads = scrape_section_page(section_url)
    for thread in threads:
        thread_comments = scrape_thread_comments(thread['URL'])
        all_comments.extend(thread_comments)
        time.sleep(1)  # Respectful delay between requests
    print(all_comments)
    return all_comments

# Scrape the forum section and save to CSV
print('running')

comments_data = scrape_forum_section(section_url)
if comments_data:
    keys = comments_data[0].keys()
    with open('dealerrefresh_comments.csv', 'w', newline='',  encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(comments_data)
