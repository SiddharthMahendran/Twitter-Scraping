# Twitter-Scraping

This Python script allows you to scrape Twitter data based on a keyword or hashtag, a start date, an end date, and the number of tweets you want to scrape. The scraped data is stored in a MongoDB database and can also be downloaded as a CSV or JSON file.

Installation:

To run this script, you need to install the following packages:
pandas
snscrape
pymongo
json
base64
streamlit
You can install the required packages using the following command:
pip install -r requirements.txt

Usage:

To run the script, simply execute the Twitter_Scraping.py file in your Python environment.

The script will open a Streamlit app in your browser, where you can enter the search parameters:

* Select the type of data you want to search for (keyword or hashtag) using the dropdown menu.
* Enter the keyword or hashtag you want to search for in the text box.
* Select the start and end dates using the date picker.
* Use the slider to select the number of tweets you want to scrape.
* Once you have entered your search parameters, click the "Upload to MongoDB" button to upload the scraped data to a MongoDB database. You can also download the    scraped data as a CSV or JSON file using the corresponding download buttons.

Functionality:

The script uses the snscrape library to scrape Twitter data. The scraped data is stored in a pandas DataFrame and then uploaded to a MongoDB database using the PyMongo library.
The Streamlit library is used to create a simple user interface for the script. The user interface allows the user to enter the search parameters and view the scraped data.

Contributing:

Contributions are welcome! If you have any suggestions or improvements, feel free to create an issue or submit a pull request.

License:

This project is created using the coding standards: https://www.python.org/dev/peps/pep-0008/.
