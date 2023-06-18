import googlemaps
import requests
import dotenv
import os
from io import BytesIO
from PIL import Image


dotenv.load_dotenv()
GMAPS_API_KEY = os.environ.get("GMAPS_API_KEY")

gmaps = googlemaps.Client(key=GMAPS_API_KEY)

# print(gmaps.reverse_geocode((37.8719, -122.2585))[0]['address_components'])
# print(gmaps.reverse_geocode((37.8719, -122.2585))[0]['formatted_address'])
geocode_result = gmaps.geocode(address="2580 Bancroft Way")
# print(geocode_result[0]['geometry']['location'])
# print(gmaps.distance_matrix((37.8719, -122.2585), (39, -122.2585), units='metric')['rows'][0]['elements'][0]['distance']['value'])
# exit()

# def get_top5_review(r):
#     sorted_reviews = sorted(r, key=lambda x: x['rating'], reverse=True)
#     # Select the top 5 reviews
#     if len(sorted_reviews < 5):
#         return sorted_reviews
#     else:
#         return  sorted_reviews[:5]

def get_restaurant_recommendations(query, lat_lng):
    try:
        restaurants = gmaps.places(query=query, location=lat_lng, type='restaurant', min_price=1, open_now=True)
        
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
            coordinate = gmaps.geocode(address=address)[0]['geometry']['location']
            distancedic = gmaps.distance_matrix(coordinate, lat_lng, units='metric')
            print(distancedic['rows'][0]['elements'][0])
            distance = 'Unknown'
            if distancedic['rows'][0]['elements'][0]['status'] == 'OK':
                distance = distancedic['rows'][0]['elements'][0]['distance']['text'] #the distance is in km
            
            if rating >= min_rating:
                recommendations.append({'name': name, 'address': address, 'rating': rating, 
                                        'website': website, 'phone number': phone_number, 
                                        'place_id': place_id, 'reviews': reviews[:3], 'photos': photos,
                                        'coordinate': coordinate, 'distance': distance})
        
        return recommendations
    
    except googlemaps.exceptions.ApiError as e:
        print(f"Error occurred: {e}")

# Provide the place, cuisine, and minimum rating for the recommendations
place = 'Berkeley'
cuisine = 'Italian'
min_rating = 4.0
query = "Give me some Italian food"


# def get_location():
#     url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={GMAPS_API_KEY}"
#     response = requests.post(url)

#     if response.status_code == 200:
#         result = response.json()
#         location = result["location"]
#         latitude = location["lat"]
#         longitude = location["lng"]
#         accuracy = result["accuracy"]
#     else:
#         print("Failed to get location")
#     return result

def get_restaurant_reviews(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,rating,reviews&key={GMAPS_API_KEY}"
    response = requests.get(url)

    user_review_texts = []

    if response.status_code == 200:
        result = response.json()
        restaurant_name = result["result"]["name"]
        reviews = result["result"]["reviews"]

        for review in reviews:
            author_name = review["author_name"]
            rating = review["rating"]
            review_text = review["text"]
            user_review_texts.append(review_text)

    return user_review_texts

def get_restaurant_photos(place_id):
    place_details = gmaps.place(place_id=place_id, fields=['photo'])

    photo_urls = []

    if 'result' in place_details:
        result = place_details['result']
        if 'photos' in result:
                photo_references = [photo['photo_reference'] for photo in result['photos']]

                # Use the photo references to retrieve the actual photos
                for reference in photo_references:
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?key={GMAPS_API_KEY}&photoreference={reference}&maxheight=500"
                    photo_urls.append(photo_url)
        else:
            print('No photos found.')
    else:
        print('Place details not found.')

    return photo_urls

def add_to_coordinate(add):
    geocode_result = gmaps.geocode(address=add)
    return geocode_result[0]['geometry']['location'] # a dictionary of lat and lng


lat_lng = (37.8719, -122.2585)
query = "find me some chinese place near campus"
get_restaurant_recommendations(query, lat_lng)