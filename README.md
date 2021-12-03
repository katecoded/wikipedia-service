# Wikipedia Service

This Python application, made using Flask, takes a search term and returns text from the most relevant Wikipedia page as a list separated by paragraph. It acts as a wrapper around the [existing MediaWiki Action API](https://www.mediawiki.org/wiki/API:Main_page).

Here is an example of how it could be used with Python and requests if it were running locally:

```
import requests

response = requests.get("http://127.0.0.1:5000", json={"search_term":"corgi"})

# response is in the format {"text_content": ["paragraph 1", ...], "title": "page title"}
response.json()
```

This application was created as part of a portfolio project for CS 361: Software Engineering I.