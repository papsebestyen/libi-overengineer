from datetime import datetime, timedelta

import pandas as pd

from .config import FORECAST_WINDOW
from .s3 import FileStorage

storage = FileStorage()


def get_raw_data(
    year: int = None,
    month: int = None,
    day: int = None,
) -> pd.DataFrame:
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    day = day or now.day

    return (
        pd.read_parquet(
            storage.download_bytes(f"{year:02}-{month:02}-{day:02}.parquet")
        )
        .reset_index()
        .drop_duplicates(subset="date")
        .dropna()
        .set_index("date")
        .asfreq("1H")
    )


def get_query_data(
    df,
    day_delta: int = 365,
    group_hours: int = 1,
) -> pd.DataFrame:
    """Get data for altair vizualization"""

    return (
        df.loc[
            lambda _df: _df.index >= (_df.index.max() - timedelta(days=day_delta)),
            :,
        ]
        .resample(f"{group_hours}H")
        .mean()
        .reset_index()
        .melt(
            id_vars="date",
            value_vars=["gift", "mug", "diy"],
            value_name="searches",
        )
        .sort_values(by="date")
    )


def get_simplicity_data(
    df,
    day_delta: int = 365,
    group_hours: int = 1,
    with_prediction: bool = False,
) -> pd.DataFrame:
    df = (
        df.assign(
            simplicity=lambda _df: _df["mug"] / _df["gift"],
        )
        .drop(columns=["gift", "mug", "diy", "isPartial"])
        .loc[
            lambda _df: _df.index >= (_df.index.max() - timedelta(days=day_delta)),
            :,
        ]
        .resample(f"{group_hours}H")
        .mean()
    )
    if with_prediction:
        storage = FileStorage()
        prediction = pd.read_parquet(storage.download_bytes("prediction.parquet"))
        df = df.join(prediction.resample(f"{group_hours}H").mean(), how="outer").assign(
            pred=lambda _df: _df["pred"].mask(~_df["simplicity"].isna())
        )
    return (
        df.reset_index()
        .rename(columns={"index": "date"})
        .melt(
            id_vars="date",
            value_name="searches",
        )
        .dropna()
    )
