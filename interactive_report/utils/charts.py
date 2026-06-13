import plotly.express as px


PRIMARY_COLOR = "#52799C"


def bar_chart(data, x, y, title, labels=None, text=None):
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        labels=labels,
        text=text,
        color_discrete_sequence=[PRIMARY_COLOR],
    )
    fig.update_traces(marker_line_color="black", marker_line_width=1)
    fig.update_layout(template="plotly_white", title_x=0.02)
    return fig
