# src/data_preprocessing.py

import pandas as pd
import numpy as np
import random

def generate_student_data(n_students=500):
    """
    Generate synthetic student data with realistic patterns
    """
    np.random.seed(42)
    random.seed(42)
    
    data = []
    
    for student_id in range(1, n_students + 1):
        # Generate base student profile
        base_performance = np.random.normal(75, 10)
        
        # Academic features
        attendance = np.clip(np.random.normal(85, 15), 40, 100)
        
        # Exam scores over 4 exams
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
        
        # Behavioral features
        study_hours = np.clip(np.random.normal(20, 8), 5, 40)
        sleep_hours = np.clip(np.random.normal(7.5, 1.5), 4, 12)
        submission_delay = np.clip(np.random.exponential(1), 0, 7)
        engagement = np.clip(np.random.normal(7, 2), 1, 10)
        
        # Calculate risk factors
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
        
        # Determine risk level
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
    
    # Calculate derived features
    df['avg_exam_score'] = df[['exam1', 'exam2', 'exam3', 'exam4']].mean(axis=1)
    df['exam_volatility'] = df[['exam1', 'exam2', 'exam3', 'exam4']].std(axis=1)
    
    return df

# Generate and save data
if __name__ == "__main__":
    print("Generating student data...")
    df = generate_student_data(500)
    
    # Create data folder if it doesn't exist
    import os
    os.makedirs('data/raw', exist_ok=True)
    
    # Save to CSV
    output_path = 'data/raw/student_data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Data generated successfully! Saved to {output_path}")
    print(f"Shape: {df.shape}")
    print(f"\nFirst 5 rows:")
    print(df.head())
    print(f"\nRisk distribution:")
    print(df['actual_risk'].value_counts())