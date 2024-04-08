import requests

# Your Azure Maps subscription key
subscription_key = 'q6E90CxFS1bb3-MfR4m0rEnV7HD7cuSLd9TZGi75O64'

# Base URL for the Azure Maps Static Map service
base_url = "https://atlas.microsoft.com/map/static/png"

# Get the address from the user
address = input("Enter the address: ")

# Geocoding API endpoint
geocoding_url = "https://atlas.microsoft.com/search/address/json"

# Geocoding API parameters
geocoding_params = {
    "api-version": "1.0",
    "subscription-key": subscription_key,
    "query": address,
    "limit": 1
}

# Make a GET request to the Geocoding API
geocoding_response = requests.get(geocoding_url, params=geocoding_params)
geocoding_data = geocoding_response.json()

# Extract the coordinates from the Geocoding API response
if geocoding_data["results"]:
    latitude = geocoding_data["results"][0]["position"]["lat"]
    longitude = geocoding_data["results"][0]["position"]["lon"]
    center = f"{longitude},{latitude}"
else:
    print("Unable to find the coordinates for the given address.")
    exit()

# Parameters for the map
params = {
    'api-version': '1.0',
    'subscription-key': subscription_key,
    'layer': 'basic',
    'style': 'main',
    'zoom': '16',
    'center': center,
    'width': '500',
    'height': '1000'
}

# Make a GET request to the Azure Maps Static Map service
response = requests.get(base_url, params=params)

# The URL to the static map image
map_image_url = response.url

print(map_image_url)