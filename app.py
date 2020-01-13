from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

import scrape_mars

app=Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)

scrape_result=mongo.db.scrape_result

@app.route("/scrape")
def scraper():
    mars_data=scrape_mars.scrape()
    # scrape_result.insert_many(mars_data)
    scrape_result.update({}, mars_data, upsert=True)
    return redirect("/")

@app.route("/")
def index():
    mars_data=scrape_result.find_one()
    return render_template("index.html",mars_data =mars_data)


if __name__ == "__main__":
    app.run(debug=True)
