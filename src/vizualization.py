import altair as alt


def get_tseries_chart(
    df,
    date_col: str = "date",
    variable_col: str = "variable",
    value_col: str = "searches",
):
    nearest = alt.selection(
        type="single",
        nearest=True,
        on="mouseover",
        fields=[date_col],
        empty="none",
    )

    line = (
        alt.Chart(df)
        .mark_line(interpolate="basis")
        .encode(
            x=f"{date_col}:T", y=f"{value_col}:Q", color=f"{variable_col}:N"
        )
    )

    selectors = (
        alt.Chart(df)
        .mark_point()
        .encode(
            x=f"{date_col}:T",
            opacity=alt.value(0),
        )
        .add_selection(nearest)
    )

    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    text = line.mark_text(align="left", dx=5, dy=-5).encode(
        text=alt.condition(nearest, f"{value_col}:Q", alt.value(" "))
    )

    rules = (
        alt.Chart(df)
        .mark_rule(color="gray")
        .encode(
            x=f"{date_col}:T",
        )
        .transform_filter(nearest)
    )

    return alt.layer(line, selectors, points, rules, text).properties(
        width=600, height=300
    )
