from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView
from .models import Task
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class Customlogin(LoginView):
    fields = '__all__'
    template_name = 'base/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self) -> str:
        return reverse_lazy('detail')

class Customlogout(LogoutView):
    template_name = 'base/logout.html'
    
class Tasklist(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'base/task.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user= self.request.user)
        context['count'] = context['tasks'].filter(completed = False).count()
        search_input = self.request.GET.get('search-area') or ''

        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith = search_input)

        context['search_input'] = search_input
        return context


class Taskdetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'base/detail.html'
    context_object_name = 'tasks'

class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','description','completed']
    template_name = 'base/create.html'
    success_url = reverse_lazy('detail')

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)


class Taskupdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title','description','completed']
    template_name = 'base/update.html'
    success_url = reverse_lazy('detail')

class Deletetask(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('detail')
    template_name = 'base/delete.html'

class RegisterForm(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url  = reverse_lazy('detail')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterForm, self).form_valid(form)
    
    def get(self, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            return redirect('detail')
        return super(RegisterForm, self).get(*args, **kwargs)

        

        


    