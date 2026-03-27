# app/ds_dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AcademicPulse",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AcademicPulse")
st.markdown("### Student Risk Detection Dashboard (DS + ML)")

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('data/raw/student_data.csv')

    df['avg_exam_score'] = df[['exam1','exam2','exam3','exam4']].mean(axis=1)
    df['exam_trend'] = df['exam4'] - df['exam1']

    df['sleep_category'] = pd.cut(
        df['sleep_hours_per_night'],
        bins=[0,6,8,12],
        labels=['Insufficient','Healthy','Excessive']
    )

    df['study_category'] = pd.cut(
        df['study_hours_per_week'],
        bins=[0,10,20,40],
        labels=['Low','Moderate','High']
    )

    return df


@st.cache_data
def load_ml_data():
    return pd.read_csv('data/processed/ml_predictions.csv')


# -------------------------------
# LOAD DATA SAFELY
# -------------------------------
try:
    df = load_data()
    st.sidebar.success("DS Data Loaded")
except:
    st.error("Run preprocessing first → python src/data_preprocessing.py")
    st.stop()

try:
    ml_df = load_ml_data()
    st.sidebar.success("ML Data Loaded")
except:
    ml_df = None
    st.sidebar.warning("ML predictions not found")

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("Filters")

risk_filter = st.sidebar.multiselect(
    "Risk Level",
    ['Low','Medium','High'],
    default=['Low','Medium','High']
)

trend_filter = st.sidebar.multiselect(
    "Performance Trend",
    ['improving','declining','stable'],
    default=['improving','declining','stable']
)

filtered_df = df[
    df['actual_risk'].isin(risk_filter) &
    df['performance_trend'].isin(trend_filter)
]

# -------------------------------
# TABS
# -------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Academic",
    "Behavioral",
    "Student Explorer",
    "ML Insights 🚀"
])

# ===============================
# TAB 1: OVERVIEW
# ===============================
with tab1:
    st.header("Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Students", len(filtered_df))
    col2.metric("Avg Attendance", f"{filtered_df['attendance'].mean():.1f}%")
    col3.metric("Avg Score", f"{filtered_df['avg_exam_score'].mean():.1f}")
    col4.metric("Avg Study Hours", f"{filtered_df['study_hours_per_week'].mean():.1f}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(
            filtered_df,
            names="actual_risk",
            title="Risk Distribution",
            color="actual_risk",
            color_discrete_map={'Low':'green','Medium':'orange','High':'red'}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(
            filtered_df,
            x="performance_trend",
            color="performance_trend",
            title="Performance Trends"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Summary Stats")
    st.dataframe(filtered_df.describe())

# ===============================
# TAB 2: ACADEMIC
# ===============================
with tab2:
    st.header("Academic Analysis")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.box(filtered_df, x="actual_risk", y="attendance", color="actual_risk")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.box(filtered_df, x="actual_risk", y="avg_exam_score", color="actual_risk")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Exam Trend")

    exams = ['exam1','exam2','exam3','exam4']
    means = filtered_df.groupby("actual_risk")[exams].mean()

    fig = go.Figure()

    for risk in means.index:
        fig.add_trace(go.Scatter(
            x=exams,
            y=means.loc[risk],
            mode="lines+markers",
            name=risk
        ))

    st.plotly_chart(fig, use_container_width=True)

# ===============================
# TAB 3: BEHAVIORAL
# ===============================
with tab3:
    st.header("Behavioral Analysis")

    fig = px.scatter(
        filtered_df,
        x="study_hours_per_week",
        y="sleep_hours_per_night",
        color="actual_risk",
        size="avg_exam_score",
        title="Study vs Sleep"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sleep Categories vs Risk")

    sleep_cross = pd.crosstab(
        filtered_df['sleep_category'],
        filtered_df['actual_risk']
    )

    st.dataframe(sleep_cross)

# ===============================
# TAB 4: STUDENT EXPLORER
# ===============================
with tab4:
    st.header("Student Explorer")

    student_id = st.selectbox(
        "Select Student",
        filtered_df['student_id']
    )

    student = filtered_df[
        filtered_df['student_id'] == student_id
    ].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Academic")
        st.write(student[['attendance','exam1','exam2','exam3','exam4']])

    with col2:
        st.subheader("Behavioral")
        st.write(student[['study_hours_per_week','sleep_hours_per_night','engagement_score']])

# ===============================
# TAB 5: ML INSIGHTS
# ===============================
with tab5:
    st.header("Machine Learning Insights")

    if ml_df is None:
        st.warning("Run ML notebook first")
    else:
        df_ml = ml_df.copy()

        ml_filter = st.selectbox(
            "ML Risk Level",
            ["All"] + list(df_ml["ml_risk_level"].unique())
        )

        if ml_filter != "All":
            df_ml = df_ml[df_ml["ml_risk_level"] == ml_filter]

        col1, col2, col3 = st.columns(3)

        col1.metric("Predictions", len(df_ml))
        col2.metric("Accuracy",
            f"{((df_ml['actual_risk']==df_ml['ml_risk_level']).mean()*100):.2f}%")
        col3.metric("Avg Burnout",
            f"{df_ml['burnout_score'].mean():.2f}")

        st.divider()

        fig1 = px.histogram(df_ml, x="ml_risk_level", color="ml_risk_level")
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.histogram(df_ml, x="burnout_score")
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Confusion Matrix")

        cm = confusion_matrix(
            df_ml["actual_risk"],
            df_ml["ml_risk_level"]
        )

        fig3, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        st.pyplot(fig3)

        fig4 = px.scatter(
            df_ml,
            x="avg_exam_score",
            y="behavioral_risk_score",
            color="anomaly",
            title="Anomaly Detection"
        )
        st.plotly_chart(fig4, use_container_width=True)

        fig5 = px.scatter(
            df_ml,
            x="academic_risk_score",
            y="burnout_score",
            color="ml_risk_level"
        )
        st.plotly_chart(fig5, use_container_width=True)

        st.subheader("High Risk Students")
        st.dataframe(df_ml[df_ml["ml_risk_level"]=="High"].head(20))

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("AcademicPulse • DS + ML Student Risk Detection System 🚀")