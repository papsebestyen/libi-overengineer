from datetime import datetime

import pandas as pd
import requests
import streamlit as st

from vizualization import get_tseries_chart

min_date = datetime(2022, 4, 16)
max_date = datetime.now()
date_option = st.sidebar.date_input(
    "Válassz egy dátumot", min_value=min_date, max_value=max_date
)

period_option = st.sidebar.number_input(
    "Válassz egy szakaszt", min_value=1, max_value=365, value=31, step=1
)

hour_grouping_option = st.sidebar.number_input(
    "Válassz egy csoportosítást",
    min_value=1,
    max_value=period_option * 24,
    value=24,
    step=1,
)

# date input, ha vmi kisebb akkor menjen egy minimum date-re
df_query = pd.DataFrame(
    requests.get(
        f"http://44.202.14.43/query_data?year={date_option.year:02}&month={date_option.month:02}&day={date_option.day:02}\
            &day_delta={period_option}&group_hours={hour_grouping_option}"
    ).json()
).assign(date=lambda _df: pd.to_datetime(_df["date"]))


chart = get_tseries_chart(
    df=df_query, date_col="date", variable_col="variable", value_col="searches"
)

st.title("Igénytelenség vs igényesség az ajándékozás terén")
st.altair_chart(chart, use_container_width=True)
