from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from pytrends.request import TrendReq


kw_list = ["gift", "mug", "diy"]
days_before = [365, 30, 1]


def get_day_before(day_before=365):
    return datetime.now() - timedelta(days=day_before)


pytrend = TrendReq()
pytrend.build_payload(kw_list, timeframe="today 12-m")


def get_data(data_path: Path):
    """ "Get data from Google Trends."""
    now = datetime.now()

    for date_range in days_before:
        past = get_day_before(date_range)

        df = pytrend.get_historical_interest(
            kw_list,
            year_start=past.year,
            month_start=past.month,
            day_start=past.day,
            hour_start=past.hour,
            year_end=now.year,
            month_end=now.month,
            day_end=now.day,
            hour_end=now.hour,
            cat=0,
            geo="",
            gprop="",
            sleep=0,
        )
        df.to_parquet(data_path / f"data_{date_range}_day.parquet")
