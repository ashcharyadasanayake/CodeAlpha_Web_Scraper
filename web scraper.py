# Import modules
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import datetime

# Define the URL and the headers
url = "https://ieeexplore.ieee.org/document/6978614"
headers = {"User-Agent": "Mozilla/5.0"}

# Try to send the request and get the response
try:
    response = requests.get(url, headers=headers)
    # Check the status code
    if response.status_code == 200:
        # Create a BeautifulSoup object from the response content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the article elements
        articles = soup.find_all("div", class_="card border-0 mb-3")

        # Use the with statement to open and close the CSV file automatically
        with open("w3schools_python_articles.csv", "w", newline="") as csv_file:
            # Create a CSV writer object
            csv_writer = csv.writer(csv_file)

            # Write the header row
            csv_writer.writerow(["Title", "Link", "Description", "Author", "Date"])

            # Loop through the article elements
            for article in articles:
                # Find the title and link elements
                title = article.find("h2", class_="card-title").text.strip()
                link = article.find("a", class_="card-link")["href"]

                # Use the urljoin function to construct the absolute URL from the relative link
                link = urljoin(url, link)

                # Find the description element
                description = article.find("p", class_="card-text").text.strip()

                # Find the author element
                author = article.find("div", class_="card-footer").text.strip()

                # Split the author element by a comma to get only the name
                author = author.split(",")[0]

                # Parse the author element into a datetime object using the strptime function
                date = datetime.datetime.strptime(author, "%b %d, %Y")

                # Get only the date part of the datetime object using the date method
                date = date.date()

                # Write the data to the CSV file
                csv_writer.writerow([title, link, description, author, date])

            # Close the CSV file
            csv_file.close()
    else:
        # Print an error message
        print(f"Request failed with status code {response.status_code}")
except Exception as e:
    # Print the exception message
    print(f"An error occurred: {e}")