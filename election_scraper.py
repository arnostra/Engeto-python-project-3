"""
election_scraper.py: Third project for the Engeto Python Academy
author: Arnošt Razima
email: razima.ar@seznam.cz
discord: Arnošt R. #3251
"""

# Import necessary libraries
import csv
import requests
import sys
from bs4 import BeautifulSoup

# Define the main function
def main():
    """
    Main function to execute the scraping and saving process.
    """
    # Set the base URL for the website and check the command-line arguments
    base_url = "https://volby.cz/pls/ps2017nss/"
    check_arguments()
    url = sys.argv[1]
    output_filename = sys.argv[2]
    first_soup = get_response(url)
    city_name = get_city_name(first_soup)
    results, header = get_municipality_links(first_soup, base_url)
    file_name = f"{output_filename}.csv" 
    print(f"Saving data to file: {file_name}")
    save_to_csv(results, header, file_name)
    print("All done, closing...")

# Function to check command-line arguments
def check_arguments():
    """
    Check if the correct number of command-line arguments was provided.
    """
    if len(sys.argv) != 3:
        print("Arguments were not entered correctly. Usage: python election_scraper.py <URL> <output_filename>")
        exit()
    else:
        print(f"Downloading data from URL: {sys.argv[1]}")
    return

# Function to get website response and create BeautifulSoup object
def get_response(url):
    """
    Get the response from the provided URL.
    """
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

# Function to extract the city name
def get_city_name(first_soup):
    """
    Extract the city name from the BeautifulSoup object.
    """
    city_name_element = first_soup.find('h3', class_='bar3')
    if city_name_element:
        return city_name_element.text.strip().split(" - ")[1]
    else:
        return "Unknown_City"

# Function to extract municipality links and data
def get_municipality_links(first_soup, base_url):
    """
    Extract municipality links and data.
    """
    results = []
    header = []

    city_name = get_city_name(first_soup) 
    names = first_soup.find_all('td', {'class': 'overflow_name'})
    for each_td in first_soup.find_all('td', {'class': 'cislo'}):
        # ...
     results[0][1] = f"Results for {city_name}"  
    header = create_header(get_response(base_url + results[0][0] + ".htm"), city_name)  
    return results, header

# Function to create the CSV header
def create_header(second_soup, city_name):
    """
    Create the CSV header.
    """
    header = ["Code", f"Location - {city_name}", "Registered", "Envelopes", "Valid"]
    # ...

# Function to save data to a CSV file
def save_to_csv(results: list, header: list, file: str):
    """
    Save data to a CSV file.
    """
    with open(file, "w", encoding="utf-8", newline="") as csv_s:
        write = csv.writer(csv_s, dialect="excel")
        write.writerow(header)
        write.writerows(results)

if __name__ == "__main__":
    main()
