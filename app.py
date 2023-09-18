from flask import Flask, render_template, request, Markup
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def get_title_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.text.strip()
        else:
            return "No title available"
    except requests.exceptions.RequestException as e:
        return str(e)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            # Split the user input into individual URLs
            urls = re.findall(r"https?://[^\s/$.?#].[^\s]*", user_input)
            links = []
            for url in urls:
                title = get_title_from_url(url)
                # Convert each URL into an internal link with title
                link = f'<a href="{url}" rel="nofollow" title="{title}">{title}</a>'
                links.append(link)

            internal_links = "<br>".join(links)  # Separate links by newline for display
            return render_template("index.html", internal_links=Markup(internal_links))

    return render_template("index.html", internal_links=None)

if __name__ == "__main__":
    app.run(debug=True)
