import requests
import datetime
import os
import csv

x = datetime.datetime.now()
this_year = x.year - 1

country_code = ''

def get_country_population(country_code, year):
    # Your World Bank Open Data API key
    api_key = "YOUR_API_KEY"

    # Prepare the URL
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/SP.POP.TOTL?format=json"

    # Send a GET request to the API with the API key and desired year
    response = requests.get(url, params={"api_key": api_key, "date": year})

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the population value
        population = data[1][0]['value']

        return year, population

        # # Print the population information
        # print(f"Country Code: {country_code}")
        # print(f"Year: {year}")
        # print(f"Population: {population}")
    else:
        return None

# Get the population of a specific country (e.g., "USA" for United States) for a specific year (e.g., 2021)

def write_csv():
    init_year = 1980
    data_list = []

    if get_country_population(country_code, init_year) is None:
        print("Cannot retrieve the data for the following country.")
    else:
        while init_year < this_year:
            year, population = get_country_population("NP", init_year)
            data_list.append([year, population])
            init_year += 1
    
    file_path = 'data_stream.csv'
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['Year', 'Population'])
        writer.writerows(data_list)

write_csv()


# print(get_country_population("NP", 2000))
