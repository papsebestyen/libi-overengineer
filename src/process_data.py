from datetime import datetime, timedelta
from .s3 import FileStorage

import pandas as pd

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


def process_query_data(
    df,
    day_delta: int = 365,
    group_hours: int = 1,
) -> pd.DataFrame:
    """Get data for altair vizualization"""

    return (
        df.loc[
            lambda _df: _df.index >= (_df.index.max() - timedelta(days=day_delta)), :
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


def process_simplicity_data(
    df,
    day_delta: int = 365,
    group_hours: int = 1,
) -> pd.DataFrame:
    return (
        df.assign(
            simplicity=lambda _df: _df["mug"] / _df["gift"],
        )
        .drop(columns=["gift", "mug", "diy"])
        .loc[lambda _df: _df.index >= (_df.index.max() - timedelta(days=day_delta)), :]
        .resample(f"{group_hours}H")
        .mean()
    )
