def format_number(value: int | float) -> str:
    return f"{value:,.0f}"


def format_currency(value: int | float) -> str:
    return f"${value / 1000:,.0f}K"


def page_intro(title: str, body: str) -> None:
    import streamlit as st

    st.title(title)
    st.write(body)


def insight_box(title: str, insights: list[str]) -> None:
    import streamlit as st

    with st.container(border=True):
        st.subheader(title)
        for insight in insights:
            st.markdown(f"- {insight}")
