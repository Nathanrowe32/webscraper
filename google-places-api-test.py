import googlemaps
import time
import mysql.connector
import string
import random
import json

def dict_to_json(dictionary):
  """Converts a Python dictionary to a JSON string.

  Args:
    dictionary: The Python dictionary to convert.

  Returns:
    A JSON string representing the dictionary.
  """

  json_string = json.dumps(dictionary)
  return json_string


def generate_random_string(length):
  """Generates a random string of the specified length.

  Args:
    length: The desired length of the string.

  Returns:
    A random string of the specified length.
  """
  letters = string.ascii_letters
  result_str = ''.join(random.choice(letters) for i in range(length))
  return result_str

def query_google(city, next_page_token=None):
    # Replace with your Google Places API key
    api_key = "HIDDEN"
    # Create a Google Maps client
    gmaps = googlemaps.Client(key=api_key)

    # Geocode the city to get its coordinates
    geocode_result = gmaps.geocode(city)  
    city_lat = geocode_result[0]["geometry"]["location"]["lat"]
    city_lng = geocode_result[0]["geometry"]["location"]["lng"]

    # Perform the Nearby Search
    result = gmaps.places_nearby(
        location=(city_lat, city_lng),
        radius=10000,  # Search radius in meters
        keyword="restaurants",
        type="restaurant",
        page_token=next_page_token  # Optionally specify the type
    )
    return result


def main():

    mydb = mysql.connector.connect(
        host="HIDDEN",
        user="HIDDEN",
        password="HIDDEN",
        database="HIDDEN"
    )
    mycursor = mydb.cursor()

    city = "Minneapolis, MN"

    j = 0
    i = 0
    # Get head of results.
    results = query_google(city)
    for restaurant in results['results']:
        j = j + 1
        print(dict_to_json(restaurant))
        sql = "INSERT INTO Google_Places (id, google_results) VALUES (%s, %s)"
        val = [generate_random_string(15), dict_to_json(restaurant)]
        mycursor.execute(sql, val)



    # While there's a next page token, keep fetching results
    while 'next_page_token' in results:
        i = i + 1
        next_page_token = results['next_page_token']
        time.sleep(5)
        results = query_google(city, next_page_token)
        # Process the results
        for restaurant in results['results']:
            j = j + 1
            sql = "INSERT INTO Google_Places (id, google_results) VALUES (%s, %s)"
            val = [generate_random_string(15), dict_to_json(restaurant)]
            mycursor.execute(sql, val)
        print(results)
        print(i)
        
    print(str(i) + " total loops")
    print(str(j) + " total places found")

    # Close the connection
    mydb.commit()
    mycursor.close()
    mydb.close()

    print("Data inserted successfully!")
        

if __name__ == "__main__":
    main()
    