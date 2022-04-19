import pickle
from pathlib import Path

from skforecast.ForecasterAutoreg import ForecasterAutoreg
from sklearn.ensemble import RandomForestRegressor

from src.config import FORECAST_WINDOW
from src.process_data import get_raw_data, get_simplicity_data


def train_forecaster(year: int = None, month: int = None, day: int = None):
    df = get_simplicity_data(
        get_raw_data(year=year, month=month, day=day, with_prediction=False)
    )

    forecaster = ForecasterAutoreg(
        regressor=RandomForestRegressor(random_state=42, n_jobs=-1),
        lags=[*range(1, 25), *range(2 * 24, 15 * 24 + 1, 24)],
    )

    forecaster.fit(y=df["simplicity"])
    return forecaster


def get_prediction():
    df = get_simplicity_data(
        get_raw_data(), day_delta=365, group_hours=1, with_prediction=False
    )
    forecaster = pickle.loads(
        Path("src/models/forecaster.pickle").read_bytes()
    )
    return forecaster.predict(
        steps=FORECAST_WINDOW, last_window=df["simplicity"]
    )
