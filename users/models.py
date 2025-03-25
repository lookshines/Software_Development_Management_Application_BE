from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.
class User(AbstractUser):
    # Define role choices
    ADMIN = "Admin"
    PROJECT_MANAGER = "Project Manger"
    PRODUCT_MANAGER = "Product manager"
    FRONTEND_DEVELOPER = "Frontend Developer"
    BACKEND_DEVELOPER = "Backend Developer"
    UI_UX_DESIGNER = "UI/UX Designer"
    CLIENT = "Client"
    
    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (PROJECT_MANAGER, "Project Manger"),
        (PRODUCT_MANAGER, "Product manager"),
        (FRONTEND_DEVELOPER, "Frontend Developer"),
        (BACKEND_DEVELOPER, "Backend Developer"),
        (UI_UX_DESIGNER, "UI/UX Designer"),
        (CLIENT, "Client")
]
    
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=BACKEND_DEVELOPER)
    
    def __str__(self):
        return f"{self.username} - {self.role}"

User = get_user_model()

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    start_date = models.DateField()
    schedule_end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    assigned_users = models.ManyToManyField(User, blank=True)
    
    def __str__(self):
        return self.project_name