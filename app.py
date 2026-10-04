
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="MIE1624 Assignment 1 Dashboard",
    page_icon="📊",
    layout="wide"
)

ASSET = Path(__file__).parent / "assets"

st.title("Stack Overflow Developer Salary Analysis")
st.caption("2025 Stack Overflow Developer Survey · MIE1624 Assignment 1")

st.info(
    "This dashboard uses only aggregated results and figures generated from the "
    "submitted Jupyter Notebook. No respondent-level dataset is embedded."
)

section = st.sidebar.radio(
    "Navigate",
    [
        "Executive Summary",
        "Q1 · Exploratory Analysis",
        "Q2 · Remote vs Hybrid",
        "Q3 · Education & Salary",
        "Methods & Notes",
    ],
)

if section == "Executive Summary":
    st.header("Executive Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Hybrid mean salary", "$83,335")
    c2.metric("Remote mean salary", "$94,688")
    c3.metric("Remote − Hybrid", "$11,353")
    c4.metric("Education ANOVA", "p < 0.001")

    st.markdown(
        """
        **Key findings**
        - Remote respondents had higher mean and median annual salaries than Hybrid respondents after the common IQR outlier treatment.
        - The Remote − Hybrid mean difference was about **$11.4k**, and both the t-test and 95% confidence intervals supported a statistically significant difference.
        - In the U.S. and Canada, Bachelor's degree holders had a lower average salary than the Master's and Professional groups.
        - The original and bootstrap ANOVA procedures both rejected equality of the three education-group means.
        """
    )

    st.subheader("Interactive summary")
    summary = pd.DataFrame(
        {
            "Group": ["Hybrid", "Remote", "Bachelor's", "Master's", "Professional"],
            "Mean Salary": [83335.16, 94687.76, 143262.86, 156808.69, 155847.99],
        }
    ).set_index("Group")
    st.bar_chart(summary)

elif section == "Q1 · Exploratory Analysis":
    st.header("Question 1 · Exploratory Data Analysis")
    st.write(
        "Job titles with fewer than 50 valid observations were excluded from "
        "role-level summaries to reduce instability."
    )

    tab1, tab2, tab3 = st.tabs(
        ["Job Satisfaction", "Salary by Job Title", "Salary vs Age"]
    )

    with tab1:
        st.image(
            str(ASSET / "q1_job_satisfaction.png"),
            caption="Average Job Satisfaction by Job Title",
            use_container_width=True,
        )
        st.write(
            "Most sufficiently represented roles cluster around 7–8 points. "
            "Senior executives and founders report the highest average satisfaction, "
            "while QA/test developers are lowest among the retained roles."
        )

    with tab2:
        st.image(
            str(ASSET / "q1_salary_by_job.png"),
            caption="Mean Salary by Job Title — IQR Outliers Removed",
            use_container_width=True,
        )
        st.write(
            "Mean compensation varies substantially by job title. After IQR-based "
            "outlier treatment, differences are less extreme, while senior and "
            "managerial roles remain among the highest-paid."
        )

    with tab3:
        st.image(
            str(ASSET / "q1_salary_vs_age_log.png"),
            caption="Annual Salary vs Age — Log Salary Scale",
            use_container_width=True,
        )
        st.write(
            "Compensation generally rises during earlier career stages and becomes "
            "more gradual later. The log scale reduces visual compression caused by "
            "the strongly right-skewed salary distribution."
        )

