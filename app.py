from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('gsextract.html')


@app.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    results = search_google_scholar(query)
    return jsonify(results)


def search_google_scholar(query):
    search_url = f"https://scholar.google.com/scholar?q={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    papers = []

    for item in soup.select('[data-lid]'):
        title = item.select_one('.gs_rt').text
        authors_and_date = item.select_one('.gs_a').text

        parts = authors_and_date.split('-')

        if len(parts) == 3:
            authors = parts[0].strip()
            pub_and_date = parts[1].split(',')
            publication = pub_and_date[0].strip()
            date = pub_and_date[1].strip() if len(pub_and_date) > 1 else "Unknown"
            journal = parts[2].strip()

        else:
            authors = authors_and_date
            publication = "Unknown"
            date = "Unknown"
            journal = "Unknown"

        # Further split authors from publication

        papers.append({
            'title': title,
            'authors': authors,
            'publication': publication,
            'date': date,
            'journal': journal,
        })

    return papers


if __name__ == '__main__':
    app.run(debug=True)
