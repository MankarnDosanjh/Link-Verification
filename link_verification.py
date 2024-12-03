'''Link Verification

Write a program that, given the URL of a web page, will attempt to download every linked page on the page. The program should flag any pages that have a 404 “Not Found” status code and print them out as broken links.'''

# NOTE: If the HTTP code is ok despite an error appearing, that error may be something else (e.g. an SSL error)

# Module imports
import requests, bs4

# Downloads page
host = input('Enter a valid website whose links you wish to check: ')
res = requests.get(host)
res.raise_for_status()

# Creates soup object
soup = bs4.BeautifulSoup(res.text, 'html.parser')

# Iterates through anchor tags
for tag in soup('a'):

    # Extracts url
    if tag['href'].startswith('https://'):
        url = tag['href']

    # Creates proper url if url is relative to host
    else:
        url = host + tag['href']

    print(f'Downloading {url}')

    # Error checking for page download
    try:
        res = requests.get(url)
        res.raise_for_status()
        print('LINK STATUS: GOOD\n')

    except:
        print(f'LINK STATUS: BAD')
        print(f'HTTP ERROR CODE: {res.status_code}\n')