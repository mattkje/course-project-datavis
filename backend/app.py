from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    return jsonify(df.to_dict(orient="records"))

@app.route("/country/<country>")
def country(country):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    df = df[df["country"] == country]
    return jsonify(df.to_dict(orient="records"))

@app.route("/year/<year>")
def year(year):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    df = df[df["year"] == int(year)]
    return jsonify(df.to_dict(orient="records"))

@app.route("/country_year/<country>/<year>")
def country_year(country, year):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    df = df[(df["country"] == country) & (df["year"] == int(year))]
    return jsonify(df.to_dict(orient="records"))

@app.route("/country_year_range/<country>/<start_year>/<end_year>")
def country_year_range(country, start_year, end_year):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    df = df[(df["country"] == country) & (df["year"] >= int(start_year)) & (df["year"] <= int(end_year))]
    return jsonify(df.to_dict(orient="records"))

@app.route("/country_code/<country_code>")
def country_code(country_code):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    df = df[df["iso_code"] == country_code]
    return jsonify(df.to_dict(orient="records"))

@app.route("/country_code_latest/<country_code>")
def country_code_latest(country_code):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    df = df[df["iso_code"] == country_code]
    df = df[df["year"] == df["year"].max()]
    return jsonify(df.to_dict(orient="records"))