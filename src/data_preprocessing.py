import pandas as pd
import numpy as np
import random
import os
from sklearn.model_selection import train_test_split

from src.config import DATA_PATH, TEST_SIZE, TARGET_COLUMN


def generate_student_data(n_students=500):
    np.random.seed(42)
    random.seed(42)
    
    data = []
    
    for student_id in range(1, n_students + 1):
        base_performance = np.random.normal(75, 10)
        
        attendance = np.clip(np.random.normal(85, 15), 40, 100)
        
        exam_scores = []
        trend = np.random.choice(['improving', 'declining', 'stable'], p=[0.3, 0.3, 0.4])
        
        for exam_num in range(1, 5):
            if trend == 'improving':
                score = base_performance + (exam_num * 2) + np.random.normal(0, 5)
            elif trend == 'declining':
                score = base_performance - (exam_num * 2) + np.random.normal(0, 5)
            else:
                score = base_performance + np.random.normal(0, 5)
            
            exam_scores.append(np.clip(score, 30, 100))
        
        study_hours = np.clip(np.random.normal(20, 8), 5, 40)
        sleep_hours = np.clip(np.random.normal(7.5, 1.5), 4, 12)
        submission_delay = np.clip(np.random.exponential(1), 0, 7)
        engagement = np.clip(np.random.normal(7, 2), 1, 10)
        
        risk_factors = 0
        if attendance < 70:
            risk_factors += 1
        if exam_scores[-1] < 60:
            risk_factors += 2
        if study_hours < 15:
            risk_factors += 1
        if sleep_hours < 6 or sleep_hours > 10:
            risk_factors += 1
        if submission_delay > 3:
            risk_factors += 1
        if engagement < 4:
            risk_factors += 2
        
        if risk_factors >= 4:
            risk_level = 'High'
        elif risk_factors >= 2:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        student = {
            'student_id': f'STU{student_id:04d}',
            'attendance': round(attendance, 1),
            'exam1': round(exam_scores[0], 1),
            'exam2': round(exam_scores[1], 1),
            'exam3': round(exam_scores[2], 1),
            'exam4': round(exam_scores[3], 1),
            'performance_trend': trend,
            'study_hours_per_week': round(study_hours, 1),
            'sleep_hours_per_night': round(sleep_hours, 1),
            'avg_assignment_delay_days': round(submission_delay, 1),
            'engagement_score': round(engagement, 1),
            'actual_risk': risk_level
        }
        
        data.append(student)
    
    df = pd.DataFrame(data)
    
    df['avg_exam_score'] = df[['exam1', 'exam2', 'exam3', 'exam4']].mean(axis=1)
    df['exam_volatility'] = df[['exam1', 'exam2', 'exam3', 'exam4']].std(axis=1)
    
    return df


def load_data():
    return pd.read_csv(DATA_PATH)


def clean_data(df):
    df = df.dropna()

    # Drop ID column (not useful for ML)
    if "student_id" in df.columns:
        df = df.drop("student_id", axis=1)

    return df


def split_data(df):
    X = df.drop(TARGET_COLUMN, axis=1)
    y = df[TARGET_COLUMN]

    return train_test_split(X, y, test_size=TEST_SIZE, random_state=42)


def generate_and_save():
    print("Generating student data...")
    
    df = generate_student_data(500)
    
    os.makedirs("data/raw", exist_ok=True)
    
    df.to_csv(DATA_PATH, index=False)
    
    print(f"Saved to {DATA_PATH}")
    print(df.head())
    print(df["actual_risk"].value_counts())


if __name__ == "__main__":
    generate_and_save()