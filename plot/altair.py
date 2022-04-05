import pandas as pd
import altair as alt
import numpy as np

historicaldf_forplot = pd.read_parquet(data_path / f"data_{date_range}_day.parquet")

historicaldf_forplot = pd.melt(historicaldf.reset_index(), id_vars='date', value_vars=['gift','mug','diy'], var_name=None, value_name='searches', col_level=None, ignore_index=True)

source = historicaldf_forplot.sort_values(by='date')[0:4999]
# Create a selection that chooses the nearest point & selects based on x-value

nearest = alt.selection(type='single', nearest=True, on='mouseover',
fields=['date'], empty='none')

# The basic line
line = alt.Chart(source).mark_line(interpolate='basis').encode(
    x='date:T',
    y='searches:Q',
    color='variable:N'
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = alt.Chart(source).mark_point().encode(
    x='date:T',
    opacity=alt.value(0),
).add_selection(
    nearest
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'searches:Q', alt.value(' '))
)

# Draw a rule at the location of the selection
rules = alt.Chart(source).mark_rule(color='gray').encode(
    x='date:T',
).transform_filter(
    nearest
)

# Put the five layers into a chart and bind the data
alt.layer(
    line, selectors, points, rules, text
).properties(
    width=600, height=300
)