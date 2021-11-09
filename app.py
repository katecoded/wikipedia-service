# Katelyn Lindsey
# Wikipedia API Wrapper Service
# app.py
# uses https://en.wikipedia.org/w/api.php

# Requests in Python are to be sent as follows:
# response = requests.get("http://127.0.0.1:5000", json={"search_term":"dandelion"})
# response.json()

from flask import Flask, render_template, jsonify, request
import json
from get_wikipedia_content import get_wikipedia_content

# define app
app = Flask(__name__)


# main and only route
@app.route("/", methods=["GET"])
def wikipedia_content():

	# get JSON data of request
	req = request.get_json()

	# get search term from request
	search_term = req["search_term"]

	# next, get formatted wikipedia content
	wiki_content = get_wikipedia_content(search_term)

	# return that wikipedia content
	return jsonify(wiki_content)


if __name__ == "__main__":
	app.run()
