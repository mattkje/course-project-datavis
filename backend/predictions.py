import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


def predict_arima(country, prediction_data):
    df = pd.read_csv("datasets/globalwarmingdata.csv")
    country_df = df[df["country"] == country]
    filter_df = country_df[["year", prediction_data]].dropna()

    filter_df["year"] = pd.to_datetime(filter_df["year"], format='%Y')
    filter_df.set_index("year", inplace=True)

    if filter_df.empty or len(filter_df) < 3:
        raise ValueError(f"Not enough data to make predictions for {prediction_data} in {country}.")

    model = ARIMA(filter_df[prediction_data], order=(1, 1, 1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=5)
    forecast_values = forecast.values
    last_year = filter_df.index.max().year
    predictions = [
        {
            "year": last_year + i + 1,
            prediction_data: float(forecast_values[i])
        }
        for i in range(5)
    ]
    return predictions