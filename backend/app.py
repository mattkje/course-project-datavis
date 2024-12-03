from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

from calculations import predict_arima, calculate_democracy_rank

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def filter_world_data():
    df = pd.read_csv("datasets/world-data-2023.csv")
    filtered_columns = df[["country", "Abbreviation", "Land Area(Km2)", "Capital/Major City", "Largest city", "Population"]]
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
    country_list = country.split(",")
    result_df = init_global_data()
    result_df = result_df[result_df["country"].isin(country_list)]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))


@app.route("/countries")
def countries():
    result_df = filter_world_data()
    countries_list = result_df["country"].unique().tolist()
    return jsonify(countries_list)

@app.route("/country_data/<country>")
def country_data(country):
    country_list = country.split(",")
    result_df = filter_world_data()
    result_df = result_df[result_df["country"].isin(country_list)]
    result_df.fillna("N/A", inplace=True)
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/year/<year>")
def year(year):
    merged_df = init_global_data()
    result_df = merged_df[merged_df["year"] == int(year)]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_year/<country>/<year>")
def country_year(country, year):
    country_list = country.split(",")
    merged_df = init_global_data()
    result_df = merged_df[(merged_df["country"].isin(country_list)) & (merged_df["year"] == int(year))]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_year_range/<country>/<start_year>/<end_year>")
def country_year_range(country, start_year, end_year):
    country_list = country.split(",")
    merged_df = init_global_data()
    result_df = merged_df[(merged_df["country"].isin(country_list)) & (merged_df["year"] >= int(start_year)) & (merged_df["year"] <= int(end_year))]
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
    country_list = country.split(",")
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    result_df = df[df["country"].isin(country_list)]
    result_df = result_df[["year", "energy_per_capita", "country"]]
    result_df.fillna("N/A", inplace=True)
    result_dict = dict(zip(result_df["year"], result_df["energy_per_capita"]))
    return jsonify(result_dict)

@app.route("/co2-growth-abs/<country>")
def co2_growth_abs(country):
    country_list = country.split(",")
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    result_df = df[df["country"].isin(country_list)]
    result_df = result_df[["year", "co2_growth_abs", "country"]]
    result_df.fillna("N/A", inplace=True)
    result_dict = dict(zip(result_df["year"], result_df["co2_growth_abs"]))
    return jsonify(result_dict)

@app.route("/co2_growth_prct/<country>")
def co2_growth_percentage(country):
    country_list = country.split(",")
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    result_df = df[df["country"].isin(country_list)]
    result_df = result_df[["year", "co2_growth_prct", "country"]]
    result_df.fillna(0, inplace=True)
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/share-global/<country>", defaults={'start_year': 1829, 'end_year': 2022})
@app.route("/co2-per-capita/<country>/<int:start_year>/<int:end_year>")
def co2_per_capita(country, start_year, end_year):
    country_list = country.split(",")
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    result_df = df[df["country"].isin(country_list)]
    result_df = result_df[["year", "co2_per_capita", "country"]]
    result_df.fillna("N/A", inplace=True)
    result_dict = dict(zip(result_df["year"], result_df["co2_per_capita"]))
    return jsonify(result_dict)

@app.route("/per_capita/<country>", defaults={'start_year': 1829, 'end_year': 2022})
@app.route("/per_capita/<country>/<int:start_year>/<int:end_year>")
def per_capita(country, start_year, end_year):
    country_list = country.split(",")
    merged_df = init_global_data()
    result_df = merged_df[merged_df["country"].isin(country_list)]
    result_df = result_df[(result_df["year"] >= start_year) & (result_df["year"] <= end_year)]
    per_capita_columns = [
        col for col in result_df.columns
        if "per_capita" in col
           and "energy" not in col
    ]

    per_capita_columns.append('year')
    per_capita_columns.append('country')

    per_capita_data_df = result_df[per_capita_columns].copy()
    per_capita_data_df.fillna(0, inplace=True)
    return jsonify(per_capita_data_df.to_dict(orient="records"))

@app.route("/temperature/<country>", defaults={'start_year': 1829, 'end_year': 2022})
@app.route("/temperature/<country>/<int:start_year>/<int:end_year>")
def temperature(country, start_year, end_year):
    country_list = country.split(",")
    merged_df = init_global_data()
    result_df = merged_df[merged_df["country"].isin(country_list)]
    result_df = result_df[(result_df["year"] >= start_year) & (result_df["year"] <= end_year)]
    temperature_columns = [
        col for col in result_df.columns
        if "temperature" in col and "share" not in col
    ]

    temperature_columns.append('year')
    temperature_columns.append('country')

    temperature_data_df = result_df[temperature_columns].copy()
    temperature_data_df.fillna(0, inplace=True)
    return jsonify(temperature_data_df.to_dict(orient="records"))


@app.route("/cumulative/<country>", defaults={'start_year': 1829, 'end_year': 2022})
@app.route("/cumulative/<country>/<int:start_year>/<int:end_year>")
def cumulative(country, start_year, end_year):
    country_list = country.split(",")
    merged_df = init_global_data()
    result_df = merged_df[merged_df["country"].isin(country_list)]
    result_df = result_df[(result_df["year"] >= start_year) & (result_df["year"] <= end_year)]
    cumulative_columns = [
        col for col in result_df.columns
        if "cumulative" in col and "share" not in col
    ]

    cumulative_columns.append('year')
    cumulative_columns.append('country')

    cumulative_data_df = result_df[cumulative_columns].copy()
    cumulative_data_df.fillna(0, inplace=True)
    return jsonify(cumulative_data_df.to_dict(orient="records"))

