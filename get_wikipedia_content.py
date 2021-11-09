# Katelyn Lindsey
# Wikipedia API Wrapper Service
# get_wikipedia_content.py
# uses https://en.wikipedia.org/w/api.php

import requests, json
from bs4 import BeautifulSoup
from sys import stderr # for debugging
import unicodedata

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
	# print("Requesting Page Data:", file=stderr)
	response = requests.get(url=URL, params=query)
	response = response.json()
	# print("Done requesting page data", file=stderr)

	# get relevant data in order to get page content later
	page_data = {"title": response["query"]["search"][0]["title"], "pageid": response["query"]["search"][0]["pageid"]}

	return page_data


def get_html(page_data):
	"""
	Returns the html text from the wikipedia page as a dictionary in HTML format.
	"""

	# first, format the query to get just the page HTML content
	query = {"action": "parse", "pageid": page_data["pageid"], "format": "json", "prop": "text"}

	# request the page HTML content
	# print("Requesting Page HTML:", file=stderr)
	response = requests.get(url=URL, params=query)
	response = response.json()
	# print("Done requesting page HTML", file=stderr)

	return response["parse"]["text"]["*"]


def strip_html(page_content):
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

	# store all of the paragraphs as one large string
	for paragraph in paragraphs:

		complete_text += paragraph.get_text() + " "

	# return the completed text
	# print("Page text is as follows\n", complete_text, file=stderr)
	return complete_text


def remove_brackets(text):
	"""
	Takes the complete text of a wikipedia page stripped of HTML and
	returns a new string of that text with extraneous brackets removed.
	"""

	cleaned_text = ""
	in_brackets = False

	# iterate through the given text
	for char in text:

		# if the current char is not a bracket and we are not within brackets,
		# add char to cleaned_text
		if char != "[" and char != "]" and not in_brackets:
			cleaned_text += char

		# else if we are currently in brackets and the current char is a closing
		# bracket, in_brackets is now False
		elif in_brackets and char == "]":
			in_brackets = False

		# else if we are not in brackets and the current char is an opening bracket,
		# in_brackets is now True
		elif not in_brackets and char == "[":
			in_brackets = True

	# return the completed cleaned text
	return cleaned_text


def clean_special_characters(text):
	"""
	Takes the complete content of a wikipedia page without brackets or html,
	and returns that text with special characters cleaned up to display normally.
	"""

	# clean up the text
	cleaned_text = unicodedata.normalize("NFKD", text)

	# return the cleaned text
	return cleaned_text	


def get_wikipedia_content(search_term):
	"""
	Uses the Wikipedia API to first get pages associated
	with search term. Then, get specific page html content.
	"""

	# get the data of the most relevant page
	page_data = get_relevant_wiki_page(search_term)

	# get the HTML content of that page
	page_content = get_html(page_data)

	# get just text content
	text = strip_html(page_content)

	# remove extraneous brackets from text content
	text = remove_brackets(text)

	# clean up special characters
	text = clean_special_characters(text)

	# format the JSON that will be returned as the response
	response_content = {"title": page_data["title"], "text_content": text}

	return response_content
