import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.test_suite import TestSuite
from evidently.test_preset import DataStabilityTestPreset
import json
import os
from datetime import datetime

class ModelMonitor:
    def __init__(self):
        self.reference_data_path = "data/processed/aqi_features.csv"
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def load_reference_data(self):
        if os.path.exists(self.reference_data_path):
            return pd.read_csv(self.reference_data_path)
        return None
        
    def generate_data_drift_report(self, current_data: pd.DataFrame):
        """Generate data drift report comparing current batch with reference"""
        reference_data = self.load_reference_data()
        
        if reference_data is None:
            print("Reference data not found. Skipping drift check.")
            return
            
        # Select numerical columns for drift check
        numerical_features = [
            'pm2_5', 'pm10', 'no2', 'so2', 'o3', 'co',
            'health_risk_score'
        ]
        
        report = Report(metrics=[
            DataDriftPreset(), 
        ])
        
        report.run(
            reference_data=reference_data[numerical_features].sample(n=min(1000, len(reference_data))), 
            current_data=current_data[numerical_features]
        )
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.reports_dir, f"drift_report_{timestamp}.html")
        report.save_html(report_path)
        
        print(f"✅ Data drift report saved to: {report_path}")
        
    def run_tests(self, current_data: pd.DataFrame):
        """Run stability tests"""
        tests = TestSuite(tests=[
            DataStabilityTestPreset(),
        ])
        
        tests.run(reference_data=None, current_data=current_data)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_path = os.path.join(self.reports_dir, f"data_stability_{timestamp}.html")
        tests.save_html(test_path)
        
        print(f"✅ Data stability tests saved to: {test_path}")

if __name__ == "__main__":
    # Example usage with generated data
    monitor = ModelMonitor()
    
    # Simulate new incoming data
    try:
        current_data = pd.read_csv("data/raw/aqi_data.csv").tail(100)
        monitor.generate_data_drift_report(current_data)
        monitor.run_tests(current_data)
    except Exception as e:
        print(f"Error running monitoring: {e}")