@app.route("/share-global/<country>", defaults={'start_year': 1829, 'end_year': 2022})
@app.route("/share-global/<country>/<int:start_year>/<int:end_year>")
def share_global(country, start_year, end_year):
    country_list = country.split(",")
    merged_df = init_global_data()
    result_df = merged_df[merged_df["country"].isin(country_list)]
    result_df = result_df[(result_df["year"] >= start_year) & (result_df["year"] <= end_year)]
    share_columns = [
        col for col in result_df.columns
        if "share_global" in col
    ]

    share_columns.append('year')
    share_columns.append('country')

    share_data_df = result_df[share_columns].copy()
    share_data_df.fillna(0, inplace=True)
    return jsonify(share_data_df.to_dict(orient="records"))

@app.route("/ghg/<country>", defaults={'start_year': 1829, 'end_year': 2022})
@app.route("/ghg/<country>/<int:start_year>/<int:end_year>")
def ghg_per_capita(country, start_year, end_year):
    country_list = country.split(",")
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    result_df = df[df["country"].isin(country_list)]
    result_df = result_df[(result_df["year"] >= start_year) & (result_df["year"] <= end_year)]

    ghg_columns = [
        col for col in result_df.columns
        if "ghg" in col
    ]

    ghg_columns.append('year')
    ghg_columns.append('country')

    ghg_data_df = result_df[ghg_columns].copy()
    ghg_data_df.fillna(0, inplace=True)

    return jsonify(ghg_data_df.to_dict(orient="records"))

@app.route("/gdp/<country>", defaults={'start_year': 1829, 'end_year': 2022})
@app.route("/gdp/<country>/<int:start_year>/<int:end_year>")
def country_gdp(country, start_year, end_year):
    country_list = country.split(",")
    # Merge datasets on 'country'
    merged_df = init_global_data()

    # Filter rows by country
    result_df = merged_df[merged_df["country"].isin(country_list)]
    result_df = result_df[(result_df["year"] >= start_year) & (result_df["year"] <= end_year)]

    # Select columns that include "gdp", plus 'year'
    gdp_columns = [
        col for col in result_df.columns
        if "_gdp" in col
    ]

    gdp_columns.append('year')
    gdp_columns.append('country')

    # Filter the DataFrame to only include selected GDP columns and 'year'
    gdp_data_df = result_df[gdp_columns].copy()

    # Replace NaN values with 0
    gdp_data_df.fillna(0, inplace=True)

    # Convert the filtered DataFrame to JSON format
    return jsonify(gdp_data_df.to_dict(orient="records"))

@app.route("/co2/<country>", defaults={'start_year': 1829, 'end_year': 2022})
@app.route("/co2/<country>/<int:start_year>/<int:end_year>")
def country_co2(country, start_year, end_year):
    country_list = country.split(",")
    merged_df = init_global_data()

    # Filter rows by country
    result_df = merged_df[merged_df["country"].isin(country_list)]
    result_df = result_df[(result_df["year"] >= start_year) & (result_df["year"] <= end_year)]

    # List of terms to exclude from CO2-related fields
    exclude_terms = ["per_capita", "per_gdp", "per_unit_energy", "share", "cumulative", "growth","temperature"]

    # Select CO2 columns, excluding specific variants, plus 'year'
    co2_columns = [
        col for col in result_df.columns
        if "co2" in col and not any(term in col for term in exclude_terms)
    ]
    co2_columns.append('year')
    co2_columns.append('country')

    # Filter the DataFrame to only include selected CO2 columns and 'year'
    co2_data_df = result_df[co2_columns].copy()

    # Replace NaN values with 0
    co2_data_df.fillna(0, inplace=True)

    # Convert the filtered DataFrame to JSON format
    return jsonify(co2_data_df.to_dict(orient="records"))

@app.route("/predict/<country>/<prediction_data>")
def predict(country, prediction_data):
    return predict_arima(country, prediction_data)

import csv

def load_country_to_continent():
    country_to_continent = {}
    with open('datasets/countryToContinent.csv', mode='r') as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip the header row
        for rows in reader:
            country_to_continent[rows[0]] = rows[1]
    return country_to_continent

@app.route("/gdp_co2")
def gdp_co2():
    merged_df = init_global_data()

    # Select the necessary columns
    result_df = merged_df[["year", "country", "gdp", "co2"]].copy()
    result_df.loc[:, :] = result_df.fillna(0)  # Replace NaN values with 0

    # Load country to continent mapping
    country_to_continent = load_country_to_continent()

    # Format the data as required
    data = {}
    for year in result_df["year"].unique():
        year_data = result_df[result_df["year"] == year]
        data[int(year)] = [
            {
                "x": row["co2"],
                "y": row["gdp"],
                "name": row["country"],
                "continent": country_to_continent.get(row["country"], "Unknown")
            }
            for _, row in year_data.iterrows()
        ]

    return jsonify(data)


@app.route("/additional-data/<country>")
def additional_data(country):
    df1 = pd.read_csv("datasets/democracy-index-eiu.csv")
    df1 = df1[df1["year"] == 2023]
    df2 = pd.read_csv("datasets/happiest-countries-in-the-world-2024.csv")
    df2["country"] = df2["country"].str.replace('"', '')
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[merged_df["country"] == country]
    result_df = result_df[["country", "HappinessRank2023", "HappinessScore2023", "DemocracyScore"]]
    result_df.fillna("N/A", inplace=True)

    try:
        democracy_rank = calculate_democracy_rank(country)
        result_df["DemocracyRank"] = democracy_rank
    except ValueError as e:
        result_df["DemocracyRank"] = str(e)

    return jsonify(result_df.to_dict(orient="records"))