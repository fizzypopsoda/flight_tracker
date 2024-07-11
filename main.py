import requests

def searchFlights():
    # Collect user inputs
    sourceAirportCode = input("Enter sourceAirportCode (e.g., BOS): ")
    destinationAirportCode = input("Enter destinationAirportCode (e.g., JFK): ")
    date = input("Enter travel date (YYYY-MM-DD): ")
    returnDate = input("Enter return date (YYYY-MM-DD): ")
    itineraryType = input("Enter itineraryType (ONE_WAY or ROUND_TRIP): ")
    sortOrder = input("Enter sortOrder (e.g., PRICE): ")
    numAdults = input("Enter number of adults (e.g., 1): ")
    numSeniors = input("Enter number of seniors (e.g., 0): ")
    classOfService = input("Enter class of service (e.g., ECONOMY): ")

    url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchFlights"

    querystring = {
        "sourceAirportCode": sourceAirportCode,
        "destinationAirportCode": destinationAirportCode,
        "date": date,
        "returnDate": returnDate,
        "itineraryType": itineraryType,
        "sortOrder": sortOrder,
        "numAdults": numAdults,
        "numSeniors": numSeniors,
        "classOfService": classOfService,
    }

    headers = {
        "x-rapidapi-key": "bba200fd56mshe960f0b2d77da71p110687jsnd7a81dfd6206",
        "x-rapidapi-host": "tripadvisor16.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    # Check if the response is successful
    if response.status_code == 200:
        json_data = response.json()
        flights = json_data['data']['flights']
        
        # Print flight details
        for flight in flights:
            print(flight)
    else:
        print("Error:", response.status_code, response.text)

if __name__ == "__main__":
    searchFlights()
