"""
election_scraper.py: Third project for the Engeto Python Academy
author: Arnošt Razima
email: razima.ar@seznam.cz
discord: Arnošt R. #3251
"""
import csv
import requests
import sys
from bs4 import BeautifulSoup

def main():
    """Main function to initiate data scraping and saving to CSV."""
    base_url = "https://volby.cz/pls/ps2017nss/"
    check_arguments()
    url = sys.argv[1]
    output_filename = sys.argv[2]
    first_soup = get_response(url)
    city_name = get_city_name(first_soup)
    vysledky, header = get_municipality_links(first_soup, base_url, city_name)
    file_name = f"vysledky_{output_filename}.csv"
    print(f"Saving data to file: {file_name}")
    save_to_csv(vysledky, header, file_name)
    print("All done, closing...")

def check_arguments():
    """Check if the correct number of command-line arguments was provided."""
    if len(sys.argv) != 3:
        print("Arguments were not entered correctly. Usage: python election_scraper.py <URL> <output_filename>")
        exit()
    else:
        print(f"Downloading data from URL: {sys.argv[1]}")
    return

def get_response(url):
    """Send an HTTP GET request and return a BeautifulSoup object for parsing."""
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def get_city_name(first_soup):
    """Extract and return the city name from the BeautifulSoup object."""
    city_name_element = first_soup.find('h3', class_='bar3')
    if city_name_element:
        return city_name_element.text.strip().split(" - ")[1]
    else:
        return "Unknown City"

def get_municipality_links(first_soup, base_url, city_name):
    """Extract municipality links and data from the first BeautifulSoup object."""
    results = []
    header = []
    each_region = 0

    names = first_soup.find_all('td', {'class': 'overflow_name'})
    for each_td in first_soup.find_all('td', {'class': 'cislo'}):
        line = [each_td.text]
        for each_name in names[each_region]:
            line.append(each_name.text)
        link = each_td.a['href']
        if each_region == 0:
            header = create_header(get_response(base_url + link))
            line.extend(collect_numbers(get_response(base_url + link)))
        else:
            line.extend(collect_numbers(get_response(base_url + link)))
        results.append(line)
        each_region += 1

    if results:
        results[0][1] = f"Výsledky pro město {city_name}"
    else:
        results.append([f"Výsledky pro město {city_name}"])

    return results, header



# Function to extract numerical data
def collect_numbers(second_soup):
    data = []

    registered = second_soup.find('td', {'headers': 'sa2'}).text
    data.append(clean_numbers(registered))
    envelopes = second_soup.find('td', {'headers': 'sa5'}).text
    data.append(clean_numbers(envelopes))
    valid = second_soup.find('td', {'headers': 'sa6'}).text
    data.append(clean_numbers(valid))

    data.extend(collect_votes(second_soup))

    return data


# Function to create CSV header
def create_header(second_soup):
    header = ["Code", "Location", "Registered", "Envelopes", "Valid"]
    for party_name in second_soup.find_all('td', {'class': 'overflow_name'}):
        header.append(party_name.text)

    return header


# Function to extract data about party votes
def collect_votes(second_soup):
    data_votes = []
    number = 1
    table_count = len(second_soup.find_all('table'))

    while number < table_count:
        votes = second_soup.find_all('td', {'headers': f't{number}sa2 t{number}sb3'})
        for each in votes:
            data_votes.append(clean_numbers(each.text))
        number += 1

    return data_votes


# Function to clean numbers and remove unwanted characters
def clean_numbers(number):
    if "\xa0" in number:
        return ''.join(number.split())
    else:
        return number


def save_to_csv(vysledky: list, header: list, file: str):
    """Save data to a CSV file with the specified name."""
    with open(file, "w", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, dialect="excel")
        csv_writer.writerow(header)
        csv_writer.writerows(vysledky)
        
# Main entry point of the script
if __name__ == "__main__":
    main()