'''Link Verification

Write a program that, given the URL of a web page, will attempt to download every linked page on the page. The program should flag any pages that have a 404 “Not Found” status code and print them out as broken links.'''

# Module imports
import requests, bs4, traceback, os, sys, time
from urllib.parse import urlparse, urlunparse
from pathlib import Path

# Saves error file alongside script
os.chdir(Path(sys.argv[0]).parent)

# Parses url and downloads HTML
url = input('Enter a URL: ')
res = requests.get(url)
res.raise_for_status()
url = urlparse(res.url)
soup = bs4.BeautifulSoup(res.text, 'html.parser')

# Iterates through pages anchor tags
for tag in soup('a'):
    # Creates link from non relative url
    parsed_tag = urlparse(tag['href'])
    if parsed_tag.scheme != '':
        crawl_link = urlunparse(parsed_tag)
    
    # Creates link from relative url
    else:
        # Adds relative location details to host site
        crawl_link = url._replace(
            path=parsed_tag.path,
            params=parsed_tag.params,
            query=parsed_tag.query,
            fragment=parsed_tag.fragment
    )
        crawl_link = urlunparse(crawl_link)
    
    print(f'Downloading link: {crawl_link}...')

    # Checks for HTML errors
    try:
        res = requests.get(crawl_link)
        if res.status_code != requests.codes.ok:
            print(f'Invalid link! Error code: {res.status_code}\n')
        else:
            print(f'Valid link!\n')

    # Exception for non-HTML errors written to a file
    except:
        print(f'Invalid link!\n')
        with open(f'error_info.txt', 'a') as fhandle:
            header = f'Invalid URL: {crawl_link}'
            fhandle.write(header + '\n')
            fhandle.write('*' * len(header))
            fhandle.write('\n' + traceback.format_exc() + '\n')

    # Prevents HTML error 429: Too many requests
    time.sleep(0.75)