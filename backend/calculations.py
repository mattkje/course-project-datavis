import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def better_predict_arima(country, prediction_data):
    # Load the dataset
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    # Filter for the selected country
    country_df = df[(df["country"] == country) & (df["year"] >= 2000)]
    # Drop rows where the 'year' column is NaN
    filter_df = country_df.dropna(subset=["year"])

    # Extract only the 'year' and the specified prediction data column
    result_df = filter_df[["year", prediction_data]].copy()
    # Convert 'year' to datetime and set it as index
    result_df["year"] = pd.to_datetime(filter_df["year"], format='%Y')
    result_df.set_index("year", inplace=True)

    # Prepare for predictions
    predictions = []
    last_year = result_df.index.max().year  # The last year in the existing data

    # Loop over columns in case there are multiple columns to forecast (though you're focusing on one)
    for column in result_df.columns:
        # Fit an ARIMA model
        model = ARIMA(result_df[column], order=(1, 1, 2))
        model_fit = model.fit()
        # Forecast 5 years into the future
        forecast = model_fit.forecast(steps=5)
        forecast_values = forecast.values

        # Build the output in the desired format
        for i in range(5):
            year = last_year + i + 1
            value = round(float(forecast_values[i]), 3)
            # Append the forecast for each year in a structured dictionary
            predictions.append({
                country: value,
                "year": year
            })

    return predictions

def better_predict_holt_winters(country, prediction_data):
    # Load the dataset
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    # Filter for the selected country
    country_df = df[(df["country"] == country) & (df["year"] >= 2000)]
    # Drop rows where the 'year' column is NaN
    filter_df = country_df.dropna(subset=["year"])

    # Extract only the 'year' and the specified prediction data column
    result_df = filter_df[["year", prediction_data]].copy()
    # Convert 'year' to datetime and set it as index
    result_df["year"] = pd.to_datetime(filter_df["year"], format='%Y')
    result_df.set_index("year", inplace=True)

    # Prepare for predictions
    predictions = []
    last_year = result_df.index.max().year  # The last year in the existing data

    # Loop over columns in case there are multiple columns to forecast (though you're focusing on one)
    for column in result_df.columns:
        # Fit an Exponential Smoothing model without seasonality
        model = ExponentialSmoothing(result_df[column], trend='add', seasonal=None)
        model_fit = model.fit()
        # Forecast 5 years into the future
        forecast = model_fit.forecast(steps=5)

        # Build the output in the desired format
        for i in range(5):
            year = last_year + i + 1
            value = round(float(forecast.iloc[i]), 3)
            # Append the forecast for each year in a structured dictionary
            predictions.append({
                country: value,
                "year": year
            })

    return predictions

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

import pandas as pd

def calculate_correlation(df, col1, col2, method='pearson'):
    """
    Calculate the correlation between two columns in a DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.
    - col1 (str): The name of the first column.
    - col2 (str): The name of the second column.
    - method (str): The correlation method to use. Available: 'pearson', 'spearman', 'kendall'.

    Returns:
    - The correlation coefficient.
    """
    if col1 not in df.columns or col2 not in df.columns:
        raise ValueError(f"Columns '{col1}' and/or '{col2}' not found in DataFrame.")

    correlation = df[[col1, col2]].corr(method=method).iloc[0, 1]
    return correlation
