from bs4 import BeautifulSoup
import requests
import pymongo
import datetime

def get_events(url):
    # Make a GET request to the URL.
    headers = {'User-Agent': 'Chrome/129.0.6668.70'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error: Failed to get webpage content.")
        return
    
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["quest_db"]
    collection = db["events"]

    # Parse the HTML content.
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all the elements containing event information.
    # You'll need to adjust this selector based on the HTML structure of the webpage.
    event_elements = soup.find_all('article', class_='tribe-events-calendar-list__event')

    # Assuming you have a ResultSet named 'results'
    result_count = 0
    for result in event_elements:
        result_count += 1
    print("Result count:", result_count)

    # Extract event information from each element.
    events = []
    for event_element in event_elements:
        event = {}

        # Extract the title of the event.
        title_element = event_element.find('a', class_='tribe-events-calendar-list__event-title-link tribe-common-anchor-thin')
        if title_element:
            event['title'] = title_element.text.strip()

        # Extract the description of the event (if available).
        description_element = event_element.find('div', class_='tribe-events-calendar-list__event-description tribe-common-b2 tribe-common-a11y-hidden')
        if description_element:
            # Extract the text from the p element inside the div
            event['description'] = description_element.find('p').text

        # Extract the date of the event (if available).
        date_element = event_element.find('span', class_='tribe-event-date-start')
        if date_element:
            event['date'] = date_element.text.strip()

        # Extract the image of the event (if available).
        image_element = event_element.find('img', class_='tribe-events-calendar-list__event-featured-image')
        if image_element:
            event['image'] = image_element['src']

        event['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        events.append(event)
        collection.insert_one(event)

    # Close the connection
    client.close()
    return events



def main():
    # Example usage:
    #url = "https://www.malcolmyards.market/public-events/"
    url = "https://surlybrewing.com/events/"
    #url = "https://gophersports.com/calendar"
    #url = "https://www.varsitytheater.com/shows"
    get_events(url)

if __name__ == "__main__":
    main()
    

