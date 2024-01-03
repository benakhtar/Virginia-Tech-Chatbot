'''
Hi there, I am a custom built web scrapper for a CS 5624 project! Happy scraping!

References:
https://github.com/ashleychampagne/Web-Scraping-Toolkit/blob/master/V2-Getting%20Started%20with%20Beautiful%20Soup.md
'''
import csv
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup


# empty list of urls to scrape
urls = []

# empty list of already scraped urls
scraped = []

# Open csv containing list of URLS to scrape
with open('websites.csv', 'r') as file:

    # Read csv
    reader = csv.reader(file)

    # Headers:
    # URL, Sraped? (Boolean, 1 true else false)
    header = next(reader)

    for lines in reader:

        # If line not blank
        if len(lines) > 0:
            
            # If URL has not been scraped yet, will only have url entry 
            # Check that URL has not been scraped yet and add to list to be scraped
            # else add to list of already scraped URLs
            if len(lines) == 1 and lines not in scraped:
                urls.append(lines[0])
            else:
                scraped.append(lines[0])

file.close()

# empty list of valid urls to add to list to be scraped
valid = []

# For every URL, scrape and add results to approprite csv
for url in urls:

    # Try URL
    try:
            # Download page
        homepage = requests.get(url)
                
        # Create Beautiful Soup object
        homepage_soup = BeautifulSoup(homepage.content, features = "html.parser")


        with open("corpus.csv", 'a',  encoding="utf-8") as file:
            # Scrape text
            texts = homepage_soup.find_all('p')
            for text in texts:
                file.write(text.getText())
        file.close()
                
        # Create a list of urls linked to from the homepage
        links = homepage_soup.find_all('a')

        # Add each link to input csv 
        for link in links:
            newURL = link.get('href')

            # If link has not already been scraped and is valid, add to list to be added to input csv
            if newURL is not None and newURL[0:4] == "http" and newURL not in scraped:
                valid.append(newURL)

        # Add url to list of urls scraped
        scraped.append(url)

    # except URL broken, invalid, etc so do nothing
    except Exception as e:
        print("FAIL: Link is broken")
        


# Open input file of websites to scrape:
with open('websites.csv', 'w') as file:

    # Overwrite existing urls in scraped to include indicator that it has already been scraped
    for s in scraped:
        file.write(s + ",1\n")

    # Append all additional links scraped from urls
    for v in valid:
        file.write(v + '\n')

file.close()

    








