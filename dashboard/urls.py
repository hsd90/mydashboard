# dashboard/urls.py
from django.contrib import admin
from django.urls import path
from dashboard import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('sales/', views.sales_statistics, name='sales_statistics'),
    path('marketing/', views.marketing_statistics, name='marketing_statistics'),
    path('geographical_report/', views.geographical_report, name='geographical_report'),
    path('materials/', views.material_categories, name='material_categories'),
    path('materials/<int:category_id>/', views.category_materials, name='category_materials'),  # This handles /materials/1/
    path('materials/detail/<int:material_id>/', views.material_detail, name='material_detail'),
    path('training/', views.training_courses, name='training_courses'),  # List of training courses
    path('training/course/<int:course_id>/', views.course_detail, name='course_detail'),  # Course details with sessions
    path('training/session/<int:session_id>/', views.session_detail, name='session_detail'),  # Session details and content
    path('training/', views.training_courses, name='training_courses'),
    path('exhibition_calendar/', views.exhibition_calendar, name='exhibition_calendar'),
    path('latest_news/', views.latest_news, name='latest_news'),
    path('latest_analyses/', views.latest_analyses, name='latest_analyses'),
    path('reports/', views.reports, name='reports'),
    path('organizational-info/', views.organizational_info, name='organizational_info'),
    path('projects/', views.projects_departments, name='projects_departments'),
    path('projects/<int:department_id>/', views.department_projects, name='department_projects'),
     path('data-sources/', views.data_sources, name='data_sources'),
    path('api/data-source/<str:source>/', views.api_data_source, name='api_data_source'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)