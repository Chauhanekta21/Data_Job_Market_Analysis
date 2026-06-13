import streamlit as st

from utils.formatting import insight_box


st.title("Final Insights & Recommendations")
st.write(
    "This page preserves the final notebook summary and presents the complete analytical conclusion."
)

final_insights = [
    "Data Science emerged as the most dominant domain in the dataset, with the highest job demand from 2020-2024. Data Engineering and Data Analysis also showed consistently strong demand, making them key hiring areas in the data industry.",
    "Machine Learning & AI stood out as the highest-paying and fastest-growing domain. Although its job demand was lower than Data Science, its salary growth increased rapidly, highlighting strong market value for AI-related skills.",
    "Data Analysis and Business Intelligence had high hiring demand but comparatively lower salaries, showing that high demand does not always translate into high pay, especially in more common or entry-focused roles.",
    "Leadership, Management, and specialized Architecture roles offered very high salaries despite lower hiring demand, indicating that senior expertise and niche skills are highly valued.",
    "Overall job demand across most domains increased from 2020-2023, reflecting strong industry growth, but several domains showed a decline in 2024, which may indicate incomplete data or market shifts.",
    "Experience level had a strong impact on both salary and hiring. Senior roles had the highest demand, while Executive roles earned the highest salaries. Entry-level roles had lower salaries and fewer opportunities.",
    "On-site work was the most common work model at 57.75% across all domains. Remote jobs also had a strong presence at 38.83% and were relatively well-paid, while Hybrid roles remained very limited at 3.41%.",
    "Medium-sized companies provided the strongest overall opportunities, with the highest hiring and median salaries. Small companies showed the lowest hiring and salary levels.",
    "Full-time employment dominated the job market, while Contract, Part-time, and Freelance roles remained limited, showing a strong preference for stable long-term employment.",
    "High-paying data roles were distributed across multiple countries including the United States, Canada, Qatar, Saudi Arabia, and others, showing global demand for data professionals.",
    "Overall, the data industry showed strong growth from 2020-2024, especially in AI, Data Science, and Engineering domains, with a clear preference for experienced professionals, specialized skills, and full-time roles.",
]

for index, insight in enumerate(final_insights, start=1):
    st.markdown(f"**{index}.** {insight}")

st.divider()

insight_box(
    "Portfolio Recommendations",
    [
        "Candidates targeting high salary growth should prioritize Machine Learning & AI, Data Architecture, and leadership-oriented skills.",
        "Candidates targeting broader job availability should focus on Data Science, Data Engineering, and Data Analysis.",
        "Early-career candidates should note that entry-level openings are more limited, so portfolio projects and practical skill proof are important.",
        "Remote opportunities remain meaningful, but on-site roles still dominate the dataset.",
        "Medium-sized companies appear strongest overall because they combine high hiring volume with strong median salaries.",
    ],
)
