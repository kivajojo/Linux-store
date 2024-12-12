from django import forms
from .models import Elderly, HealthRecord

class ElderlyForm(forms.ModelForm):
    class Meta:
        model = Elderly
        fields = ['name', 'gender', 'birth_date', 'phone', 'address', 
                 'medical_history', 'emergency_contact', 'emergency_phone']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
        }

class HealthRecordForm(forms.ModelForm):
    ACTIVITY_LEVELS = [
        ('低', '低强度'),
        ('中', '中等强度'),
        ('高', '高强度'),
    ]

    activity_level = forms.ChoiceField(choices=ACTIVITY_LEVELS, required=False)

    class Meta:
        model = HealthRecord
        exclude = ['elderly', 'created_by', 'created_at', 'updated_at']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'blood_pressure': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例如：120/80'
            }),
            'heart_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '40',
                'max': '200'
            }),
            'blood_sugar': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1'
            }),
            'activity_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例如：散步、太极拳'
            }),
            'activity_duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'sleep_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.5'
            }),
            'breakfast': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请描述早餐内容'
            }),
            'lunch': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请描述午餐内容'
            }),
            'dinner': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请描述晚餐内容'
            }),
            'water_intake': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1'
            }),
        }