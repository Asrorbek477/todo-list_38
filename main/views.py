from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *

class IndexView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        context = {'tasks': tasks}
        return render(request, 'index.html', context)

    def post(self, request):
        Task.objects.create(
            title = request.POST['title'],
            details = request.POST['details'],
            status = request.POST['status'],
            deadline = request.POST.get('deadline') if request.POST.get('deadline') else None,
            user = request.user
        )
        return redirect('home')

class TaskUpdateView(View):

    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        return render(request, 'task-update.html', {'task': task})

    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)

        task.title = request.POST.get('title')
        task.details = request.POST.get('details')
        task.status = request.POST.get('status')
        task.save()

        return redirect('home')

def delete_task(request, id):
    task = get_object_or_404(Task, id=id)

    if request.method == "POST":
        task.delete()
        return redirect('home')

    return render(request, 'delete.html', {'task': task})

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        if request.POST.get('password') == request.POST.get('password-repeat'):
            if request.POST.get('username') not in User.objects.values_list('username', flat=True):
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password'],
                )
                login(request, user)
                return redirect('home')
            return redirect('/login/')
        return redirect('register')

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password'],
        )

        if user:
            login(request, user)
            return redirect('home')
        return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login')