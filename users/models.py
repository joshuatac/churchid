from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.img import image_resize
import uuid
import random
import string


def generate_unique_id():
    """Generate a unique numeric ID for the username"""
    while True:
        unique_id = ''.join(random.choices(string.digits, k=8))  # Generate an 8-digit number
        if not Member.objects.filter(username=unique_id).exists():
            return unique_id
        
        
class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    leader = models.OneToOneField("Member", on_delete=models.SET_NULL, null= True, blank=True, related_name="leader_department")
    church = models.ForeignKey("Church", on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'users'


class Church(models.Model):
    DENOMINATION_CHOICES = (
        ("Charismatic", "Charismatic"),
        ("Pentecostal", "Pentecostal"),
        ("Catholic", "Catholic"),
        ("Orthodox", "Orthodox"),
        ("Others", "Others"),
    )
    
    BRANCH_TYPE_CHOICES = (
        ("Branch", "Branch"),
        ("Province", "Province"),
        ("Chapter", "Chapter"),
        ("Center", "Center"),
        ("Place", "Place"),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    denomination = models.CharField(max_length=50, choices=DENOMINATION_CHOICES, blank=True)
    founded = models.DateField(null=True, blank=True)
    website = models.CharField(max_length=100, blank=True)
    branch_name = models.CharField(max_length=100, blank=True)
    branch_type = models.CharField(max_length=100, choices=BRANCH_TYPE_CHOICES, blank=True)
    address = models.CharField(max_length=150, blank=True)
    logo = models.ImageField(upload_to="logos/", blank= True, null=True)
    is_active = models.BooleanField(default=False)
    
    @property
    def overseer(self):
        return Member.objects.get(is_staff = True, role ="leader", church = self)
    
    @property
    def logo_url(self):
        return self.get_logo_url
    
    def get_logo_url(self):
        if self.logo:
            return self.logo.url  # Return the uploaded file
        return "/images/logos/default.jpg"  # Return the default file
    
    def save(self, *args, **kwargs):
        if self.logo:
            image_resize(self.logo, 300, 300)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Member(AbstractUser):
    
    TITLE_CHOICES = (
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
        ('Pastor', 'Pastor'),
        ('Elder', 'Elder'),
        ('Prophet', 'Prophet'),
        ('Apostle', 'Apostle'),
    )
    
    ROLE_CHOICES = (
        
        ("admin", "Admin"),
        ("leader", "Leader"),
        ("member", "Member")
    )
    

    SEX_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name="members", related_query_name="members", blank=True, null=True)
    first_name = models.CharField(max_length= 50, blank=False)
    last_name = models.CharField(max_length= 50, blank=False)
    email = models.EmailField()
    username = models.CharField(max_length=50, unique=True, blank=True) 
    address = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    box_number = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=20, choices=TITLE_CHOICES, blank=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")
    is_active = models.BooleanField(default=False)
    new = models.BooleanField(default=True)
    department = models.ForeignKey(Department, blank=True, null=True, on_delete=models.SET_NULL, related_name="members")

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = generate_unique_id()
        if self.is_superuser:
            self.is_active = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_full_name() if self.get_full_name() else self.username}"
    
    

