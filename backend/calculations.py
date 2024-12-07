import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


def predict_arima(country, prediction_data):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    country_df = df[df["country"] == country]
    filter_df = country_df.dropna(subset=["year"])

    if prediction_data == "co2":
        exclude_terms = ["per_capita", "per_gdp", "per_unit_energy", "share", "cumulative", "growth","temperature"]
        co2_columns = [
            col for col in filter_df.columns
            if "co2" in col and not any(term in col for term in exclude_terms)
        ]
        co2_columns.append('year')
        result_df = filter_df[co2_columns].copy()

    elif prediction_data == "gdp":
        gdp_columns = [
            col for col in filter_df.columns
            if "_gdp" in col
        ]
        gdp_columns.append('year')
        result_df = filter_df[gdp_columns].copy()

    elif prediction_data == "per_capita":
        per_capita_columns = [
            col for col in filter_df.columns
            if "per_capita" in col
               and "energy" not in col
        ]
        per_capita_columns.append('year')
        result_df = filter_df[per_capita_columns].copy()

    elif prediction_data == "co2_growth_prct":
        result_df = filter_df[["year", "co2_growth_prct"]].copy()

    else:
        result_df = pd.DataFrame()

    if result_df.empty or len(result_df) < 3:
        raise ValueError(f"Not enough data to make predictions for {prediction_data} in {country}.")

    result_df["year"] = pd.to_datetime(filter_df["year"], format='%Y')
    result_df.set_index("year", inplace=True)

    predictions = []
    last_year = result_df.index.max().year

    for column in result_df.columns:
        if column == 'year':
            continue
        model = ARIMA(result_df[column], order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=5)
        forecast_values = forecast.values
        for i in range(5):
            if len(predictions) <= i:
                predictions.append({"year": last_year + i + 1, "country": country})
            predictions[i][column] = round(float(forecast_values[i]), 3)

    return predictions

def calculate_democracy_rank(country):
    df = pd.read_csv("datasets/democracy-index-eiu.csv")
    filter_df = df[df["year"] == 2023]
    filter_df = filter_df.sort_values(by="DemocracyScore", ascending=False).reset_index(drop=True)

    if country not in filter_df["country"].values:
        raise ValueError(f"No data found for {country} in 2023.")
    country_rank = filter_df[filter_df["country"] == country].index[0] + 1
    return country_rank