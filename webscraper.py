from bs4 import BeautifulSoup
import requests
import datetime
import requests
import mysql.connector
import random
import string

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

def get_events(url, mydb):
    # Make a GET request to the URL.
    headers = {'User-Agent': 'Chrome/129.0.6668.70'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error: Failed to get webpage content.")
        return
    
    mycursor = mydb.cursor()

    # Parse the HTML content.
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all the elements containing event information.
    # You'll need to adjust this selector based on the HTML structure of the webpage.
    event_elements = soup.find_all('article', class_='tribe-events-calendar-list__event')

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

        sql = "INSERT INTO Minneapolis_Events (id, title, description, date, image, timestamp) VALUES (%s, %s, %s, %s, %s, %s)"
        val = [generate_random_string(15), event['title'], event['description'], event['date'], event['image'],
            event['timestamp']]
        mycursor.execute(sql, val)

    # Close the connection
    mydb.commit()
    mycursor.close()
    mydb.close()
    print("Event data successfully scraped and commited to database!")

def get_gopher_sports(url, mydb):
    # Make a GET request to the URL.
    headers = {'User-Agent': 'Chrome/129.0.6668.70'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error: Failed to get webpage content.")
        return
    mycursor = mydb.cursor()

    soup = BeautifulSoup(response.content, 'html.parser')

    games_element = soup.find_all('div', class_='s-game-card__header border-theme-border-light w-full overflow-hidden border rounded-[10px]')
    games = []
    for game_element in games_element:
        game_data = {}

        game_data['id'] = generate_random_string(15)
        sport_element = soup.find('h2', class_='s-common__header-title !s-text-heading-large text-theme-safe-light border-theme-brand-light !m-0 border-l-4 border-solid px-4 pl-[20px]')
        if sport_element:
            game_data['sport'] = sport_element.text

        opponent_element = game_element.find('a', class_='text-theme-safe s-text-paragraph-bold block')
        if opponent_element:
            game_data['opponent'] = opponent_element.text.strip()

        location_element = game_element.find('p', class_='text-theme-muted s-text-paragraph-small flex items-center justify-start')
        if location_element:
            game_data['location'] = location_element.find_all('span')[1].text

        date_element = game_element.find('div', class_='whitespace-nowrap')
        if date_element:
            game_data['date'] = date_element.find_all('span')[0].text
        elif (date_element == None):
            game_data['date'] = game_element.find('p', class_='text-theme-safe s-text-paragraph-bold flex').text

        time_element = game_element.find('span', class_='s-text-paragraph-small text-theme-muted flex items-center whitespace-nowrap')
        if time_element:
            game_data['time'] = time_element.text.strip()

        image_element = game_element.find('img', class_='object-contain h-[60px] w-[60px]')
        if image_element:
            game_data['image'] = image_element['src']
        
        game_data['url'] = url

        game_data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        games.append(game_data)

        sql = "INSERT INTO Sports_Scraper (id, sport, opponent, location, date, time, image, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = [game_data['id'], game_data['sport'], game_data['opponent'], game_data['location'], game_data['date'],
            game_data['time'], game_data['image'], game_data['url']]
        mycursor.execute(sql, val)

    # Close the connection
    mydb.commit()
    mycursor.close()
    mydb.close()
    print("Gopher data successfully scraped and commited to database!")

def scrape_jina_ai(url):
  response = requests.get("https://r.jina.ai/" + url)
  return response.text

def main():
    # Create a new client and connect to the server
    mydb = mysql.connector.connect(
        host="HIDDEN",
        user="HIDDEN",
        password="HIDDEN",
        database="HIDDEN"
    )
    # event_urls = [
    #     "https://www.malcolmyards.market/public-events/", 
    #     "https://surlybrewing.com/events/"
    # ]


    # game_urls = [
    #     "https://gophersports.com/sports/football/schedule", 
    #     "https://gophersports.com/sports/mens-ice-hockey/schedule"
    # ]
    
    # for event_url in event_urls:
    #     get_events(event_url, mydb)

    # for game_url in game_urls:
    #     get_gopher_sports(game_url, mydb)

    # url = "https://www.thecedar.org/"
    # get_cedar_events(url)

    # url = "https://www.ticketmaster.com/discover/concerts/minneapolis"
    # print(scrape_jina_ai(url))

if __name__ == "__main__":
    main()
    

