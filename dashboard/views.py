# dashboard/views.py
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from .models import (
    Employee, Department, Position, EducationLevel,
    Product, Customer, Sale, Branch
)
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth,Coalesce
from django.utils import timezone
from datetime import timedelta
from django.db.models import Value 
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from .models import CountryEconomicData  # Assuming you have a model for country reports

def home(request):
    # Total number of employees
    total_employees = Employee.objects.filter(status='Active').count()

    # Number of left persons, total hiring, retention rate, leave rate
    total_hired = Employee.objects.count()
    total_left = Employee.objects.filter(status='Left').count()
    retention_rate = (total_employees / total_hired) * 100 if total_hired > 0 else 0
    leave_rate = (total_left / total_hired) * 100 if total_hired > 0 else 0

    # Education levels distribution
    education_distribution = Employee.objects.values('education_level__level').annotate(count=Count('id'))

    # Employees per department
    employees_per_department = Employee.objects.values('department__name').annotate(count=Count('id'))

    # Total salary per department
    salary_per_department = Employee.objects.values('department__name').annotate(total_salary=Sum('salary'))
    # Convert total_salary to float
    salary_per_department = list(salary_per_department)
    for item in salary_per_department:
        item['total_salary'] = float(item['total_salary']) if item['total_salary'] else 0.0

    # Gender diversity
    gender_distribution = Employee.objects.values('gender').annotate(count=Count('id'))

    # Payments per male/female
    salary_per_gender = Employee.objects.values('gender').annotate(total_salary=Sum('salary'))
    # Convert total_salary to float
    salary_per_gender = list(salary_per_gender)
    for item in salary_per_gender:
        item['total_salary'] = float(item['total_salary']) if item['total_salary'] else 0.0

    # Age distribution for age pyramid
    age_bins = [(20, 30), (31, 40), (41, 50), (51, 60)]
    age_distribution = []
    for age_range in age_bins:
        male_count = Employee.objects.filter(
            age__gte=age_range[0], age__lte=age_range[1], gender='M'
        ).count()
        female_count = Employee.objects.filter(
            age__gte=age_range[0], age__lte=age_range[1], gender='F'
        ).count()
        age_distribution.append({
            'age_range': f'{age_range[0]}-{age_range[1]}',
            'male': male_count,
            'female': female_count
        })

    # Position distribution
    position_distribution = Employee.objects.values('position__level').annotate(count=Count('id'))

    context = {
        'total_employees': total_employees,
        'total_hired': total_hired,
        'total_left': total_left,
        'retention_rate': retention_rate,
        'leave_rate': leave_rate,
        'education_distribution': list(education_distribution),
        'employees_per_department': list(employees_per_department),
        'salary_per_department': salary_per_department,
        'gender_distribution': list(gender_distribution),
        'salary_per_gender': salary_per_gender,
        'age_distribution': age_distribution,
        'position_distribution': list(position_distribution),
    }
    
    return render(request, 'dashboard/home.html', context)

from collections import defaultdict

from django.db.models.functions import TruncWeek, TruncMonth, Coalesce
from django.db.models import Sum, Value
from django.shortcuts import render
from .models import Sale  # Assuming Sale is your model


from django.db.models import Count

