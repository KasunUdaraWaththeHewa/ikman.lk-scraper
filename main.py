import requests
from bs4 import BeautifulSoup

# Base URL of the page you want to scrape
base_url = 'https://ikman.lk/en/ads/sri-lanka/cars?sort=date&order=desc&buy_now=0&urgent=0&page='

# Initialize a page number variable
page_number = 1

# Loop until there are no more ads to scrape
while True:
    # Create the complete URL for the current page
    url = f'{base_url}{page_number}'

    # Send a GET request to fetch the raw HTML content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the advertisement containers (li elements)
        ad_containers = soup.find_all('li', class_=['top-ads-container--1Jeoq', 'normal--2QYVk'])

        # If there are no ads, break the loop
        if not ad_containers:
            break

        # Loop through each ad container and extract the details
        for ad in ad_containers:
            # Get the title of the car
            title = ad.find('h2', class_='heading--2eONR')
            if title:
                title = title.text.strip()
            else:
                continue  # Skip if title not found

            # Get the URL of the car ad
            link = ad.find('a', class_='card-link--3ssYv')['href']

            # Get the price of the car
            price = ad.find('div', class_='price--3SnqI')
            if price:
                price = price.text.strip()
            else:
                continue  # Skip if price not found

            # Get the location of the car
            location = ad.find('div', class_='description--2-ez3')
            if location:
                location = location.text.strip()
            else:
                continue  # Skip if location not found

            # Print the extracted details
            print(f'Title: {title}')
            print(f'Link: https://ikman.lk{link}')
            print(f'Price: {price}')
            print(f'Location: {location}')
            print('-' * 50)

        # Increment the page number for the next iteration
        page_number += 1
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        break
