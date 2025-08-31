from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Task(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', "Нове"
        IN_PROGRESS = 'in_progress', "В процесі" 
        DONE = 'done', "Виконане"
        CANCELED = 'canceled', "Відмінене"
        REVIEW = 'review', "Превіряється"
    
    class Priority(models.TextChoices):
        LOW = 'low', 'Низький'
        MEDIUM = 'medium', 'Середній'
        HIGH = 'high', 'Високий'
        EMERGENCY = 'emergency', 'Невідкладний'
        OPTIONAL = 'optional', "Необов'язковий"
    
    title = models.CharField(max_length=255, verbose_name="Назва завдання")
    description = models.TextField(verbose_name="Опис")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', verbose_name='Автор')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW, verbose_name="Статус")
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.LOW, verbose_name='Пріоритет')
    due_date = models.DateField(verbose_name='Термірмін виконання', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("task_detail", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ['-created_at']
        
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments', verbose_name='Завдання')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="Автор")
    text = models.TextField(verbose_name="Текст коментаря")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Коментар до {self.task.title}. Автор: {self.author.username} Дата: {self.created_at}"
    
    class Meta:
        ordering = ['created_at']