def sales_statistics(request):
    # Total sales
    total_sales = Sale.objects.aggregate(
        total_revenue=Sum('total_price')
    )['total_revenue'] or 0
    total_sales = float(total_sales)

    # Sales by product
    sales_by_product = Sale.objects.values('product__name').annotate(
        total=Sum('total_price')
    )
    sales_by_product = list(sales_by_product)
    for item in sales_by_product:
        item['total'] = float(item['total'])

    # Sales by category
    sales_by_category = Sale.objects.values('product__category').annotate(
        total=Sum('total_price')
    )
    sales_by_category = list(sales_by_category)
    for item in sales_by_category:
        item['total'] = float(item['total'])

    # Sales over time (monthly)
    sales_over_time = Sale.objects.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total=Sum('total_price')
    ).order_by('month')

    sales_over_time_formatted = []
    for item in sales_over_time:
        month = item['month']
        formatted_month = month.isoformat() if month else ''
        sales_over_time_formatted.append({
            'month': formatted_month,
            'total': float(item['total'])
        })

    # Sales per Branch
    sales_per_branch = Sale.objects.annotate(
        branch_name=Coalesce('branch__name', Value('نامشخص'))
    ).values('branch_name').annotate(
        total=Sum('total_price')
    ).order_by('branch_name')
    sales_per_branch = list(sales_per_branch)
    for item in sales_per_branch:
        item['total'] = float(item['total'])

    # Sales per Branch Weekly
    sales_per_branch_weekly = Sale.objects.annotate(
        week=TruncWeek('date'),
        branch_name=Coalesce('branch__name', Value('نامشخص'))
    ).values('week', 'branch_name').annotate(
        total=Sum('total_price')
    ).order_by('week', 'branch_name')

    sales_per_branch_weekly_formatted = []
    for item in sales_per_branch_weekly:
        week = item['week']
        formatted_week = week.isoformat() if week else ''
        sales_per_branch_weekly_formatted.append({
            'week': formatted_week,
            'branch_name': item['branch_name'],
            'total': float(item['total'])
        })

    # Sales per Branch Monthly
    sales_per_branch_monthly = Sale.objects.annotate(
        month=TruncMonth('date'),
        branch_name=Coalesce('branch__name', Value('نامشخص'))
    ).values('month', 'branch_name').annotate(
        total=Sum('total_price')
    ).order_by('month', 'branch_name')

    sales_per_branch_monthly_formatted = []
    for item in sales_per_branch_monthly:
        month = item['month']
        formatted_month = month.isoformat() if month else ''
        sales_per_branch_monthly_formatted.append({
            'month': formatted_month,
            'branch_name': item['branch_name'],
            'total': float(item['total'])
        })

    # Timeline Sales Data
    timeline_sales_data = Sale.objects.annotate(
        timeline_date=TruncMonth('date')  # You can adjust this to TruncDay or TruncWeek if needed
    ).values('timeline_date').annotate(
        total=Sum('total_price')
    ).order_by('timeline_date')

    timeline_sales_data_formatted = []
    for item in timeline_sales_data:
        date = item['timeline_date']
        formatted_date = date.isoformat() if date else ''
        timeline_sales_data_formatted.append({
            'timeline_date': formatted_date,
            'total': float(item['total'])
        })

    # Sales per country (geographical distribution by sales)
    sales_per_country = Sale.objects.values('customer__country').annotate(
        total=Sum('total_price')
    ).order_by('customer__country')

    sales_per_country_formatted = []
    for item in sales_per_country:
        sales_per_country_formatted.append({
            'country': item['customer__country'],
            'total': float(item['total'])
        })

    # Number of customers per country
    customers_per_country = Customer.objects.values('country').annotate(
        count=Count('id')
    ).order_by('country')

    customers_per_country_formatted = []
    for item in customers_per_country:
        customers_per_country_formatted.append({
            'country': item['country'],
            'count': item['count']
        })

    context = {
        'total_sales': total_sales,
        'sales_by_product': sales_by_product,
        'sales_by_category': sales_by_category,
        'sales_over_time': sales_over_time_formatted,
        'sales_per_branch': sales_per_branch,
        'sales_per_branch_weekly': sales_per_branch_weekly_formatted,
        'sales_per_branch_monthly': sales_per_branch_monthly_formatted,
        'timeline_sales_data': timeline_sales_data_formatted,
        'sales_per_country': sales_per_country_formatted,
        'customers_per_country': customers_per_country_formatted,
    }

    return render(request, 'dashboard/sales_statistics.html', context)

def marketing_statistics(request):
    # Placeholder view for Marketing Statistics
    return render(request, 'dashboard/marketing_statistics.html')

