#!/usr/bin/python3 -B

from engineserver import indexdata, cleanup
from flask import Flask, render_template, request, flash, redirect, send_from_directory, url_for

cleanup.cleanup_database()

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

url_database = indexdata.SearchDatabase()
desc_database = indexdata.DescriptionDatabase()

url_database.load_db()
desc_database.load_db()

url_database.search("wikipedia")

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == "POST":
        query = request.form["query"]
        results = url_database.search(query)
        data = {}
        data_pros = desc_database.fetch_contents()



        for current_page in results[0]:
            print(current_page)
            print(data_pros[current_page])
            data[current_page] =  data_pros[current_page]

        return render_template("search.html", results=results, length=len(results), data=data)

    return render_template("index.html")

app.run(host='0.0.0.0', port=8080)