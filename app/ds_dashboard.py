# app/ds_dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Page configuration
st.set_page_config(
    page_title="AcademicPulse",
    page_icon="📊",
    layout="wide"
)

# Title - simplified
st.title("AcademicPulse")
st.markdown("Student Risk Detection Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/raw/student_data.csv')
    df['avg_exam_score'] = df[['exam1', 'exam2', 'exam3', 'exam4']].mean(axis=1)
    df['exam_trend'] = df['exam4'] - df['exam1']
    df['sleep_category'] = pd.cut(df['sleep_hours_per_night'], 
                                  bins=[0, 6, 8, 12], 
                                  labels=['Insufficient', 'Healthy', 'Excessive'])
    df['study_category'] = pd.cut(df['study_hours_per_week'],
                                  bins=[0, 10, 20, 40],
                                  labels=['Low', 'Moderate', 'High'])
    return df

try:
    df = load_data()
    st.sidebar.success("Data loaded successfully")
except:
    st.error("Please generate data first using: python src/data_preprocessing.py")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")

risk_filter = st.sidebar.multiselect(
    "Risk Level",
    options=['Low', 'Medium', 'High'],
    default=['Low', 'Medium', 'High']
)

trend_filter = st.sidebar.multiselect(
    "Performance Trend",
    options=['improving', 'declining', 'stable'],
    default=['improving', 'declining', 'stable']
)

filtered_df = df[df['actual_risk'].isin(risk_filter) & 
                 df['performance_trend'].isin(trend_filter)]

# Main dashboard - simplified tab names
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Academic Analysis",
    "Behavioral Analysis", 
    "Student Explorer"
])