def geographical_report(request):
    countries = CountryEconomicData.objects.all()
    context = {
        'countries': {country.country_name: {
            'name': country.country_name,
            'population': country.population,
            'gdp': str(country.gdp),  # Convert Decimal to string for JSON
            'annual_gdp_growth': str(country.annual_gdp_growth),
            'life_expectancy': country.life_expectancy,
            'report_pdf': country.report_pdf.url if country.report_pdf else None
        } for country in countries}
    }
    return render(request, 'dashboard/geographical_report.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Category, Material

def material_categories(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/material_categories.html', {'categories': categories})

def category_materials(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    materials = category.materials.all()
    return render(request, 'dashboard/category_materials.html', {'category': category, 'materials': materials})

def material_detail(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    documents = material.documents.all()
    return render(request, 'dashboard/material_detail.html', {'material': material, 'documents': documents})


from django.shortcuts import render, get_object_or_404
from .models import TrainingCourse, TrainingSession

# View to list all training courses
def training_courses(request):
    courses = TrainingCourse.objects.all()
    return render(request, 'dashboard/training_courses.html', {'courses': courses})

# View to show details of a single course and its sessions
def course_detail(request, course_id):
    course = get_object_or_404(TrainingCourse, id=course_id)
    sessions = course.sessions.all()
    return render(request, 'dashboard/course_detail.html', {'course': course, 'sessions': sessions})

# View to show details of a specific session and its content
def session_detail(request, session_id):
    session = get_object_or_404(TrainingSession, id=session_id)
    return render(request, 'dashboard/session_detail.html', {'session': session})
from .models import OrganizationalInfo

def organizational_info(request):
    files = OrganizationalInfo.objects.all()  # Fetch all organizational info files
    return render(request, 'dashboard/organizational-info.html', {'files': files})


def exhibition_calendar(request):
    return render(request, 'dashboard/exhibition_calendar.html')

def latest_news(request):
    return render(request, 'dashboard/latest_news.html')

def latest_analyses(request):
    return render(request, 'dashboard/latest_analyses.html')

def reports(request):
    return render(request, 'dashboard/reports.html')
from django.shortcuts import render
from .models import ExhibitionEvent
import json
from django.utils.safestring import mark_safe

from .models import ExhibitionEvent
import json
from django.utils.safestring import mark_safe

from django.shortcuts import render
from .models import ExhibitionEvent
import calendar
from collections import defaultdict
from django.utils import timezone

from collections import defaultdict
from django.shortcuts import render
import calendar

from collections import defaultdict

from collections import defaultdict
from django.shortcuts import render
import calendar
from datetime import datetime

from django.shortcuts import render
import calendar
from .models import ExhibitionEvent

def exhibition_calendar(request):
    events = ExhibitionEvent.objects.all()

    # Define Persian month names
    persian_month_names = [
        'ژانویه', 'فوریه', 'مارس', 'آوریل',
        'مه', 'ژوئن', 'ژوئیه', 'اوت',
        'سپتامبر', 'اکتبر', 'نوامبر', 'دسامبر'
    ]

    # Initialize a regular dict with all months
    events_by_month = {month: [] for month in persian_month_names}

    # Assign events to the correct month
    for event in events:
        month_index = event.event_date.month - 1  # 0-based index
        if 0 <= month_index < 12:
            persian_month = persian_month_names[month_index]
            events_by_month[persian_month].append(event)

    # Debugging: Print organized events
    print(events_by_month)

    return render(request, 'dashboard/exhibition_calendar.html', {
        'events_by_month': events_by_month,
        'persian_month_names': persian_month_names,
    })


from django.shortcuts import render
from .models import News

def latest_news(request):
    news_list = News.objects.all().order_by('-publication_date')  # Newest first
    return render(request, 'dashboard/latest_news.html', {'news_list': news_list})
# dashboard/views.py

from django.shortcuts import render, get_object_or_404
from .models import Department, Project

def projects_departments(request):
    departments = Department.objects.all()
    return render(request, 'dashboard/projects_departments.html', {'departments': departments})

def department_projects(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    projects = Project.objects.filter(department=department)
    context = {
        'department': department,
        'projects': projects
    }
    return render(request, 'dashboard/department_projects.html', context)


from django.shortcuts import render
from django.http import JsonResponse

def data_sources(request):
    return render(request, 'dashboard/data_sources.html')

# Example API view to simulate fetching data
import random
from datetime import timedelta
from django.utils import timezone

def api_data_source(request, source):
    days = int(request.GET.get('days', 30))
    data = []
    for i in range(days):
        date = timezone.now() - timedelta(days=i)
        value = random.uniform(1000, 5000)  # Simulating data values
        data.append({'date': date.isoformat(), 'value': value})
    return JsonResponse(data, safe=False)
