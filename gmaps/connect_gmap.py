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
# geocode_result = gmaps.geocode(address="2580 Bancroft Way")
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
        
        recommendations = {}
        
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
            # print(distancedic['rows'][0]['elements'][0])
            distance = 'Unknown'
            if distancedic['rows'][0]['elements'][0]['status'] == 'OK':
                distance = distancedic['rows'][0]['elements'][0]['distance']['text'] #the distance is in km
            
            if rating >= min_rating:
                recommendations[place_id] = {'name': name, 'address': address, 'rating': rating, 
                                        'website': website, 'phone number': phone_number, 
                                        'place_id': place_id, 'reviews': reviews[:3], 'photos': photos,
                                        'coordinate': coordinate, 'distance': distance}
        
        return recommendations
    
    except googlemaps.exceptions.ApiError as e:
        print(f"Error occurred: {e}")

# Provide the place, cuisine, and minimum rating for the recommendations
# place = 'Berkeley'
# cuisine = 'Italian'
min_rating = 4.0
# query = "Give me some Italian food"


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

def coord_to_name(coord):
    lat, lng = coord['lat'], coord['lng']
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GMAPS_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        if len(data['results']) > 0:
            result = data['results'][0]
            print(result.keys())
            return result['name']
    return None

def get_name_from_address(address):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GMAPS_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        if len(data['results']) > 0:
            result = data['results'][0]
            
            print(result['address_components'])
            for component in result['address_components']:
                if 'restaurant' in component['types']:
                    return component['long_name']
            return None
    return None


def get_establishment_name(coord):
    latitude, longitude = coord
    gmaps = googlemaps.Client(key=GMAPS_API_KEY)
    reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
    
    for result in reverse_geocode_result:
        for component in result['address_components']:
            if 'establishment' in component['types']:
                return component['long_name']
    return None  # No establishment found

def get_restaurant_name(address):
    gmaps = googlemaps.Client(key=GMAPS_API_KEY)
    geocode_result = gmaps.geocode(address)
    
    if geocode_result:
        first_result = geocode_result[0]
        for component in first_result['address_components']:
            if 'restaurant' in component['types']:
                return first_result['name']
    
    return None  # No restaurant found

def get_name(coord):
    lat, lng = coord['lat'], coord['lng']
    url1 = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GMAPS_API_KEY}'
    response1 = requests.get(url1)
    data1 = response1.json()
    placeid = data1['results'][0]['place_id']
    url2 = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={placeid}&key={GMAPS_API_KEY}'
    response2 = requests.get(url2)
    data2 = response2.json()
    if data2['status'] == 'OK':
        if 'result' in data2 and 'name' in data2['result']:
            return data2['result']['name']
    return None



# lat_lng = (37.8719, -122.2585)
# query = "find me some chinese place near campus"
# get_restaurant_recommendations(query, lat_lng)