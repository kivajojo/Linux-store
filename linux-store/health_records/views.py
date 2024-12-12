from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import HealthRecord, Elderly
from .forms import HealthRecordForm, ElderlyForm
from django.db.models import Avg, Max, Min, Sum
from django.utils import timezone
from datetime import timedelta
from .services.health_analyzer import HealthAnalyzer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth import logout
from django.db.models.functions import TruncDate
from django.core.serializers.json import DjangoJSONEncoder
import json
from datetime import datetime
from django.urls import reverse
from .services.risk_analyzer import RiskAnalyzer

@login_required
def dashboard(request):
    """显示用户仪表盘"""
    try:
        records = HealthRecord.objects.filter(user=request.user).order_by('-date')[:5]  # 只获取最近5条记录
        context = {
            'records': records,
            'user': request.user,
        }
        return render(request, 'health_record/dashboard.html', context)
    except Exception as e:
        messages.error(request, f'获取记录失败：{str(e)}')
        return render(request, 'health_record/dashboard.html', {'records': []})

@login_required
def record_create(request, elderly_id):
    elderly = get_object_or_404(Elderly, id=elderly_id)
    
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.elderly = elderly
            record.created_by = request.user
            record.save()
            messages.success(request, '健康记录添加成功')
            return redirect('health_records:elderly_detail', elderly_id=elderly.id)
    else:
        form = HealthRecordForm()
    
    return render(request, 'health_record/record_form.html', {
        'form': form,
        'elderly': elderly,
        'title': f'为 {elderly.name} 添加健康记录',
	'record': None,
	'is_create': True
    })

@login_required
def record_detail(request, elderly_id, record_id):
    elderly = get_object_or_404(Elderly, id=elderly_id)
    record = get_object_or_404(HealthRecord, id=record_id, elderly=elderly)
    
    # 获取最近30天的记录
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    records = HealthRecord.objects.filter(
        elderly=elderly,
        date__range=[start_date, end_date]
    ).order_by('date')
    
    # 准备图表数据
    chart_data = {
        'dates': [],
        'blood_pressure': {
            'systolic': [],
            'diastolic': []
        },
        'heart_rate': [],
        'blood_sugar': [],
        'weight': []
    }
    
    # 处理血压数据和其他指标
    for r in records:
        chart_data['dates'].append(r.date.strftime('%Y-%m-%d'))
        
        # 处理血压数据
        if r.blood_pressure and '/' in r.blood_pressure:
            sys, dia = r.blood_pressure.split('/')
            chart_data['blood_pressure']['systolic'].append(int(sys))
            chart_data['blood_pressure']['diastolic'].append(int(dia))
        
        # 处理其他指标
        chart_data['heart_rate'].append(r.heart_rate)
        chart_data['blood_sugar'].append(float(r.blood_sugar))
        chart_data['weight'].append(float(r.weight))
    
    # 计算平均值等统计数据
    avg_systolic = sum(chart_data['blood_pressure']['systolic']) / len(chart_data['blood_pressure']['systolic']) if chart_data['blood_pressure']['systolic'] else 0
    avg_diastolic = sum(chart_data['blood_pressure']['diastolic']) / len(chart_data['blood_pressure']['diastolic']) if chart_data['blood_pressure']['diastolic'] else 0
    
    context = {
        'elderly': elderly,
        'record': record,
        'chart_data': json.dumps(chart_data),
        'blood_pressure_analysis': {
            'average_systolic': round(avg_systolic, 1),
            'average_diastolic': round(avg_diastolic, 1),
        }
    }
    
    # 添加风险分析
    risk_analyzer = RiskAnalyzer(records)
    health_status = risk_analyzer.get_overall_health_status()
    
    context.update({
        'health_status': health_status,
        'risks': health_status['risks'],
        'risk_level': health_status['risk_level']
    })
    
    return render(request, 'health_record/record_detail.html', context)

@login_required
def record_edit(request, record_id):
    record = get_object_or_404(HealthRecord, id=record_id, user=request.user)
    
    if request.method == 'POST':
        form = HealthRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, '健康记录已更新')
            return redirect('health_records:record_detail', record_id=record_id)
    else:
        form = HealthRecordForm(instance=record)
    
    return render(request, 'health_record/record_form.html', {
        'form': form,
        'record': record,
        'is_edit': True
    })

@login_required
def record_delete(request, record_id):
    """删除健康记录"""
    record = get_object_or_404(HealthRecord, id=record_id)
    elderly = record.elderly
    
    # 检查权限
    if elderly.created_by != request.user:
        messages.error(request, '您没有权限删除此记录')
        return redirect('health_records:elderly_detail', elderly_id=elderly.id)
    
    if request.method == 'POST':
        elderly_id = record.elderly.id  # 保存老人ID以便重定向
        record.delete()
        messages.success(request, '健康记录已删除')
        return redirect('health_records:elderly_detail', elderly_id=elderly_id)
    
    return redirect('health_records:record_detail', record_id=record_id)

