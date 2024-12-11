import pandas as pd
import numpy as np
from scipy import stats

class HealthAnalyzer:
    def __init__(self, health_records):
        self.df = pd.DataFrame(list(health_records.values()))
        
    def analyze_blood_pressure(self):
        """分析血压趋势"""
        # 分离收缩压和舒张压
        self.df[['systolic', 'diastolic']] = self.df['blood_pressure'].str.split('/', expand=True).astype(float)
        
        trends = {
            'systolic_trend': self._calculate_trend(self.df['systolic']),
            'diastolic_trend': self._calculate_trend(self.df['diastolic']),
            'avg_systolic': self.df['systolic'].mean(),
            'avg_diastolic': self.df['diastolic'].mean(),
        }
        return trends
    
    def analyze_weight_trend(self):
        """分析体重趋势"""
        return {
            'trend': self._calculate_trend(self.df['weight']),
            'avg_weight': self.df['weight'].mean(),
            'weight_change': self.df['weight'].iloc[-1] - self.df['weight'].iloc[0]
        }
    
    def _calculate_trend(self, series):
        """计算趋势斜率"""
        x = np.arange(len(series))
        slope, _, _, _, _ = stats.linregress(x, series)
        return slope

    def calculate_risk_score(self):
        """计算健康风险评分"""
        risk_score = 0
        
        # 血压风险评估
        if self.df['systolic'].mean() > 140 or self.df['diastolic'].mean() > 90:
            risk_score += 2
            
        # 心率风险评估
        if self.df['heart_rate'].mean() > 100 or self.df['heart_rate'].mean() < 60:
            risk_score += 1
            
        # 血糖风险评估
        if self.df['blood_sugar'].mean() > 7:
            risk_score += 2
            
        return risk_score