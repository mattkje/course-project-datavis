from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    df_html = df.to_html()
    return render_template('show_csv_data.html', data_var=df_html)

@app.route("/country/<country>")
def country(country):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    df = df[df["country"] == country]
    df_html = df.to_html()
    return render_template('show_csv_data.html', data_var=df_html)

@app.route("/year/<year>")
def year(year):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    df = df[df["year"] == int(year)]
    df_html = df.to_html()
    return render_template('show_csv_data.html', data_var=df_html)

@app.route("/country_year/<country>/<year>")
def country_year(country, year):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    df = df[(df["country"] == country) & (df["year"] == int(year))]
    df_html = df.to_html()
    return render_template('show_csv_data.html', data_var=df_html)

@app.route("/country_year_range/<country>/<start_year>/<end_year>")
def country_year_range(country, start_year, end_year):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    df = df[(df["country"] == country) & (df["year"] >= int(start_year)) & (df["year"] <= int(end_year))]
    df_html = df.to_html()
    return render_template('show_csv_data.html', data_var=df_html)

@app.route("/country_code/<country_code>")
def country_code(country_code):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    df = df[df["iso_code"] == country_code]
    df_html = df.to_html()
    return render_template('show_csv_data.html', data_var=df_html)

@app.route("/country_code_latest/<country_code>")
def country_code_latest(country_code):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    df = df[df["iso_code"] == country_code]
    df = df[df["year"] == df["year"].max()]
    df_html = df.to_html()
    return render_template('show_csv_data.html', data_var=df_html)

notCountries = [
'Africa',
'Africa (GCP)',
'Asia',
'Asia (GCP)',
'Asia (excl. China and India)',
'Central America (GCP)',
'Europe',
'Europe (GCP)',
'Europe (excl. EU-27)',
'Europe (excl. EU-28)',
'European Union (27)',
'European Union (28)',
'High-income countries',
'International aviation',
'International shipping',
'International transport',
'Least developed countries (Jones et al.)',
'Low-income countries',
'Lower-middle-income countries',
'Middle East (GCP)',
'North America',
'North America (GCP)',
'North America (excl. USA)',
'Non-OECD (GCP)',
'Oceania',
'Oceania (GCP)',
'Panama Canal Zone',
'Panama Canal Zone (GCP)',
'Ryukyu Islands',
'Ryukyu Islands (GCP)',
'South America',
'South America (GCP)',
'Upper-middle-income countries',
'World'
]