@login_required
def statistics(request):
    records = HealthRecord.objects.filter(user=request.user).order_by('date')
    
    if not records.exists():
        return render(request, 'health_record/statistics.html', {
            'has_records': False
        })
    
    # 准备数据
    dates = [record.date.strftime('%Y-%m-%d') for record in records]
    
    # 处理血压数据（取收缩压）
    blood_pressures = [int(record.blood_pressure.split('/')[0]) for record in records]
    
    heart_rates = [record.heart_rate for record in records]
    blood_sugars = [float(record.blood_sugar) for record in records]
    weights = [float(record.weight) for record in records]
    
    context = {
        'has_records': True,
        'dates': json.dumps(dates),
        'blood_pressures': json.dumps(blood_pressures),
        'heart_rates': json.dumps(heart_rates),
        'blood_sugars': json.dumps(blood_sugars),
        'weights': json.dumps(weights),
    }
    
    return render(request, 'health_record/statistics.html', context)

@login_required
def record_update(request, elderly_id, record_id):
    elderly = get_object_or_404(Elderly, id=elderly_id)
    record = get_object_or_404(HealthRecord, id=record_id, elderly=elderly)
    
    if request.method == 'POST':
        form = HealthRecordForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save()
            messages.success(request, '健康记录更新成功')
            return redirect('health_records:record_detail', 
                          elderly_id=elderly.id, 
                          record_id=record.id)
    else:
        form = HealthRecordForm(instance=record)
    
    context = {
        'elderly': elderly,
        'record': record,
        'form': form,
        'is_update': True
    }
    return render(request, 'health_record/record_form.html', context)

@require_http_methods(["DELETE"])
def delete_health_record(request, record_id):
    try:
        record = HealthRecord.objects.get(id=record_id, user=request.user)
        record.delete()
        return JsonResponse({"message": "记录删除成功"}, status=200)
    except HealthRecord.DoesNotExist:
        return JsonResponse({"error": "记录不存在"}, status=404)

@login_required
def record_list(request):
    """显示健康记录列表"""
    records = HealthRecord.objects.filter(user=request.user).order_by('-date')
    return render(request, 'health_record/record_list.html', {
        'records': records
    })

@login_required
def record_detail(request, elderly_id, record_id):
    elderly = get_object_or_404(Elderly, id=elderly_id)
    record = get_object_or_404(HealthRecord, id=record_id, elderly=elderly)
    
    # 获取最近30天的记录
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    records = HealthRecord.objects.filter(
        elderly=elderly,
        date__range=[start_date, end_date]
    ).order_by('date')
    
    # 准备图表数据
    chart_data = {
        'dates': [],
        'blood_pressure': {
            'systolic': [],
            'diastolic': []
        },
        'heart_rate': [],
        'blood_sugar': [],
        'weight': []
    }
    
    # 处理血压数据和其他指标
    for r in records:
        chart_data['dates'].append(r.date.strftime('%Y-%m-%d'))
        
        # 处理血压数据
        if r.blood_pressure and '/' in r.blood_pressure:
            sys, dia = r.blood_pressure.split('/')
            chart_data['blood_pressure']['systolic'].append(int(sys))
            chart_data['blood_pressure']['diastolic'].append(int(dia))
        
        # 处理其他指标
        chart_data['heart_rate'].append(r.heart_rate)
        chart_data['blood_sugar'].append(float(r.blood_sugar))
        chart_data['weight'].append(float(r.weight))
    
    # 计算平均值等统计数据
    avg_systolic = sum(chart_data['blood_pressure']['systolic']) / len(chart_data['blood_pressure']['systolic']) if chart_data['blood_pressure']['systolic'] else 0
    avg_diastolic = sum(chart_data['blood_pressure']['diastolic']) / len(chart_data['blood_pressure']['diastolic']) if chart_data['blood_pressure']['diastolic'] else 0
    
    context = {
        'elderly': elderly,
        'record': record,
        'chart_data': json.dumps(chart_data),
        'blood_pressure_analysis': {
            'average_systolic': round(avg_systolic, 1),
            'average_diastolic': round(avg_diastolic, 1),
        }
    }
    
    # 添加风险分析
    risk_analyzer = RiskAnalyzer(records)
    health_status = risk_analyzer.get_overall_health_status()
    
    context.update({
        'health_status': health_status,
        'risks': health_status['risks'],
        'risk_level': health_status['risk_level']
    })
    
    return render(request, 'health_record/record_detail.html', context)

@login_required
@require_POST
def delete_record(request, elderly_id, record_id):
    elderly = get_object_or_404(Elderly, id=elderly_id)
    record = get_object_or_404(HealthRecord, id=record_id, elderly=elderly)
    
    try:
        record.delete()
        messages.success(request, '记录删除成功')
    except Exception as e:
        messages.error(request, f'删除失败：{str(e)}')
    
    return redirect('health_records:elderly_detail', elderly_id=elderly_id)

