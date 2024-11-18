from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def filter_world_data():
    df = pd.read_csv("datasets/world-data-2023.csv")
    filtered_columns = df[["country", "Abbreviation", "Land Area(Km2)", "Capital/Major City", "Largest city"]]
    return filtered_columns

def init_global_data():
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = filter_world_data()
    return pd.merge(df1, df2, on="country")

@app.route("/")
def home():
    return "Welcome to Group 5's API! :)"

@app.route("/country/<country>")
def country(country):
    result_df = init_global_data()
    result_df = result_df[result_df["country"] == country]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/year/<year>")
def year(year):
    merged_df = init_global_data()
    result_df = merged_df[merged_df["year"] == int(year)]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_year/<country>/<year>")
def country_year(country, year):
    merged_df = init_global_data()
    result_df = merged_df[(merged_df["country"] == country) & (merged_df["year"] == int(year))]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_year_range/<country>/<start_year>/<end_year>")
def country_year_range(country, start_year, end_year):
    merged_df = init_global_data()
    result_df = merged_df[(merged_df["country"] == country) & (merged_df["year"] >= int(start_year)) & (merged_df["year"] <= int(end_year))]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_code/<country_code>")
def country_code(country_code):
    merged_df = init_global_data()
    result_df = merged_df[merged_df["iso_code"] == country_code]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_code_latest/<country_code>")
def country_code_latest(country_code):
    merged_df = init_global_data()
    result_df = merged_df[merged_df["iso_code"] == country_code]
    result_df = result_df[result_df["year"] == result_df["year"].max()]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/energy-per-capita/<country>")
def energy_per_capita(country):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    result_df = df[df["country"] == country]
    result_df = result_df[["year", "energy_per_capita"]]
    result_df.fillna("N/A", inplace=True)
    result_dict = dict(zip(result_df["year"], result_df["energy_per_capita"]))
    return jsonify(result_dict)

@app.route("/co2-growth-abs/<country>")
def co2_growth_abs(country):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    result_df = df[df["country"] == country]
    result_df = result_df[["year", "co2_growth_abs"]]
    result_df.fillna("N/A", inplace=True)
    result_dict = dict(zip(result_df["year"], result_df["co2_growth_abs"]))
    return jsonify(result_dict)

@app.route("/co2-growth-%/<country>")
def co2_growth_percentage(country):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    result_df = df[df["country"] == country]
    result_df = result_df[["year", "co2_growth_prct"]]
    result_df.fillna(0, inplace=True)
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/co2-per-capita/<country>")
def co2_per_capita(country):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    result_df = df[df["country"] == country]
    result_df = result_df[["year", "co2_per_capita"]]
    result_df.fillna("N/A", inplace=True)
    result_dict = dict(zip(result_df["year"], result_df["co2_per_capita"]))
    return jsonify(result_dict)

@app.route("/per-capita/<country>")
def per_capita(country):
    merged_df = init_global_data()
    result_df = merged_df[merged_df["country"] == country]
    per_capita_columns = [
        col for col in result_df.columns
        if "per_capita" in col
    ]

    if 'year' in result_df.columns:
        per_capita_columns.append('year')

    per_capita_data_df = result_df[per_capita_columns].copy()
    per_capita_data_df.fillna(0, inplace=True)
    return jsonify(per_capita_data_df.to_dict(orient="records"))

@app.route("/cumulative/<country>")
def cumulative(country):
    merged_df = init_global_data()
    result_df = merged_df[merged_df["country"] == country]
    cumulative_columns = [
        col for col in result_df.columns
        if "cumulative" in col and "share" not in col
    ]

    if 'year' in result_df.columns:
        cumulative_columns.append('year')

    cumulative_data_df = result_df[cumulative_columns].copy()
    cumulative_data_df.fillna(0, inplace=True)
    return jsonify(cumulative_data_df.to_dict(orient="records"))

@app.route("/share-global/<country>")
def share_global(country):
    merged_df = init_global_data()
    result_df = merged_df[merged_df["country"] == country]
    share_columns = [
        col for col in result_df.columns
        if "share_global" in col
    ]

    if 'year' in result_df.columns:
        share_columns.append('year')

    share_data_df = result_df[share_columns].copy()
    share_data_df.fillna(0, inplace=True)
    return jsonify(share_data_df.to_dict(orient="records"))

@app.route("/ghg/<country>")
def ghg_per_capita(country):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    result_df = df[df["country"] == country]

    ghg_columns = [
        col for col in result_df.columns
        if "ghg" in col
    ]

    if 'year' in result_df.columns:
        ghg_columns.append('year')

    ghg_data_df = result_df[ghg_columns].copy()
    ghg_data_df.fillna(0, inplace=True)

    return jsonify(ghg_data_df.to_dict(orient="records"))

@app.route("/gdp/<country>")
def country_gdp(country):
    # Merge datasets on 'country'
    merged_df = init_global_data()

    # Filter rows by country
    result_df = merged_df[merged_df["country"] == country]

    # Select columns that include "gdp", plus 'year'
    gdp_columns = [
        col for col in result_df.columns
        if "_gdp" in col
    ]

    # Ensure 'year' is included
    if 'year' in result_df.columns:
        gdp_columns.append('year')

    # Filter the DataFrame to only include selected GDP columns and 'year'
    gdp_data_df = result_df[gdp_columns].copy()

    # Replace NaN values with 0
    gdp_data_df.fillna(0, inplace=True)

    # Convert the filtered DataFrame to JSON format
    return jsonify(gdp_data_df.to_dict(orient="records"))

@app.route("/co2/<country>")
def country_co2(country):
    merged_df = init_global_data()

    # Filter rows by country
    result_df = merged_df[merged_df["country"] == country]

    # List of terms to exclude from CO2-related fields
    exclude_terms = ["per_capita", "per_gdp", "per_unit_energy", "share", "cumulative", "growth","temperature"]

    # Select CO2 columns, excluding specific variants, plus 'year'
    co2_columns = [
        col for col in result_df.columns
        if "co2" in col and not any(term in col for term in exclude_terms)
    ]

    # Ensure 'year' is included
    if 'year' in result_df.columns:
        co2_columns.append('year')

    # Filter the DataFrame to only include selected CO2 columns and 'year'
    co2_data_df = result_df[co2_columns].copy()

    # Replace NaN values with 0
    co2_data_df.fillna(0, inplace=True)

    # Convert the filtered DataFrame to JSON format
    return jsonify(co2_data_df.to_dict(orient="records"))