with tab1:
    st.header("Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", len(filtered_df))
    
    with col2:
        low = len(filtered_df[filtered_df['actual_risk']=='Low'])
        med = len(filtered_df[filtered_df['actual_risk']=='Medium'])
        high = len(filtered_df[filtered_df['actual_risk']=='High'])
        st.metric("Risk Distribution", f"{low} L / {med} M / {high} H")
    
    with col3:
        st.metric("Avg Attendance", f"{filtered_df['attendance'].mean():.1f}%")
    
    with col4:
        st.metric("Avg Exam Score", f"{filtered_df['avg_exam_score'].mean():.1f}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        risk_counts = filtered_df['actual_risk'].value_counts().reset_index()
        risk_counts.columns = ['Risk Level', 'Count']
        fig = px.pie(risk_counts, values='Count', names='Risk Level',
                    title='Student Risk Distribution',
                    color='Risk Level',
                    color_discrete_map={'Low':'green', 'Medium':'orange', 'High':'red'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        trend_counts = filtered_df['performance_trend'].value_counts().reset_index()
        trend_counts.columns = ['Trend', 'Count']
        fig = px.bar(trend_counts, x='Trend', y='Count',
                    title='Performance Trends',
                    color='Trend',
                    color_discrete_map={'improving':'green', 'stable':'blue', 'declining':'red'})
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Summary Statistics")
    stats_df = filtered_df[['attendance', 'avg_exam_score', 'study_hours_per_week',
                           'sleep_hours_per_night', 'engagement_score']].describe()
    st.dataframe(stats_df)

with tab2:
    st.header("Academic Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.box(filtered_df, x='actual_risk', y='attendance',
                    title='Attendance Distribution by Risk Level',
                    color='actual_risk',
                    color_discrete_map={'Low':'green', 'Medium':'orange', 'High':'red'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(filtered_df, x='actual_risk', y='avg_exam_score',
                    title='Exam Score Distribution by Risk Level',
                    color='actual_risk',
                    color_discrete_map={'Low':'green', 'Medium':'orange', 'High':'red'})
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Performance Trends Across Exams")
    exam_columns = ['exam1', 'exam2', 'exam3', 'exam4']
    exam_means = filtered_df.groupby('actual_risk')[exam_columns].mean().reset_index()
    
    fig = go.Figure()
    for risk in ['Low', 'Medium', 'High']:
        risk_data = exam_means[exam_means['actual_risk'] == risk]
        if not risk_data.empty:
            fig.add_trace(go.Scatter(
                x=['Exam 1', 'Exam 2', 'Exam 3', 'Exam 4'],
                y=[risk_data['exam1'].values[0], 
                   risk_data['exam2'].values[0],
                   risk_data['exam3'].values[0], 
                   risk_data['exam4'].values[0]],
                mode='lines+markers',
                name=f'{risk} Risk',
                line=dict(color={'Low':'green', 'Medium':'orange', 'High':'red'}[risk])
            ))
    
    fig.update_layout(title='Exam Score Trends by Risk Level',
                     xaxis_title='Exams',
                     yaxis_title='Average Score')
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Correlation Matrix")
    numeric_cols = ['attendance', 'exam1', 'exam2', 'exam3', 'exam4', 
                   'study_hours_per_week', 'sleep_hours_per_night', 
                   'engagement_score']
    corr = filtered_df[numeric_cols].corr()
    
    fig = px.imshow(corr, text_auto=True, aspect="auto",
                   title="Feature Correlations",
                   color_continuous_scale='RdBu_r')
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Behavioral Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.box(filtered_df, x='actual_risk', y='study_hours_per_week',
                    title='Study Hours by Risk Level',
                    color='actual_risk',
                    color_discrete_map={'Low':'green', 'Medium':'orange', 'High':'red'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(filtered_df, x='actual_risk', y='sleep_hours_per_night',
                    title='Sleep Hours by Risk Level',
                    color='actual_risk',
                    color_discrete_map={'Low':'green', 'Medium':'orange', 'High':'red'})
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.box(filtered_df, x='actual_risk', y='engagement_score',
                    title='Engagement Score by Risk Level',
                    color='actual_risk',
                    color_discrete_map={'Low':'green', 'Medium':'orange', 'High':'red'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(filtered_df, x='actual_risk', y='avg_assignment_delay_days',
                    title='Assignment Delay by Risk Level',
                    color='actual_risk',
                    color_discrete_map={'Low':'green', 'Medium':'orange', 'High':'red'})
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Study Hours vs Sleep Hours")
    fig = px.scatter(filtered_df, x='study_hours_per_week', y='sleep_hours_per_night',
                    color='actual_risk', size='avg_exam_score',
                    hover_data=['student_id'],
                    title='Study vs Sleep Patterns',
                    color_discrete_map={'Low':'green', 'Medium':'orange', 'High':'red'})
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Sleep Patterns Analysis")
    sleep_risk = pd.crosstab(filtered_df['sleep_category'], filtered_df['actual_risk'])
    fig = px.bar(sleep_risk, title='Risk Distribution by Sleep Category',
                barmode='group',
                color_discrete_map={'Low':'green', 'Medium':'orange', 'High':'red'})
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("Student Explorer")
    
    student_id = st.selectbox("Select Student ID", filtered_df['student_id'].tolist())
    
    if student_id:
        student = filtered_df[filtered_df['student_id'] == student_id].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk_color = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}[student['actual_risk']]
            st.markdown(f"### Risk Level")
            st.markdown(f"<h2 style='color:{risk_color};'>{student['actual_risk']}</h2>", 
                       unsafe_allow_html=True)
        
        with col2:
            trend_color = {'improving': 'green', 'stable': 'blue', 'declining': 'red'}[student['performance_trend']]
            st.markdown(f"### Performance Trend")
            st.markdown(f"<h2 style='color:{trend_color};'>{student['performance_trend']}</h2>", 
                       unsafe_allow_html=True)
        
        with col3:
            st.markdown("### Avg Exam Score")
            st.markdown(f"<h2>{student['avg_exam_score']:.1f}</h2>", 
                       unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Academic Details")
            st.write(f"Attendance: {student['attendance']}%")
            st.write(f"Exam 1: {student['exam1']:.1f}")
            st.write(f"Exam 2: {student['exam2']:.1f}")
            st.write(f"Exam 3: {student['exam3']:.1f}")
            st.write(f"Exam 4: {student['exam4']:.1f}")
            st.write(f"Trend: {student['performance_trend']}")
        
        with col2:
            st.subheader("Behavioral Details")
            st.write(f"Study Hours: {student['study_hours_per_week']}/week")
            st.write(f"Sleep Hours: {student['sleep_hours_per_night']}/night")
            st.write(f"Assignment Delay: {student['avg_assignment_delay_days']} days")
            st.write(f"Engagement: {student['engagement_score']}/10")
        
        st.subheader("Risk Factors")
        factors = []
        if student['attendance'] < 70:
            factors.append("Low attendance")
        if student['avg_exam_score'] < 65:
            factors.append("Low academic performance")
        if student['performance_trend'] == 'declining':
            factors.append("Declining performance")
        if student['study_hours_per_week'] < 15:
            factors.append("Low study hours")
        if student['sleep_hours_per_night'] < 6 or student['sleep_hours_per_night'] > 10:
            factors.append("Irregular sleep")
        if student['avg_assignment_delay_days'] > 3:
            factors.append("Assignment delays")
        if student['engagement_score'] < 5:
            factors.append("Low engagement")
        
        if factors:
            for f in factors:
                st.write(f"• {f}")
        else:
            st.write("No major risk factors detected")

st.markdown("---")
st.markdown("AcademicPulse - Student Risk Detection Dashboard")