import googlemaps
import requests
import dotenv
import os
from io import BytesIO
from PIL import Image


dotenv.load_dotenv()
GMAPS_API_KEY = os.environ.get("GMAPS_API_KEY")

gmaps = googlemaps.Client(key=GMAPS_API_KEY)


def get_restaurant_recommendations(query):
    try:
        restaurants = gmaps.places(query=query, type='restaurant', min_price=1, max_price=4, open_now=True)
        
        recommendations = []
        
        for restaurant in restaurants['results']:
            name = restaurant['name']
            address = restaurant['formatted_address']
            rating = restaurant.get('rating', 0)
            website = restaurant.get('website', 'N/A')
            phone_number = restaurant.get('formatted_phone_number', 'N/A')
            place_id = restaurant['place_id']
            reviews = get_restaurant_reviews(place_id)
            photos = get_restaurant_photos(place_id) # a list of url's
            
            if rating >= min_rating:
                recommendations.append({'name': name, 'address': address, 'rating': rating, 
                                        'website': website, 'phone number': phone_number, 
                                        'place_id': place_id, 'reviews': reviews, 'photos': photos})
        
        return recommendations
    
    except googlemaps.exceptions.ApiError as e:
        print(f"Error occurred: {e}")

# Provide the place, cuisine, and minimum rating for the recommendations
place = 'Berkeley'
cuisine = 'Italian'
min_rating = 4.0
query = "Give me some Italian food"


def get_location():
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={GMAPS_API_KEY}"
    response = requests.post(url)

    if response.status_code == 200:
        result = response.json()
        location = result["location"]
        latitude = location["lat"]
        longitude = location["lng"]
        accuracy = result["accuracy"]
    else:
        print("Failed to get location")
    return result

def get_restaurant_reviews(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,rating,reviews&key={GMAPS_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        result = response.json()
        restaurant_name = result["result"]["name"]
        reviews = result["result"]["reviews"]

        for review in reviews:
            author_name = review["author_name"]
            rating = review["rating"]
            review_text = review["text"]
    else:
        print("Failed to fetch reviews")

def get_restaurant_photos(place_id):
    place_details = gmaps.place(place_id=place_id, fields=['photo'])

    if 'result' in place_details:
        result = place_details['result']
        if 'photos' in result:
                photo_references = [photo['photo_reference'] for photo in result['photos']]

                photo_urls = []
                
                # Use the photo references to retrieve the actual photos
                for reference in photo_references:
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?key={GMAPS_API_KEY}&photoreference={reference}&maxheight=500"
                    photo_urls.append(photo_url)
        else:
            print('No photos found.')
    else:
        print('Place details not found.')

    return photo_urls

get_restaurant_recommendations(query)