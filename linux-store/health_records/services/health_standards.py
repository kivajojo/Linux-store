class HealthStandards:
    # 血压标准范围
    BLOOD_PRESSURE = {
        'normal': {'systolic': (90, 120), 'diastolic': (60, 80)},
        'pre_high': {'systolic': (120, 140), 'diastolic': (80, 90)},
        'high': {'systolic': (140, 999), 'diastolic': (90, 999)}
    }
    
    # 心率标准范围
    HEART_RATE = {
        'normal': (60, 100),
        'low': (0, 60),
        'high': (100, 999)
    }
    
    # 血糖标准范围
    BLOOD_SUGAR = {
        'fasting': {'normal': (3.9, 6.1), 'pre_high': (6.1, 7.0), 'high': (7.0, 999)},
        'after_meal': {'normal': (3.9, 7.8), 'pre_high': (7.8, 11.1), 'high': (11.1, 999)}
    }