# Twitter-Scraping

This project provides a Python-based web application (Graphical User Interface) to search and scrape tweets from Twitter, based on specific keywords or hashtags, and within a date range. The scraped data can be saved to a MongoDB database or downloaded as CSV or JSON files.

Getting started

Prerequisites:

Before running the application, you need to have the following installed:
Python 3
pip
streamlit
pymongo
snscrape

Installation:

You can install the required packages using the following command:
pip install -r requirements.txt

Usage:

You can run the application locally by running the following command in your terminal:
streamlit run app.py
This will start a Streamlit server that you can access on your web browser at http://localhost:8501.
Once you access the application, you can select the type of data you want to search (keyword or hashtag), enter the keyword/hashtag, select the date range, and choose how many tweets to scrape. You can then upload the scraped data to a MongoDB database or download it as a CSV or JSON file.

Contributing:

Contributions are welcome! If you have any suggestions or improvements, feel free to create an issue or submit a pull request.

License:

This project is created using the coding standards: https://www.python.org/dev/peps/pep-0008/.
