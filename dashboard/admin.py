# dashboard/admin.py

from django.contrib import admin
from .models import (
    Department,
    Position,
    EducationLevel,
    Employee,
    Product,
    Customer,
    Sale,
    Branch
)

admin.site.register(Department)
admin.site.register(Position)
admin.site.register(EducationLevel)
admin.site.register(Employee)
admin.site.register(Product)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'country', 'customer_type', 'region')
    list_filter = ('country', 'customer_type', 'region')
    search_fields = ('first_name', 'last_name', 'country')

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'date', 'quantity', 'total_price', 'branch')
    list_filter = ('date', 'branch', 'product')
    search_fields = ('customer__first_name', 'customer__last_name', 'product__name')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city')


from .models import Country,CountryReport  # Replace with your actual model names

@admin.register(CountryReport)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country', 'population', 'gdp', 'life_expectancy','report_pdf')
    search_fields = ('country',)

@admin.register(Country)
class CountryAdmin2(admin.ModelAdmin):
    list_display = ('name',)


# dashboard/admin.py

from django.contrib import admin
from .models import CountryEconomicData

@admin.register(CountryEconomicData)
class CountryEconomicDataAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'population', 'gdp', 'annual_gdp_growth', 'life_expectancy')
    search_fields = ('name',)


from django.contrib import admin
from .models import Category, Material, MaterialDocument

class MaterialDocumentInline(admin.TabularInline):
    model = MaterialDocument
    extra = 1

class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    inlines = [MaterialDocumentInline]

admin.site.register(Category)
admin.site.register(Material, MaterialAdmin)


from .models import TrainingCourse, TrainingSession

class TrainingSessionInline(admin.TabularInline):
    model = TrainingSession
    extra = 1  # Allows adding one additional session at a time

class TrainingCourseAdmin(admin.ModelAdmin):
    inlines = [TrainingSessionInline]
    list_display = ('title', 'created_at')
    search_fields = ['title']

admin.site.register(TrainingCourse, TrainingCourseAdmin)

# dashboard/admin.py

from .models import OrganizationalInfo

@admin.register(OrganizationalInfo)
class OrganizationalInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_type', 'file')
    search_fields = ('title',)
from django.contrib import admin
from .models import ExhibitionEvent

@admin.register(ExhibitionEvent)
class ExhibitionEventAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'event_date']
    list_filter = ['event_date']


from django.contrib import admin
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date')
    list_filter = ('publication_date',)
    search_fields = ('title', 'summary', 'content')
    ordering = ('-publication_date',)

# dashboard/admin.py
from django.contrib import admin
from .models import Project, Task

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1  # Number of blank tasks to display initially

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'start_date', 'end_date')
    search_fields = ('name', 'department__name')
    inlines = [TaskInline]

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'progress', 'responsible_person')
    search_fields = ('name', 'project__name')
    list_filter = ('project', 'progress')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)