@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    messages.success(request, '您已成功退出登录')
    return redirect('login')

@login_required
def profile_update(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.name = request.POST.get('name', '')
            user.phone = request.POST.get('phone', '')
            user.gender = request.POST.get('gender', '')
            
            birth_date = request.POST.get('birth_date')
            if birth_date:
                user.birth_date = birth_date
                
            user.emergency_contact = request.POST.get('emergency_contact', '')
            user.emergency_phone = request.POST.get('emergency_phone', '')
            user.medical_history = request.POST.get('medical_history', '')
            
            user.save()
            messages.success(request, '人信息更新成功')
            return redirect('health_records:dashboard')
        except Exception as e:
            messages.error(request, f'更新失败：{str(e)}')
    
    return render(request, 'health_record/profile_form.html', {
        'user': request.user
    })

@login_required
def elderly_list(request):
    """老年人列表图"""
    elderly_list = Elderly.objects.all()
    return render(request, 'health_record/elderly_list.html', {
        'elderly_list': elderly_list
    })

@login_required
def elderly_create(request):
    if request.method == 'POST':
        try:
            elderly = Elderly(
                name=request.POST['name'],
                gender=request.POST['gender'],
                birth_date=request.POST['birth_date'],
                phone=request.POST['phone'],
                address=request.POST['address'],
                emergency_contact=request.POST['emergency_contact'],
                emergency_phone=request.POST['emergency_phone'],
                medical_history=request.POST['medical_history'],
                created_by=request.user
            )
            elderly.save()
            messages.success(request, '老年人信息添加成功')
            return redirect('health_records:elderly_detail', elderly_id=elderly.id)
        except Exception as e:
            messages.error(request, f'添加失败：{str(e)}')
            return render(request, 'health_record/elderly_form.html')
    
    return render(request, 'health_record/elderly_form.html')

@login_required
def elderly_detail(request, elderly_id):
    """老年人详情"""
    elderly = get_object_or_404(Elderly, pk=elderly_id)
    records = HealthRecord.objects.filter(elderly=elderly).order_by('-date')
    
    return render(request, 'health_record/elderly_detail.html', {
        'elderly': elderly,
        'records': records
    })

@login_required
def elderly_update(request, elderly_id):
    elderly = get_object_or_404(Elderly, id=elderly_id)
    
    if request.method == 'POST':
        form = ElderlyForm(request.POST, instance=elderly)
        if form.is_valid():
            form.save()
            messages.success(request, '老人信息更新成功')
            return redirect('health_records:elderly_detail', elderly_id=elderly.id)
    else:
        # 初始化表单时传入 elderly 实例
        form = ElderlyForm(instance=elderly)
    
    return render(request, 'health_record/elderly_form.html', {
        'elderly': elderly,
        'form': form,
        'is_update': True
    })

@login_required
def update_recommendation(request, record_id):
    """更新健康记录的个性化建议"""
    record = get_object_or_404(HealthRecord, id=record_id)
    
    # 检查权限
    if record.elderly.created_by != request.user:
        messages.error(request, '您没有权限修改此记录')
        return redirect('health_records:record_detail', record_id=record.id)
    
    if request.method == 'POST':
        recommendation = request.POST.get('recommendation')
        record.recommendation = recommendation
        record.save()
        messages.success(request, '健康建议已更新')
    
    return redirect('health_records:record_detail', record_id=record.id)

@login_required
def health_analysis(request, elderly_id):
    elderly = get_object_or_404(Elderly, id=elderly_id)
    record = HealthRecord.objects.filter(elderly=elderly).latest('date')  # 获取最新记录
    
    context = {
        'elderly': elderly,
        'record': record,  # 确保里传递了 record
        # ... 其他上下文数据 ...
    }
    return render(request, 'health_record/analysis.html', context)

@login_required
def update_record(request, elderly_id, record_id):
    elderly = get_object_or_404(Elderly, id=elderly_id)
    record = get_object_or_404(HealthRecord, id=record_id, elderly=elderly)
    
    if request.method == 'POST':
        form = HealthRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, '健康记录更新成功')
            return redirect('health_records:elderly_detail', elderly_id=elderly_id)
    else:
        # 预填充表单数据
        initial_data = {
            'date': record.date,
            'blood_pressure': record.blood_pressure,
            'heart_rate': record.heart_rate,
            'blood_sugar': record.blood_sugar,
            'weight': record.weight,
            'activity_type': record.activity_type,
            'activity_duration': record.activity_duration,
            'sleep_duration': record.sleep_duration,
            'breakfast': record.breakfast,
            'lunch': record.lunch,
            'dinner': record.dinner,
            'water_intake': record.water_intake,
        }
        form = HealthRecordForm(initial=initial_data)
    
    return render(request, 'health_record/record_form.html', {
        'form': form,
        'elderly': elderly,
        'record': record,
        'is_update': True
    })
