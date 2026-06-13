import plotly.express as px


PRIMARY_COLOR = "#52799C"
SECONDARY_COLOR = "#A9C4D9"
TERTIARY_COLOR = "#D3E5F0"
DOMAIN_COLORS = [
    "#52799C",
    "#6B9E78",
    "#C27C49",
    "#8E6BBE",
    "#D0A23F",
    "#4F9AA3",
    "#B35D6A",
    "#737373",
]


def apply_layout(fig, height=520):
    fig.update_layout(
        template="plotly_white",
        title_x=0.02,
        height=height,
        margin=dict(l=20, r=20, t=70, b=40),
        legend_title_text="",
    )
    return fig


def bar_chart(data, x, y, title, labels=None, text=None, color=None, height=520):
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        labels=labels,
        text=text,
        color=color,
        color_discrete_sequence=DOMAIN_COLORS if color else [PRIMARY_COLOR],
    )
    fig.update_traces(marker_line_color="black", marker_line_width=1)
    return apply_layout(fig, height)


def horizontal_bar_chart(data, x, y, title, labels=None, text=None, height=620):
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        labels=labels,
        text=text,
        orientation="h",
        color_discrete_sequence=[PRIMARY_COLOR],
    )
    fig.update_traces(marker_line_color="black", marker_line_width=1)
    fig.update_yaxes(autorange="reversed")
    return apply_layout(fig, height)


def line_chart(data, x, y, color, title, labels=None, height=560):
    fig = px.line(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
        labels=labels,
        markers=True,
        color_discrete_sequence=DOMAIN_COLORS,
    )
    fig.update_traces(line_width=3, marker_size=8)
    return apply_layout(fig, height)


def grouped_bar_chart(data, x, y, color, title, labels=None, height=560):
    fig = px.bar(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
        labels=labels,
        barmode="group",
        color_discrete_sequence=DOMAIN_COLORS,
    )
    fig.update_traces(marker_line_color="black", marker_line_width=0.7)
    return apply_layout(fig, height)


def pie_chart(data, names, values, title, labels=None, height=480):
    fig = px.pie(
        data,
        names=names,
        values=values,
        title=title,
        labels=labels,
        color_discrete_sequence=[PRIMARY_COLOR, SECONDARY_COLOR, TERTIARY_COLOR],
        hole=0.35,
    )
    fig.update_traces(textinfo="percent+label", pull=[0.04] * len(data))
    return apply_layout(fig, height)


def scatter_chart(data, x, y, text, title, labels=None, height=560):
    fig = px.scatter(
        data,
        x=x,
        y=y,
        text=text,
        title=title,
        labels=labels,
        size=[18] * len(data),
        color=text,
        color_discrete_sequence=DOMAIN_COLORS,
    )
    fig.update_traces(textposition="middle right", marker_line_color="black", marker_line_width=1)
    return apply_layout(fig, height)


def box_chart(data, y, title, x=None, labels=None, height=520):
    fig = px.box(
        data,
        x=x,
        y=y,
        title=title,
        labels=labels,
        color=x,
        color_discrete_sequence=DOMAIN_COLORS,
        points="outliers",
    )
    return apply_layout(fig, height)
