from heapq import merge

from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    return jsonify(df.to_dict(orient="records"))

@app.route("/country/<country>")
def country(country):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = pd.read_csv("datasets/world-data-2023.csv")
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[merged_df["country"] == country]
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/year/<year>")
def year(year):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = pd.read_csv("datasets/world-data-2023.csv")
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[merged_df["year"] == int(year)]
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_year/<country>/<year>")
def country_year(country, year):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = pd.read_csv("datasets/world-data-2023.csv")
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[(merged_df["country"] == country) & (merged_df["year"] == int(year))]
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_year_range/<country>/<start_year>/<end_year>")
def country_year_range(country, start_year, end_year):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = pd.read_csv("datasets/world-data-2023.csv")
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[(merged_df["country"] == country) & (merged_df["year"] >= int(start_year)) & (merged_df["year"] <= int(end_year))]
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_code/<country_code>")
def country_code(country_code):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = pd.read_csv("datasets/world-data-2023.csv")
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[merged_df["iso_code"] == country_code]
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_code_latest/<country_code>")
def country_code_latest(country_code):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = pd.read_csv("datasets/world-data-2023.csv")
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[merged_df["iso_code"] == country_code]
    result_df = result_df[result_df["year"] == result_df["year"].max()]
    return jsonify(result_df.to_dict(orient="records"))