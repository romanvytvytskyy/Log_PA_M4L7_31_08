from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import (LoginRequiredMixin, 
                                        UserPassesTestMixin)
from django.views.generic.edit import FormMixin
from .models import Task
from .form import TaskForm, CommentForms

# Create your views here.
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Task.objects.filter(author = self.request.user)
        status = self.request.GET.get('status', '')
        priority = self.request.GET.get('priority', '')
        
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority = priority)
        return queryset
        # return Task.objects.filter(author=self.request.user)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['status_choices'] = Task.Status.choices
        context['priority_choices'] = Task.Priority.choices

        context['status_choices'] = self.request.GET.get('status', '')
        context['priority_choices'] = self.request.GET.get('priority', '')
    
        return context
    
class TaskDetailView(LoginRequiredMixin, generic.DetailView, FormMixin):
    model = Task
    template_name = 'tasks/task_detail.html'
    form_class = CommentForms
    
    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = self.get_form()
        context['comments'] = self.object.comments.all()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid(form):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.task = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)
    
class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    template_name = 'tasks/task_create.html'
    form_class = TaskForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class TaskDeleteView(LoginRequiredMixin, generic.DeleteView, 
                     UserPassesTestMixin):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('task_list')
    
    def test(self):
        task = self.get_object()
        return self.request.user == task.author
    
class TaskUpdateView(LoginRequiredMixin, generic.UpdateView, 
                     UserPassesTestMixin):
    model = Task
    template_name = 'tasks/task_update.html'
    form_class = TaskForm
    
    def test(self):
        task = self.get_object()
        return self.request.user == task.author
    
    