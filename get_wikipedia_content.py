# Katelyn Lindsey
# Wikipedia API Wrapper Service
# get_wikipedia_content.py

import requests, json
from bs4 import BeautifulSoup
from sys import stderr # for debugging
import unicodedata

URL = "https://en.wikipedia.org/w/api.php"


def get_relevant_wiki_page(search_term):
	"""
	Returns the most relevent Wikipedia page data (without text content)
	as a dictionary in the following format:
	{"title": "page title", "pageid": page id}
	"""

	# format the query to get only the data for the most relevant page
	query = {"action": "query", "format": "json", "list": "search", "srsearch": search_term, "srlimit": 1}

	response = requests.get(url=URL, params=query)
	response = response.json()

	# only need title and pageid - used for getting page content later
	page_data = {"title": response["query"]["search"][0]["title"], "pageid": response["query"]["search"][0]["pageid"]}

	return page_data


def get_html(page_data):
	"""
	Returns the HTML text from the Wikipedia page as a dictionary in HTML format.
	"""

	# format the query to get just the page HTML content
	query = {"action": "parse", "pageid": page_data["pageid"], "format": "json", "prop": "text"}

	response = requests.get(url=URL, params=query)
	response = response.json()

	return response["parse"]["text"]["*"]


def strip_html(page_content):
	"""
	Returns an array of paragraphs after stripping HTML from the
	page content using BeautifulSoup. 
	"""

	# prepare the HTML to be parsed
	parsed_content = BeautifulSoup(page_content, "html.parser")

	# get all of the paragraphs in the content
	paragraphs = parsed_content.find_all("p")

	complete_text = []
	# store all of the paragraphs in a list
	for paragraph in paragraphs:

		text = paragraph.get_text()

		# only add non-empty paragraphs
		if text != "" and text != "\n":
			complete_text.append(text)

	return complete_text


def remove_brackets(text):
	"""
	Takes a string of text from a Wikipedia page stripped of HTML and
	returns a new string of that text with extraneous brackets removed.
	"""

	cleaned_text = ""
	in_brackets = False

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

	return cleaned_text


def fix_special_characters(text):
	"""
	Takes a string of text from a Wikipedia page without brackets or HTML,
	and returns that text with special characters fixed to display normally.
	"""

	cleaned_text = unicodedata.normalize("NFKD", text)

	return cleaned_text	


def clean_text(text_array):
	"""
	Takes an array of strings and cleans it up by removing brackets
	and ensuring special characters display properly.
	"""

	for index in range(len(text_array)):

		text_array[index] = remove_brackets(text_array[index])
		text_array[index] = fix_special_characters(text_array[index])


def get_wikipedia_content(search_term):
	"""
	Uses the Wikipedia API to first get the most relevant 
	Wikipedia page and its HTML content based on the given
	search term. Then, the text content is cleaned up and 
	separated by paragraph.
	Returns a dictionary with the title and list of paragraphs
	in the following format:
	{"title": "page title", "text_content": ["paragraph 1", ...]}
	"""

	# get the content of the most relevant Wikipedia page
	page_data = get_relevant_wiki_page(search_term)
	page_content = get_html(page_data)

	# get the text from the HTML content and clean it up
	paragraph_array = strip_html(page_content)
	clean_text(paragraph_array)

	response_content = {"title": page_data["title"], "text_content": paragraph_array}

	return response_content
