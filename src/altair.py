from datetime import datetime

import pandas as pd
import requests
import streamlit as st

import altair as alt

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
source = pd.DataFrame(
    requests.get(
        f"http://44.202.14.43/query_data?year={date_option.year:02}&month={date_option.month:02}&day={date_option.day:02}\
            &day_delta={period_option}&group_hours={hour_grouping_option}"
    ).json()
).assign(date=lambda _df: pd.to_datetime(_df["date"]))


# Create a selection that chooses the nearest point & selects based on x-value

nearest = alt.selection(
    type="single", nearest=True, on="mouseover", fields=["date"], empty="none"
)

# The basic line
line = (
    alt.Chart(source)
    .mark_line(interpolate="basis")
    .encode(x="date:T", y="searches:Q", color="variable:N")
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = (
    alt.Chart(source)
    .mark_point()
    .encode(
        x="date:T",
        opacity=alt.value(0),
    )
    .add_selection(nearest)
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align="left", dx=5, dy=-5).encode(
    text=alt.condition(nearest, "searches:Q", alt.value(" "))
)

# Draw a rule at the location of the selection
rules = (
    alt.Chart(source)
    .mark_rule(color="gray")
    .encode(
        x="date:T",
    )
    .transform_filter(nearest)
)

# Put the five layers into a chart and bind the data
c = alt.layer(line, selectors, points, rules, text).properties(
    width=600, height=300
)

st.title("Igénytelenség vs igényesség az ajándékozás terén")
st.altair_chart(c, use_container_width=True)
