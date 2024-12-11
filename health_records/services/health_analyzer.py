from datetime import datetime, timedelta
import numpy as np
from scipy import stats
from .health_standards import HealthStandards

class HealthAnalyzer:
    def __init__(self, records):
        self.records = list(records)  # 确保转换为列表
        self.standards = HealthStandards()
        # 添加调试信息
        print(f"初始化分析器，获取到 {len(self.records)} 条记录")
        
    def has_sufficient_data(self):
        """检查是否有足够的数据进行分析"""
        return len(self.records) >= 2  # 降低到只需要2条记录即可分析
        
    def analyze_blood_pressure_trend(self):
        """分析血压趋势"""
        if not self.has_sufficient_data():
            print("数据不足，无法分析")  # 添加调试信息
            return {
                'average_systolic': 0,
                'average_diastolic': 0,
                'trend': 'insufficient_data',
                'message': f'当前仅有 {len(self.records)} 条记录，至少需要2条记录才能进行分析'
            }
            
        # 数据处理
        try:
            blood_pressures = [r.blood_pressure.split('/') for r in self.records]
            systolic = [int(bp[0]) for bp in blood_pressures]
            diastolic = [int(bp[1]) for bp in blood_pressures]
            
            print(f"处理血压数据：收缩压 {systolic}，舒张压 {diastolic}")  # 调试信息
            
            return {
                'average_systolic': sum(systolic) / len(systolic),
                'average_diastolic': sum(diastolic) / len(diastolic),
                'trend': 'up' if systolic[-1] > systolic[0] else 'down',
                'message': '数据分析完成'
            }
        except Exception as e:
            print(f"数据处理出错：{str(e)}")  # 错误信息
            return {
                'error': f'数据处理出错：{str(e)}'
            }
    
    def _assess_blood_pressure_risks(self, systolic, diastolic):
        """评估血压风险"""
        risks = []
        avg_systolic = sum(systolic) / len(systolic)
        avg_diastolic = sum(diastolic) / len(diastolic)
        
        if avg_systolic > self.standards.BLOOD_PRESSURE['high']['systolic'][0]:
            risks.append("收缩压偏高，请注意监测")
        if avg_diastolic > self.standards.BLOOD_PRESSURE['high']['diastolic'][0]:
            risks.append("舒张压偏高，请注意监测")
        
        return risks or ["血压指标在正常范围内"]
    
    def _generate_bp_recommendations(self, systolic, diastolic):
        """生成血压相关建议"""
        recommendations = ["保持规律测量血压的好习惯"]
        
        if max(systolic) > self.standards.BLOOD_PRESSURE['high']['systolic'][0]:
            recommendations.extend([
                "控制饮食盐分摄入",
                "适量运动，避免剧烈运动",
                "保持心情愉悦，避免情绪波动"
            ])
            
        return recommendations
    
    def generate_comprehensive_analysis(self):
        """生成综合分析报告"""
        bp_analysis = self.analyze_blood_pressure_trend()
        hr_analysis = self.analyze_heart_rate_trend()
        bs_analysis = self.analyze_blood_sugar_trend()
        
        return {
            'blood_pressure': bp_analysis,
            'heart_rate': hr_analysis,
            'blood_sugar': bs_analysis,
            'overall_risks': self.identify_overall_risks(),
            'lifestyle_recommendations': self.generate_lifestyle_recommendations()
        }
    
    def generate_health_insights(self):
        """生成健康洞察报告"""
        return {
            'blood_pressure': self._analyze_blood_pressure_details(),
            'heart_rate': self._analyze_heart_rate_details(),
            'blood_sugar': self._analyze_blood_sugar_details(),
            'weight': self._analyze_weight_details(),
            'overall_health': self._generate_overall_health_assessment()
        }
        
    def _analyze_blood_pressure_details(self):
        """详细分析血压数据"""
        systolic_values = [int(r.blood_pressure.split('/')[0]) for r in self.records]
        diastolic_values = [int(r.blood_pressure.split('/')[1]) for r in self.records]
        
        return {
            'average_systolic': sum(systolic_values) / len(systolic_values),
            'average_diastolic': sum(diastolic_values) / len(diastolic_values),
            'max_systolic': max(systolic_values),
            'min_systolic': min(systolic_values),
            'trend': self._calculate_trend(systolic_values),
            'risk_level': self._assess_blood_pressure_risk(systolic_values, diastolic_values)
        }
