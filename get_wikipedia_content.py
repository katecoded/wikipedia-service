# Katelyn Lindsey
# Wikipedia API Wrapper Service
# get_wikipedia_content.py
# uses https://en.wikipedia.org/w/api.php

import requests, json
from bs4 import BeautifulSoup
from sys import stderr # for debugging

URL = "https://en.wikipedia.org/w/api.php"


def get_relevant_wiki_page(search_term):
	"""
	Returns the most relevent wikipedia page data as a 
	dictionary in the following format:
	{"title": "page title", "pageid": page id}
	"""

	# first, format the query so that only the data of one page is returned
	query = {"action": "query", "format": "json", "list": "search", "srsearch": search_term, "srlimit": 1}

	# request the data
	print("Requesting Page Data:", file=stderr)
	response = requests.get(url=URL, params=query)
	response = response.json()
	print("Done requesting page data", file=stderr)

	# get relevant data in order to get page content later
	page_data = {"title": response["query"]["search"][0]["title"], "pageid": response["query"]["search"][0]["pageid"]}

	return page_data


def get_wiki_text(page_data):
	"""
	Returns the text from the wikipedia page as a dictionary in HTML format.
	"""

	# first, format the query to get just the page HTML content
	query = {"action": "parse", "pageid": page_data["pageid"], "format": "json", "prop": "text"}

	# request the page HTML content
	print("Requesting Page HTML:", file=stderr)
	response = requests.get(url=URL, params=query)
	response = response.json()
	print("Done requesting page HTML", file=stderr)

	return response["parse"]["text"]["*"]


def clean_up_text(page_content):
	"""
	Returns a string of text after stripping HTML fron the
	page content using BeautifulSoup. 
	"""

	# prepare the html to be parsed
	parsed_content = BeautifulSoup(page_content, "html.parser")

	# place where all text will be stored
	complete_text = ""

	# get all of the paragraphs in the content
	paragraphs = parsed_content.find_all("p")

	# store all of the paragraphs
	for paragraph in paragraphs:

		complete_text += paragraph.get_text() + "\n"

	# return the completed text
	print("Page text is as follows\n", complete_text, file=stderr)
	return complete_text


def get_wikipedia_content(search_term):
	"""
	Uses the Wikipedia API to first get pages associated
	with search term. Then, get specific page html content.
	"""

	print("Received search term", search_term, file=stderr)

	# get the data of the most relevant page
	page_data = get_relevant_wiki_page(search_term)

	# get the HTML content of that page
	page_content = get_wiki_text(page_data)

	# get just text content
	text = clean_up_text(page_content)

	# format the JSON that will be returned as the response
	response_content = {"title": page_data["title"], "text_content": text}

	return response_content
