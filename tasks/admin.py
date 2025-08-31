from django.contrib import admin
from .models import Task, Comment

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority', 'author')
    search_fields = ('title', 'description')
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'created_at')
    list_filter = ('author',)
    search_fields = ('text',)