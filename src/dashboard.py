from datetime import datetime
from json import dumps

import pandas as pd
import requests
import streamlit as st

from vizualization import get_tseries_chart

with st.sidebar:
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

    show_forecast = st.checkbox(
        "Előrejelzés",
        value=False,
        disabled=False if date_option == max_date.date() else True,
    )

df_query = pd.DataFrame(
    requests.get(
        f"http://44.202.14.43/query_data?\
        year={date_option.year:02}&month={date_option.month:02}&day={date_option.day:02}\
        &day_delta={period_option}&group_hours={hour_grouping_option}"
    ).json()
).assign(date=lambda _df: pd.to_datetime(_df["date"]))

df_simplicity = pd.DataFrame(
    requests.get(
        f"http://44.202.14.43/simplicity_data?\
        year={date_option.year:02}&month={date_option.month:02}&day={date_option.day:02}\
        &day_delta={period_option}&group_hours={hour_grouping_option}\
        &with_prediction={dumps(show_forecast)}"
    ).json()
).assign(date=lambda _df: pd.to_datetime(_df["date"]))


chart_query = get_tseries_chart(
    df=df_query, date_col="date", variable_col="variable", value_col="searches"
)

st.markdown(
    """
# Ajándékozás keresések

#### Ajándékozáshoz kapcsolódó Google keresések időbeli alakulása

Az értékek arányokat mutatnak. Az elmúlt 1 évben egy órában tapasztalható \
legnagyobb jelenti a 100-at, a többi érték pedig ehhez képest aránylik.
"""
)

st.altair_chart(chart_query, use_container_width=True)

chart_simplicity = get_tseries_chart(
    df=df_simplicity,
    date_col="date",
    variable_col="variable",
    value_col="searches",
)

st.markdown(
    """
# Igénytelenség index (II) alakulása

#### Az általunk összeállított igénytelenség mutató alakulása
"""
)
st.latex(r"II_t = \frac{bögre\ keresések_t}{ajándék\ keresések_t}")
st.altair_chart(chart_simplicity, use_container_width=True)
