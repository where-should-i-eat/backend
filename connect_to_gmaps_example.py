import googlemaps
import requests


API_KEY = 'AIzaSyApB2EHBitg3ROhOl9gSpeVGbYN47KvlVo'

gmaps = googlemaps.Client(key=API_KEY)


def get_restaurant_recommendations(place, cuisine, min_rating):
    try:
        # Perform a text search to find restaurants matching the given criteria
        query = f"{cuisine} restaurants in {place}"
        restaurants = gmaps.places(query=query, type='restaurant', min_price=1, max_price=4, open_now=True)
        
        recommendations = []
        
        for restaurant in restaurants['results']:
            name = restaurant['name']
            address = restaurant['formatted_address']
            rating = restaurant.get('rating', 0)
            website = restaurant.get('website', 'N/A')
            phone_number = restaurant.get('formatted_phone_number', 'N/A')
            
            if rating >= min_rating:
                recommendations.append({'name': name, 'address': address, 'rating': rating, 
                                        'website': website, 'phone number': phone_number})
        
        return recommendations
    
    except googlemaps.exceptions.ApiError as e:
        print(f"Error occurred: {e}")

# Provide the place, cuisine, and minimum rating for the recommendations
place = 'Berkeley'
cuisine = 'Italian'
min_rating = 4.0

print(get_restaurant_recommendations(place, cuisine, min_rating))
our_recommendation = get_restaurant_recommendations(place, cuisine, min_rating)



import requests

def get_location():
    # Replace "YOUR_API_KEY" with your actual API key

    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={API_KEY}"
    response = requests.post(url)

    if response.status_code == 200:
        result = response.json()
        location = result["location"]
        latitude = location["lat"]
        longitude = location["lng"]
        accuracy = result["accuracy"]
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Accuracy: {accuracy} meters")
    else:
        print("Failed to get location")
    return (location)

print(get_location())
