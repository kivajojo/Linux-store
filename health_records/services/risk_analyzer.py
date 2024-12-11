class RiskAnalyzer:
    def __init__(self, records):
        self.records = records
        self.risks = []
        
    def analyze_blood_pressure_risks(self):
        """分析血压相关风险"""
        latest_records = self.records.order_by('-date')[:3]  # 获取最近3条记录
        high_pressure_count = 0
        low_pressure_count = 0
        
        for record in latest_records:
            if record.blood_pressure:
                systolic, diastolic = map(int, record.blood_pressure.split('/'))
                if systolic >= 140 or diastolic >= 90:
                    high_pressure_count += 1
                elif systolic < 90 or diastolic < 60:
                    low_pressure_count += 1
        
        if high_pressure_count >= 2:
            self.risks.append({
                'type': 'blood_pressure',
                'level': 'high',
                'description': '警告：最近血压偏高，建议及时就医检查',
                'recommendations': [
                    '控制饮食中的盐分摄入',
                    '保持规律运动',
                    '避免情绪激动',
                    '按时服用降压药物（如有医嘱）'
                ]
            })
        elif low_pressure_count >= 2:
            self.risks.append({
                'type': 'blood_pressure',
                'level': 'warning',
                'description': '注意：最近血压偏低，请注意观察',
                'recommendations': [
                    '适当增加盐分摄入',
                    '避免剧烈运动',
                    '注意补充水分'
                ]
            })
    
    def analyze_heart_rate_risks(self):
        """分析心率相关风险"""
        latest_records = self.records.order_by('-date')[:3]
        high_rate_count = 0
        low_rate_count = 0
        
        for record in latest_records:
            if record.heart_rate > 100:
                high_rate_count += 1
            elif record.heart_rate < 60:
                low_rate_count += 1
        
        if high_rate_count >= 2:
            self.risks.append({
                'type': 'heart_rate',
                'level': 'warning',
                'description': '注意：最近心率偏快，建议进一步检查',
                'recommendations': [
                    '保持心情平静',
                    '避免剧烈运动',
                    '限制咖啡因摄入'
                ]
            })
        elif low_rate_count >= 2:
            self.risks.append({
                'type': 'heart_rate',
                'level': 'warning',
                'description': '注意：最近心率偏慢，请注意观察',
                'recommendations': [
                    '适当进行有氧运动',
                    '保持充足睡眠',
                    '注意保暖'
                ]
            })
    
    def analyze_blood_sugar_risks(self):
        """分析血糖相关风险"""
        latest_records = self.records.order_by('-date')[:3]
        high_sugar_count = 0
        low_sugar_count = 0
        
        for record in latest_records:
            if record.blood_sugar > 7.0:
                high_sugar_count += 1
            elif record.blood_sugar < 3.9:
                low_sugar_count += 1
        
        if high_sugar_count >= 2:
            self.risks.append({
                'type': 'blood_sugar',
                'level': 'high',
                'description': '警告：最近血糖偏高，建议就医检查',
                'recommendations': [
                    '控制碳水化合物摄入',
                    '规律运动',
                    '按时服用降糖药物（如有医嘱）',
                    '定期监测血糖'
                ]
            })
        elif low_sugar_count >= 2:
            self.risks.append({
                'type': 'blood_sugar',
                'level': 'high',
                'description': '警告：最近血糖偏低，需要及时处理',
                'recommendations': [
                    '随身携带糖果',
                    '定时进食',
                    '避免空腹运动'
                ]
            })
    
    def get_overall_health_status(self):
        """获取整体健康状况评估"""
        self.analyze_blood_pressure_risks()
        self.analyze_heart_rate_risks()
        self.analyze_blood_sugar_risks()
        
        return {
            'risks': self.risks,
            'risk_level': 'high' if any(r['level'] == 'high' for r in self.risks) else 'warning' if self.risks else 'normal',
            'total_risks': len(self.risks)
        }