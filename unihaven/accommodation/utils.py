# accommodation/utils.py

import math
import requests

def calculate_distance(point1, point2):
    """
    Calculate distance between two points using equirectangular approximation.
    point1 and point2 are (latitude, longitude) tuples in degrees.
    Returns distance in kilometers.
    """
    R = 6371  # Earth radius in kilometers
    
    # Convert to radians
    lat1 = math.radians(point1[0])
    lon1 = math.radians(point1[1])
    lat2 = math.radians(point2[0])
    lon2 = math.radians(point2[1])
    
    # Calculate the mean latitude for x calculation
    lat_mean = (lat1 + lat2) / 2
    
    # Calculate x and y differences
    x = (lon2 - lon1) * math.cos(lat_mean)
    y = lat2 - lat1
    
    # Calculate distance
    distance = math.sqrt(x*x + y*y) * R
    
    return distance

def get_address_info(building_name):
    url = "https://www.als.gov.hk/lookup"
    params = {
        "q": building_name,
        "n": 1,
        "output": "json"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        # Extract latitude, longitude and GeoAddress from response
        # This will depend on the exact structure of their API response
        return {
            'latitude': data['AddressLookupResult'][0]['Latitude'],
            'longitude': data['AddressLookupResult'][0]['Longitude'],
            'geo_address': data['AddressLookupResult'][0]['GeoAddress']
        }
    else:
        # Handle error
        return None

# HKU campus locations - hardcoded for simplicity
CAMPUS_LOCATIONS = {
    'main': (22.283, 114.137),  # Main campus
    'medical': (22.270, 114.131),  # Medical campus
    'cyberport': (22.261, 114.131),  # Cyberport campus
    # Add other campuses as needed
}

def get_campus_coordinates(campus_name):
    """Get coordinates for a named HKU campus."""
    return CAMPUS_LOCATIONS.get(campus_name.lower())
