from django import forms
from .models import Task, Comment
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 
            'description', 
            'status',
            'priority',
            'due_date',
            'attachment',
            ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }
class CommentForms(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'rows':3,
                    'placeholder': "Ваш коментар..."
                    }
            )
        }