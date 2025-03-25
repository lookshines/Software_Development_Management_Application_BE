from django.db import models
from django.contrib.auth.models import AbstractUser

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