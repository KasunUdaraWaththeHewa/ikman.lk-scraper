import requests
from bs4 import BeautifulSoup

# Step 1: Fetch categories from the API
category_api_url = 'https://ikman.lk/data/categories/en'
category_response = requests.get(category_api_url)

# Check if the category request was successful
if category_response.status_code == 200:
    categories = category_response.json()  # Parse JSON response
else:
    print(f"Failed to retrieve categories. Status code: {category_response.status_code}")
    categories = {}

# Display available categories
print("Available Categories:")
for category_id, category_info in categories.items():
    print(f"{category_id}: {category_info['name']}")

# Select a category ID dynamically (you can modify this part based on your needs)
selected_category_id = input("Enter the category ID you want to scrape (e.g., '391' for Vehicles): ")

# Step 2: Construct the base URL using the selected category ID
base_url = f'https://ikman.lk/en/ads/sri-lanka/{categories[selected_category_id]["slug"]}?sort=date&order=desc&buy_now=0&urgent=0&page='

# Initialize a page number variable
page_number = 1

# Step 3: Loop until there are no more ads to scrape
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
