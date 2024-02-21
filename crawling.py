import requests
import json

def get_restaurants(api_key, latitude, longitude, radius=16093):  # 10 miles in meters
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius,
        "categories": "restaurants",
        "limit": 50  # Max limit allowed by Yelp API per request
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_reviews(api_key, business_id):
    url = f"https://api.yelp.com/v3/businesses/{business_id}/reviews"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def save_to_file(new_data, filename="restaurants.json"):
    try:
        with open(filename, 'r') as file:
            # Load existing data
            existing_data = json.load(file)
            existing_ids = {restaurant["id"] for restaurant in existing_data.get("businesses", [])}
    except FileNotFoundError:
        existing_data = {"businesses": []}
        existing_ids = set()

    # Add only new restaurants
    new_businesses = [business for business in new_data.get("businesses", []) if business["id"] not in existing_ids]
    existing_data["businesses"].extend(new_businesses)

    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=4)

    return len(new_businesses)

# Example usage:
api_key = "mDHUtSTqVEujrNgU0Nl4aaXKjmhG_Nm0yWvGTS5p8QKEDGZzdTmcsyi2zK-D1yhXxglIIDawSjXJwkJrFbp1qFkS2ZH-6hfnOxvBNQSGO_FgVWxC2DF9VphDoTDVZXYx"
latitude = 29.684831299427866   # Example latitude, replace with your location
longitude = -95.48195064082688  # Example longitude, replace with your location
restaurants = get_restaurants(api_key, latitude, longitude)
if restaurants:
    save_to_file(restaurants)
    print(f"Saved {len(restaurants.get('businesses', []))} restaurants to restaurants.json")