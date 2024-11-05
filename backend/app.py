from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(df.to_dict(orient="records"))

@app.route("/country/<country>")
def country(country):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = pd.read_csv("datasets/world-data-2023.csv")
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[merged_df["country"] == country]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/year/<year>")
def year(year):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = pd.read_csv("datasets/world-data-2023.csv")
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[merged_df["year"] == int(year)]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_year/<country>/<year>")
def country_year(country, year):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = pd.read_csv("datasets/world-data-2023.csv")
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[(merged_df["country"] == country) & (merged_df["year"] == int(year))]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_year_range/<country>/<start_year>/<end_year>")
def country_year_range(country, start_year, end_year):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = pd.read_csv("datasets/world-data-2023.csv")
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[(merged_df["country"] == country) & (merged_df["year"] >= int(start_year)) & (merged_df["year"] <= int(end_year))]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_code/<country_code>")
def country_code(country_code):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = pd.read_csv("datasets/world-data-2023.csv")
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[merged_df["iso_code"] == country_code]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/country_code_latest/<country_code>")
def country_code_latest(country_code):
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = pd.read_csv("datasets/world-data-2023.csv")
    merged_df = pd.merge(df1, df2, on="country")
    result_df = merged_df[merged_df["iso_code"] == country_code]
    result_df = result_df[result_df["year"] == result_df["year"].max()]
    result_df.fillna("N/A", inplace=True)  # Replace NaN values with "N/A"
    return jsonify(result_df.to_dict(orient="records"))

@app.route("/co2/<country>")
def country_co2(country):
    # Load datasets
    df1 = pd.read_csv("datasets/globalwarmingdata.csv")
    df2 = pd.read_csv("datasets/world-data-2023.csv")

    # Merge datasets on 'country'
    merged_df = pd.merge(df1, df2, on="country")

    # Filter rows by country
    result_df = merged_df[merged_df["country"] == country]

    # List of terms to exclude from CO2-related fields
    exclude_terms = ["per_capita", "per_gdp", "per_unit_energy","share","cumulative","growth"]

    # Select CO2 columns, excluding specific variants, plus 'year'
    co2_columns = [
        col for col in result_df.columns
        if "co2" in col and not any(term in col for term in exclude_terms)
    ]

    # Ensure 'year' is included
    if 'year' in result_df.columns:
        co2_columns.append('year')

    # Filter the DataFrame to only include selected CO2 columns and 'year'
    co2_data_df = result_df[co2_columns]

    # Replace NaN values with "N/A"
    co2_data_df.fillna("N/A", inplace=True)

    # Convert the filtered DataFrame to JSON format
    return jsonify(co2_data_df.to_dict(orient="records"))