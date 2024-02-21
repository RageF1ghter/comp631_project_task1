import json
import requests

# Function to get reviews for a given business ID
def get_reviews(api_key, business_id):
    url = f"https://api.yelp.com/v3/businesses/{business_id}/reviews"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to read existing data from the file
def read_existing_data(filename="restaurants.json"):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"businesses": []}

# Function to save updated data (including reviews) to the file
def save_to_file(data, filename="reviews.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# API Key - replace "YOUR_API_KEY" with your actual Yelp API key
api_key = "mDHUtSTqVEujrNgU0Nl4aaXKjmhG_Nm0yWvGTS5p8QKEDGZzdTmcsyi2zK-D1yhXxglIIDawSjXJwkJrFbp1qFkS2ZH-6hfnOxvBNQSGO_FgVWxC2DF9VphDoTDVZXYx"

# Read existing restaurant data
existing_data = read_existing_data()
existing_ids = [restaurant["id"] for restaurant in existing_data.get("businesses", [])]

# Fetch reviews for each restaurant and append them to the restaurant data
for restaurant in existing_data["businesses"]:
    if restaurant["id"] in existing_ids:
        review_data = get_reviews(api_key, restaurant["id"])
        if review_data:
            restaurant["reviews"] = review_data.get("reviews", [])

# Save the updated restaurant data, including reviews, back to the file
save_to_file(existing_data)