elif section == "Q2 · Remote vs Hybrid":
    st.header("Question 2 · Remote vs Hybrid Salary Comparison")

    st.subheader("Descriptive statistics")
    q2_stats = pd.DataFrame(
        [
            ["Hybrid", 7565, 83335.16, 75410, 52600.63],
            ["Remote", 6585, 94687.76, 87000, 63131.07],
        ],
        columns=["Work Arrangement", "n", "Mean Salary", "Median Salary", "Std. Dev."],
    )
    st.dataframe(
        q2_stats.style.format(
            {"Mean Salary": "${:,.0f}", "Median Salary": "${:,.0f}", "Std. Dev.": "${:,.0f}"}
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "A common 1.5×IQR upper threshold of $256,963.50 was applied. "
        "This removed 238 Hybrid observations (3.05%) and 349 Remote observations (5.03%)."
    )

    st.subheader("Two-sample t-test")
    ttest = pd.DataFrame(
        [
            ["Manual pooled t-test", -11.665912, 2.647665e-31],
            ["SciPy pooled t-test", -11.665912, 2.647665e-31],
            ["Bootstrap-mean t-test", -1152.139650, 0.0],
        ],
        columns=["Method", "t-statistic", "p-value"],
    )
    st.dataframe(ttest, use_container_width=True, hide_index=True)
    st.write(
        "The manual and built-in tests agree exactly and reject equal mean salaries. "
        "The bootstrap-mean test reaches the same conclusion; its much larger absolute "
        "t-statistic reflects the lower variability of sample means relative to individual salaries."
    )

    st.subheader("Bootstrap analysis · 10,000 replications")
    tab1, tab2, tab3 = st.tabs(
        ["Group mean distributions", "Remote − Hybrid difference", "Standardized difference"]
    )
    with tab1:
        st.image(str(ASSET / "q2_bootstrap_means.png"), use_container_width=True)
    with tab2:
        st.image(str(ASSET / "q2_bootstrap_difference.png"), use_container_width=True)
    with tab3:
        st.image(str(ASSET / "q2_standardized_difference.png"), use_container_width=True)

    st.subheader("95% confidence intervals")
    ci = pd.DataFrame(
        [
            ["Formula-based t interval", 9445.11, 13260.09],
            ["Bootstrap percentile interval", 9396.20, 13277.91],
        ],
        columns=["Method", "Lower", "Upper"],
    )
    st.dataframe(
        ci.style.format({"Lower": "${:,.0f}", "Upper": "${:,.0f}"}),
        use_container_width=True,
        hide_index=True,
    )
    st.success(
        "Both intervals lie entirely above zero, supporting a positive Remote − Hybrid mean salary difference."
    )

    st.subheader("Median-based comparison")
    c1, c2, c3 = st.columns(3)
    c1.metric("Hybrid median", "$75,410")
    c2.metric("Remote median", "$87,000")
    c3.metric("Remote − Hybrid median", "$11,590")

    median_tests = pd.DataFrame(
        [
            ["Mood's median test", 68.641745, 1.180779e-16],
            ["Bootstrap median test", None, 0.0],
        ],
        columns=["Method", "Statistic", "p-value"],
    )
    st.dataframe(median_tests, use_container_width=True, hide_index=True)

elif section == "Q3 · Education & Salary":
    st.header("Question 3 · Education Level and Salary")
    st.write(
        "Analysis is restricted to respondents in the United States and Canada and "
        "compares Bachelor's, Master's, and Professional degree holders."
    )

    st.subheader("Descriptive statistics after outlier treatment")
    q3_stats = pd.DataFrame(
        [
            ["Bachelor's", 2840, 143262.86, 138621, 62500.03],
            ["Master's", 1013, 156808.69, 150000, 69626.16],
            ["Professional", 275, 155847.99, 151000, 70621.96],
        ],
        columns=["Education", "n", "Mean Salary", "Median Salary", "Std. Dev."],
    )
    st.dataframe(
        q3_stats.style.format(
            {"Mean Salary": "${:,.0f}", "Median Salary": "${:,.0f}", "Std. Dev.": "${:,.0f}"}
        ),
        use_container_width=True,
        hide_index=True,
    )
    st.caption("Common 1.5×IQR upper threshold: $348,500.")

    st.subheader("One-way ANOVA")
    c1, c2 = st.columns(2)
    c1.metric("Original F-statistic", "18.758")
    c2.metric("Original p-value", "7.77 × 10⁻⁹")
    st.write(
        "The null hypothesis of equal mean salaries across all three education groups is rejected."
    )

    st.subheader("Bootstrap analysis · 10,000 replications")
    tab1, tab2, tab3 = st.tabs(
        ["Three mean distributions", "Pairwise mean differences", "Standardized differences"]
    )
    with tab1:
        st.image(str(ASSET / "q3_bootstrap_means.png"), use_container_width=True)
        st.write(
            "The Bachelor's distribution is shifted left of the Master's and Professional distributions."
        )
    with tab2:
        st.image(str(ASSET / "q3_pairwise_differences.png"), use_container_width=True)
        st.write(
            "Master − Bachelor and Professional − Bachelor are concentrated above zero, "
            "while Professional − Master overlaps zero substantially."
        )
    with tab3:
        st.image(str(ASSET / "q3_standardized_differences.png"), use_container_width=True)
        st.write(
            "After standardization, the pairwise distributions are centered near zero "
            "with broadly similar shapes."
        )

    st.subheader("Bootstrap ANOVA")
    anova = pd.DataFrame(
        [
            ["Original-data ANOVA", 18.757987, 7.768408e-09],
            ["Bootstrap ANOVA", 19.884159, 9.999000e-05],
        ],
        columns=["Method", "F-statistic", "p-value"],
    )
    st.dataframe(anova, use_container_width=True, hide_index=True)
    st.success(
        "Both the original and bootstrap procedures reject equality of the three mean salaries."
    )

elif section == "Methods & Notes":
    st.header("Methods & Notes")
    st.markdown(
        """
        **Dataset**
        - 2025 Stack Overflow Developer Survey cleaned dataset used in the submitted notebook.
        - The public dashboard contains only aggregated results and exported figures.

        **Outlier treatment**
        - Q2: common 1.5×IQR upper salary threshold = **$256,963.50**.
        - Q3: common 1.5×IQR upper salary threshold = **$348,500**.

        **Inference**
        - Q2 uses pooled two-sample t-tests, bootstrap resampling, confidence intervals, and Mood's median test.
        - Q3 uses one-way ANOVA and a bootstrap null distribution for the ANOVA F-statistic.
        - Bootstrap procedures use **10,000 replications**.

        **Important interpretation**
        - Results describe associations in the survey sample and should not be interpreted as causal effects of work mode or education on salary.
        """
    )
