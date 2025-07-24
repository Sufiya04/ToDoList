from django.db import models

# Create your models here.
class Todo(models.Model):
    task=models.CharField(max_length=50)
    des=models.TextField()
    time=models.DateTimeField(auto_now_add=True)
class Meta:
    verbose_name_plural="Todo"