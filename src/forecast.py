import pickle
from pathlib import Path
from src.process_data import process_simplicity_data, get_raw_data
from src.config import FORECAST_WINDOW
import pandas as pd
from datetime import datetime

import pandas as pd
import requests
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from sklearn.ensemble import RandomForestRegressor

from .process_data import process_simplicity_data, get_raw_data
from .config import FORECAST_WINDOW


def train_forecaster(year: int = None, month: int = None, day: int = None):
    df = process_simplicity_data(get_raw_data(year=year, month=month, day=day))

    forecaster = ForecasterAutoreg(
        regressor=RandomForestRegressor(random_state=42, n_jobs=-1),
        lags=[*range(1, 25), *range(2 * 24, 15 * 24 + 1, 24)],
    )

    forecaster.fit(y=df["simplicity"])
    return forecaster


def get_prediction():
    df = process_simplicity_data(get_raw_data())
    forecaster = pickle.loads(Path("src/models/forecaster.pickle").read_bytes())
    return forecaster.predict(steps=FORECAST_WINDOW, last_window=df["simplicity"])
