# Katelyn Lindsey
# Wikipedia API Wrapper Service
# app.py
# wraps the existing Wikipedia API: https://www.mediawiki.org/wiki/API:Main_page

from flask import Flask, render_template, jsonify, request
import json
from get_wikipedia_content import get_wikipedia_content

# define app
app = Flask(__name__)


# main route
@app.route("/", methods=["GET"])
def wikipedia_content():

	req = request.get_json()
	search_term = req["search_term"]

	# get content from most relevant Wikipedia page
	wiki_content = get_wikipedia_content(search_term)

	# return that Wikipedia content
	return jsonify(wiki_content)


if __name__ == "__main__":
	app.run()
