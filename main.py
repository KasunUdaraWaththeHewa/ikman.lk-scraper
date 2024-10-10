import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()


# Define a model for the response of ads
class Ad(BaseModel):
    title: str
    link: str
    price: str
    location: str


# Define a model for the response of categories
class Category(BaseModel):
    id: int
    slug: str
    name: str


# API endpoint to fetch categories
@app.get('/api/categories', response_model=List[Category])
def get_categories():
    category_api_url = 'https://ikman.lk/data/categories/en'
    category_response = requests.get(category_api_url)

    if category_response.status_code == 200:
        # Parse the response as JSON
        categories = category_response.json()

        # Create a list to store filtered categories
        filtered_categories = []

        for category_id, category_data in categories.items():
            # Extract 'id', 'slug', and 'name' from each category
            filtered_categories.append({
                'id': category_data.get('id'),
                'slug': category_data.get('slug'),
                'name': category_data.get('name')
            })

        return filtered_categories
    else:
        raise HTTPException(status_code=category_response.status_code, detail="Failed to retrieve categories")

# API endpoint to scrape advertisements based on the selected category_ID
@app.post('/api/scrape_ads', response_model=List[Ad])
def scrape_ads(category_slug: str):
    # Construct the base URL using the provided category slug
    base_url = f'https://ikman.lk/en/ads/sri-lanka/{category_slug}?sort=date&order=desc&buy_now=0&urgent=0&page='
    print(base_url)

    page_number = 1
    ads_list = []

    # Loop until there are no more ads to scrape
    while True:
        url = f'{base_url}{page_number}'
        response = requests.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to retrieve the webpage")

        soup = BeautifulSoup(response.content, 'html.parser')
        ad_containers = soup.find_all('li', class_=['top-ads-container--1Jeoq', 'normal--2QYVk'])

        if not ad_containers:
            break  # Exit loop if no more ads

        for ad in ad_containers:
            title_tag = ad.find('h2', class_='heading--2eONR')
            link_tag = ad.find('a', class_='card-link--3ssYv')
            price_tag = ad.find('div', class_='price--3SnqI')
            location_tag = ad.find('div', class_='description--2-ez3')

            if not (title_tag and link_tag and price_tag and location_tag):
                continue  # Skip ads with missing data

            title = title_tag.text.strip()
            link = link_tag['href']
            price = price_tag.text.strip()
            location = location_tag.text.strip()

            ads_list.append(Ad(
                title=title,
                link=f'https://ikman.lk{link}',
                price=price,
                location=location
            ))

        page_number += 1

    return ads_list


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
