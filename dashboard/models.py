# dashboard/models.py
from django.utils import timezone  # Import timezone

from django.db import models
from django.contrib.auth.models import User  # Assuming you're using Django's built-in User model

# Employee-related models
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Position(models.Model):
    title = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.level})'


class EducationLevel(models.Model):
    level = models.CharField(max_length=50)  # e.g., 'High School', 'Bachelor', 'Master', 'PhD'

    def __str__(self):
        return self.level

class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'مرد'),
        ('F', 'زن'),
    ]

    STATUS_CHOICES = [
        ('Active', 'فعال'),
        ('Left', 'ترک خدمت'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    education_level = models.ForeignKey(EducationLevel, on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    date_of_hire = models.DateField(default=timezone.now)  # Corrected
    date_of_leave = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# Sales-related models
class Branch(models.Model):
    name = models.CharField(max_length=100)  # Name of the branch
    city = models.CharField(max_length=100)  # City where the branch is located

    def __str__(self):
        return f'{self.name} ({self.city})'

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  # E.g., 'Electronics', 'Clothing', etc.
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ('Trader', 'Trader'),
        ('Producer', 'Producer'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    region = models.CharField(max_length=50)  # E.g., 'North', 'South', etc.
    country = models.CharField(max_length=50, default='')
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPE_CHOICES, default='Trader')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically calculate total price
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Sale of {self.product.name} to {self.customer.first_name} on {self.date}'

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CountryReport(models.Model):
    country = models.OneToOneField(Country, on_delete=models.CASCADE)
    population = models.BigIntegerField()
    gdp = models.BigIntegerField()  # GDP in local currency
    annual_gdp = models.BigIntegerField()  # Annual GDP in local currency
    life_expectancy = models.FloatField()
    report_pdf = models.FileField(upload_to='reports/', blank=True, null=True)

    def __str__(self):
        return f"{self.country.name} Report"

class CountryEconomicData(models.Model):
    country_name = models.CharField(max_length=100, unique=True)
    population = models.BigIntegerField()
    gdp = models.DecimalField(max_digits=20, decimal_places=2)
    annual_gdp_growth = models.DecimalField(max_digits=5, decimal_places=2)
    life_expectancy = models.DecimalField(max_digits=4, decimal_places=2)
    report_pdf = models.FileField(upload_to='reports/', null=True, blank=True)

    def __str__(self):
        return self.country_name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='category_icons/', null=True, blank=True)

    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, related_name='materials', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='material_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class MaterialDocument(models.Model):
    material = models.ForeignKey(Material, related_name='documents', on_delete=models.CASCADE)
    document_type = models.CharField(max_length=200, choices=[
        ('بازرگان', 'بازرگان'),
        ('تولید‌کننده', 'تولیدکننده'),
        ('درون‌سازمانی', 'درون‌سازمانی'),
        ('وبسایت', 'وبسایت'),
        ('شبکه‌های اجتماعی', 'شبکه‌های اجتماعی'),
        ('نمایشگاه‌ها', 'نمایشگاه‌ها'),
        ('ویزیتوری', 'ویزیتوری'),
        ('وبینار', 'وبینار'),
        ('سیمنارها', 'سیمنارها'),
    ])
    pdf_file = models.FileField(upload_to='material_documents/', null=True, blank=True)

    def __str__(self):
        return f"{self.material.name} - {self.document_type}"

class TrainingCourse(models.Model):
    title = models.CharField(max_length=200)  # The name of the training course
    description = models.TextField(blank=True)  # Optional description of the course
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp when the course was created

    def __str__(self):
        return self.title

# Training session model
class TrainingSession(models.Model):
    course = models.ForeignKey(TrainingCourse, related_name='sessions', on_delete=models.CASCADE)  # Course associated with the session
    title = models.CharField(max_length=200)  # Name of the session (e.g., "Session 1")
    content_text = models.TextField(blank=True)  # Optional text content for the session
    content_image = models.ImageField(upload_to='training_images/', null=True, blank=True)  # Optional image content
    content_video = models.FileField(upload_to='training_videos/', null=True, blank=True)  # Optional video/multimedia content
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp when the session was created

    def __str__(self):
        return f'{self.title} - {self.course.title}'

class OrganizationalInfo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file_type = models.CharField(max_length=10, choices=[
        ('PDF', 'PDF'),
        ('WORD', 'Word'),
        ('PPT', 'PowerPoint')
    ])
    file = models.FileField(upload_to='organizational_info_files/')

    def __str__(self):
        return self.title

class ExhibitionEvent(models.Model):
    event_name = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateField()

    def __str__(self):
        return f"{self.event_name} on {self.event_date}"

class News(models.Model):
    title = models.CharField(max_length=255)
    publication_date = models.DateField()
    summary = models.TextField()
    content = models.TextField(blank=True, null=True)  # Optional: Full article content
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)  # Optional: Image for the news
    link = models.URLField(blank=True, null=True)  # Optional: External link to full article

    class Meta:
        ordering = ['-publication_date']  # Newest first

    def __str__(self):
        return self.title

class Project(models.Model):
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    progress = models.PositiveIntegerField(default=0)  # Percentage (0-100)
    responsible_person = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

