from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# import our Mars scraping library
import scrape_mars_2

# Create an instance of our Flask app.
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#homepage
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# set route/scrape
@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars_2.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)
    # return render_template("index.html", mars=mars)
   

if __name__ == "__main__":
    app.run(debug=True)

