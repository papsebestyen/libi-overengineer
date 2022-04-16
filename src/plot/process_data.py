from pathlib import Path
from datetime import datetime, timedelta
from s3 import FileStorage

import pandas as pd

storage = FileStorage()

def process_data(
    year: int = None,
    month: int = None,
    day: int = None,
    day_delta: int = 365,
    group_hours: int = 1,
) -> pd.DataFrame:
    """Get data for altair vizualization"""
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    day = day or now.day

    return (
        pd.read_parquet(storage.download_bytes(f"{year:02}-{month:02}-{day:01}.parquet"))
        .loc[lambda _df: _df.index >= (_df.index.max() - timedelta(days=day_delta)), :]
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
