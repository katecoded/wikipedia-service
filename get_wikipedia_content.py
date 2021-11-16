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
	response = requests.get(url=URL, params=query)
	response = response.json()

	# get relevant data of most relevant page in order to get page content later
	page_data = {"title": response["query"]["search"][0]["title"], "pageid": response["query"]["search"][0]["pageid"]}

	return page_data


def get_html(page_data):
	"""
	Returns the HTML text from the wikipedia page as a dictionary in HTML format.
	"""

	# first, format the query to get just the page HTML content
	query = {"action": "parse", "pageid": page_data["pageid"], "format": "json", "prop": "text"}

	# request the page HTML content
	response = requests.get(url=URL, params=query)
	response = response.json()

	return response["parse"]["text"]["*"]


def strip_html(page_content):
	"""
	Returns an array of paragraphs after stripping HTML fron the
	page content using BeautifulSoup. 
	"""

	# prepare the html to be parsed
	parsed_content = BeautifulSoup(page_content, "html.parser")

	# get all of the paragraphs in the content
	paragraphs = parsed_content.find_all("p")

	# create list to store complete text in
	complete_text = []

	# store all of the paragraphs in a list
	for paragraph in paragraphs:

		text = paragraph.get_text()

		if text != "" and text != "\n":
			complete_text.append(text)

	# return the completed text
	return complete_text


def remove_brackets(text):
	"""
	Takes a string of text from a wikipedia page stripped of HTML and
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


def fix_special_characters(text):
	"""
	Takes a string of text from a wikipedia page without brackets or HTML,
	and returns that text with special characters fixed to display normally.
	"""

	# clean up the text
	cleaned_text = unicodedata.normalize("NFKD", text)

	# return the cleaned text
	return cleaned_text	


def clean_text(text_array):
	"""
	Takes an array of strings and cleans it up by removing brackets
	and ensuring special characters display properly.
	"""

	# loop through the array of strings, cleaning up each string one by one
	for index in range(len(text_array)):

		# remove extraneous brackets
		text_array[index] = remove_brackets(text_array[index])

		# clean up special characters
		text_array[index] = fix_special_characters(text_array[index])


def get_wikipedia_content(search_term):
	"""
	Uses the Wikipedia API to first get pages associated
	with search term. Then, get specific page HTML content,
	get the paragraphs from that content, and format that
	as JSON to return.
	"""

	# get the data of the most relevant page
	page_data = get_relevant_wiki_page(search_term)

	# get all of the HTML content of that page
	page_content = get_html(page_data)

	# strip the HTML to get an array of paragraph strings
	paragraph_array = strip_html(page_content)

	# clean up the array of strings (remove brackets and fix special characters)
	clean_text(paragraph_array)

	# format the JSON that will be returned as the response
	response_content = {"title": page_data["title"], "text_content": paragraph_array}

	return response_content
