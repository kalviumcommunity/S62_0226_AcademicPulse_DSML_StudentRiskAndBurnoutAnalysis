import numpy as np
import pandas as pd
import joblib

from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class StudentRiskDetector:
    def __init__(self, n_clusters=3, contamination=0.1):
        self.n_clusters = n_clusters
        self.contamination = contamination

        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.isolation_forest = IsolationForest(
            contamination=contamination, random_state=42
        )

        self.feature_cols = None
        self.cluster_risk_map = {}

    def fit(self, df: pd.DataFrame):
        self.feature_cols = [
            "avg_exam_score",
            "exam_volatility",
            "exam_trend",
            "attendance",
            "study_hours_per_week",
            "sleep_hours_per_night",
            "avg_assignment_delay_days",
            "engagement_score",
            "behavioral_risk_score",
        ]

        X = df[self.feature_cols]
        X_scaled = self.scaler.fit_transform(X)

        clusters = self.kmeans.fit_predict(X_scaled)
        self.isolation_forest.fit(X_scaled)

        df["cluster"] = clusters
        self._map_clusters(df)

    def _map_clusters(self, df):
        cluster_summary = df.groupby("cluster")[
            ["avg_exam_score", "behavioral_risk_score"]
        ].mean()

        cluster_summary["risk_score"] = (
            -cluster_summary["avg_exam_score"]
            + cluster_summary["behavioral_risk_score"] * 10
        )

        sorted_clusters = cluster_summary.sort_values("risk_score").index.tolist()
        labels = ["Low", "Medium", "High"]

        for i, cluster in enumerate(sorted_clusters):
            self.cluster_risk_map[cluster] = labels[i]

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        X = df[self.feature_cols]
        X_scaled = self.scaler.transform(X)

        df = df.copy()

        df["cluster"] = self.kmeans.predict(X_scaled)
        df["ml_risk_level"] = df["cluster"].map(self.cluster_risk_map)

        distances = self.kmeans.transform(X_scaled)
        min_dist = distances.min(axis=1)

        df["burnout_score"] = 100 * (min_dist / min_dist.max())

        df["academic_risk_score"] = (
            (100 - df["avg_exam_score"]) * 0.6
            + df["behavioral_risk_score"] * 8
        )

        df["anomaly"] = self.isolation_forest.predict(X_scaled)
        df["anomaly"] = df["anomaly"].map({1: 0, -1: 1})

        return df

    def save_model(self, path: str):
        joblib.dump(self, path)

    @staticmethod
    def load_model(path: str):
        return joblib.load(path)