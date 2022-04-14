from datetime import datetime, timedelta
from pathlib import Path

from pytrends.request import TrendReq


kw_list = ["gift", "mug", "diy"]
days_before = [365, 30, 1]


def get_day_before(day=datetime.now(), delta_days=365):
    return day - timedelta(days=delta_days)


pytrend = TrendReq()
pytrend.build_payload(kw_list, timeframe="today 12-m")


def get_data(day: datetime, data_path: Path):
    """ "Get data from Google Trends."""

    for date_range in days_before:
        past = get_day_before(day, date_range)

        df = pytrend.get_historical_interest(
            kw_list,
            year_start=past.year,
            month_start=past.month,
            day_start=past.day,
            hour_start=past.hour,
            year_end=day.year,
            month_end=day.month,
            day_end=day.day,
            hour_end=day.hour,
            cat=0,
            geo="",
            gprop="",
            sleep=0,
        )
        df.to_parquet(data_path / f"{day:%Y-%m-%d}_{date_range}.parquet")
