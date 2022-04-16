import altair as alt
import streamlit as st

import requests
import pandas as pd

# Ez az apiból húzza be a dolgokat egyből, innen kéne felépíteni a frontendet
# ahhoz hogy működjön indítsd el az api.py-t (ip és port lehet más lesz)
source = pd.DataFrame(
    requests.get(
        "http://44.202.14.43/data?year=2022&month=04&day=15&day_delta=31&group_hours=1"
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
c = alt.layer(line, selectors, points, rules, text).properties(width=600, height=300)

st.title("Igénytelenség vs igényesség az ajándékozás terén")
st.altair_chart(c, use_container_width=True)
