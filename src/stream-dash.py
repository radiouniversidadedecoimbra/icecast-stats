from flask import Flask, jsonify, render_template, request, url_for, redirect
from stream import Stream

app = Flask(__name__)

def countries_dict():
    url = "stream.ruc.pt"
    mount = "/high"

    stream = Stream(url, mount)
    return stream.listeners_locations

@app.route("/countries")
@app.route("/countries.json")
def countries():
    url = "stream.ruc.pt"
    mount = "/high"

    stream = Stream(url, mount)
    lis_loc = stream.listeners_locations

    return jsonify(lis_loc)

@app.route("/")
def index():
    data = countries_dict()
    list_countries = list(data.keys())
    list_listeners = list(data.values())
    print(list_listeners, list_countries)
    print(list_countries[0])
    return render_template("dash.html", data = data) #, ctr = list_countries, lst = list_listeners)

if __name__ == "__main__":
    app.run()