import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

class HealthVisualizer:
    def __init__(self, health_records):
        self.df = pd.DataFrame(list(health_records.values()))
        
    def prepare_blood_pressure_data(self, records):
        """处理血压数据，分离收缩压和舒张压"""
        dates = []
        systolic = []  # 收缩压
        diastolic = []  # 舒张压
        
        for record in records:
            dates.append(record.date.strftime('%Y-%m-%d'))
            # 假设血压格式为 "120/80"
            if record.blood_pressure and '/' in record.blood_pressure:
                sys, dia = record.blood_pressure.split('/')
                systolic.append(int(sys))
                diastolic.append(int(dia))
            else:
                systolic.append(None)
                diastolic.append(None)
        
        return {
            'dates': dates,
            'systolic': systolic,
            'diastolic': diastolic
        }

    def get_health_data_charts(self, records):
        """生成所有健康数据图表"""
        bp_data = self.prepare_blood_pressure_data(records)
        
        blood_pressure_chart = {
            'title': '血压趋势',
            'labels': bp_data['dates'],
            'datasets': [
                {
                    'label': '收缩压',
                    'data': bp_data['systolic'],
                    'borderColor': 'rgb(255, 99, 132)',
                    'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                    'fill': False
                },
                {
                    'label': '舒张压',
                    'data': bp_data['diastolic'],
                    'borderColor': 'rgb(54, 162, 235)',
                    'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                    'fill': False
                }
            ]
        }
        
        # ... 其他图表的代码保持不变 ...
        
        return {
            'blood_pressure_chart': blood_pressure_chart,
            # ... 其他图表 ...
        }