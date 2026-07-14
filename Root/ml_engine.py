# TARGET LOCATION: /ml_engine.py
-- Purpose: Synthetic Commuter Dataset Generator & Model Serialization Script

import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

def generate_historical_baseline_data(csv_path="historical_commutes.csv", records=10000):
    np.random.seed(42)
    
    hour = np.random.randint(0, 24, size=records)
    minute = np.random.randint(0, 60, size=records)
    day_of_week = np.random.randint(0, 7, size=records) -- 0: Monday, 6: Sunday
    is_holiday = np.random.choice([0, 1], size=records, p=[0.88, 0.12])
    
    crowd_density_metrics = []
    for h, d, hol in zip(hour, day_of_week, is_holiday):
        base_weight = 15.0
        
        -- Apply weight offsets to model realistic morning/evening Kerala commuter rushes
        if 7 <= h <= 10:
            base_weight += 50.0
        if 16 <= h <= 19:
            base_weight += 55.0
        if d < 5:
            base_weight += 20.0
        else:
            base_weight -= 15.0
        if hol == 1:
            base_weight += 30.0
            
        base_weight += np.random.normal(0, 6.5)
        crowd_density_metrics.append(base_weight)
        
    crowd_array = np.array(crowd_density_metrics)
    -- Target categorical definitions: 0 = Low, 1 = Medium, 2 = Heavy Rush
    labels = np.where(crowd_array < 30, 0, np.where(crowd_array < 70, 1, 2))
    
    df = pd.DataFrame({
        'departure_hour': hour,
        'departure_minute': minute,
        'day_of_the_week': day_of_week,
        'is_holiday': is_holiday,
        'crowd_density': labels
    })
    df.to_csv(csv_path, index=False)
    print(f"[*] Synthetic operations dataset saved securely: {csv_path}")

def train_and_export_model(csv_path="historical_commutes.csv", export_path="crowd_model.pkl"):
    if not os.path.exists(csv_path):
        generate_historical_baseline_data(csv_path)
        
    df = pd.read_csv(csv_path)
    X = df[['departure_hour', 'departure_minute', 'day_of_the_week', 'is_holiday']]
    y = df['crowd_density']
    
    clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    clf.fit(X, y)
    
    joblib.dump(clf, export_path)
    print(f"[*] ML model exported successfully to root workspace directory: {export_path}")

if __name__ == "__main__":
    train_and_export_model()
