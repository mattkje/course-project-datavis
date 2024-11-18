from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def filter_world_data():
    df = pd.read_csv("datasets/world-data-2023.csv")
    filtered_columns = df[["country", "Abbreviation", "Land Area(Km2)", "Capital/Major City", "Largest city"]]
    return filtered_columns

@app.route("/")
def home():
    return "Welcome to Group 5's API! :)"

@app.route("/country/<country>")
def country(country):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = filter_world_data()
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[merged_df["country"] == country]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/year/<year>")
def year(year):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = filter_world_data()
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[merged_df["year"] == int(year)]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_year/<country>/<year>")
def country_year(country, year):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = filter_world_data()
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[(merged_df["country"] == country) & (merged_df["year"] == int(year))]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_year_range/<country>/<start_year>/<end_year>")
def country_year_range(country, start_year, end_year):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = filter_world_data()
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[(merged_df["country"] == country) & (merged_df["year"] >= int(start_year)) & (merged_df["year"] <= int(end_year))]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_code/<country_code>")
def country_code(country_code):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = filter_world_data()
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[merged_df["iso_code"] == country_code]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_code_latest/<country_code>")
def country_code_latest(country_code):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = filter_world_data()
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[merged_df["iso_code"] == country_code]
    result_df = result_df[result_df["year"] == result_df["year"].max()]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

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
    result_df.fillna("N/A", inplace=True)
    result_dict = dict(zip(result_df["year"], result_df["co2_growth_prct"]))
    return jsonify(result_dict)

@app.route("/co2-per-capita/<country>")
def co2_per_capita(country):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    result_df = df[df["country"] == country]
    result_df = result_df[["year", "co2_per_capita"]]
    result_df.fillna("N/A", inplace=True)
    result_dict = dict(zip(result_df["year"], result_df["co2_per_capita"]))
    return jsonify(result_dict)

@app.route("/energy-per-capita/<country>")
def energy_per_capita(country):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    result_df = df[df["country"] == country]
    result_df = result_df[["year", "energy_per_capita"]]
    result_df.fillna("N/A", inplace=True)
    result_dict = dict(zip(result_df["year"], result_df["energy_per_capita"]))
    return jsonify(result_dict)

@app.route("/ghg-per-capita/<country>")
def ghg_per_capita(country):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    result_df = df[df["country"] == country]
    result_df = result_df[["year", "ghg_per_capita", "ghg_excluding_lucf_per_capita"]]
    result_df.fillna("N/A", inplace=True)
    result_dict = {
        row["year"]: {
            "ghg_per_capita": row["ghg_per_capita"],
            "ghg_excluding_lucf_per_capita": row["ghg_excluding_lucf_per_capita"],
        }
        for _, row in result_df.iterrows()
    }
    return jsonify(result_dict)

@app.route("/co2-per-gdp/<country>")
def co2_per_gdp(country):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    result_df = df[df["country"] == country]
    result_df = result_df[["year", "co2_per_gdp"]]
    result_df.fillna("N/A", inplace=True)
    result_dict = dict(zip(result_df["year"], result_df["co2_per_gdp"]))
    return jsonify(result_dict)

@app.route("/energy-per-gdp/<country>")
def energy_per_gdp(country):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    result_df = df[df["country"] == country]
    result_df = result_df[["year", "energy_per_gdp"]]
    result_df.fillna("N/A", inplace=True)
    result_dict = dict(zip(result_df["year"], result_df["energy_per_gdp"]))
    return jsonify(result_dict)

@app.route("/co2-per-energy/<country>")
def co2_per_energy(country):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    result_df = df[df["country"] == country]
    result_df = result_df[["year", "co2_per_unit_energy"]]
    result_df.fillna("N/A", inplace=True)
    result_dict = dict(zip(result_df["year"], result_df["co2_per_unit_energy"]))
    return jsonify(result_dict)

@app.route("/co2/<country>")
def country_co2(country):
    # Load datasets
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = filter_world_data()

    # Merge datasets on 'country'
    merged_df = pd.merge(df1, df2, on="country")

    # Filter rows by country
    result_df = merged_df[merged_df["country"] == country]

    # List of terms to exclude from CO2-related fields
    exclude_terms = ["per_capita", "per_gdp", "per_unit_energy", "share", "cumulative", "growth"]

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