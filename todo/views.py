from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import TodoForm
from .models import Todo
from django.utils import timezone


def home(request):
    return render(request, 'todo/home.html')

# Create your views here.
def signUp(request):
    form = UserCreationForm()
    context = {"form": form}
    if request.method == "POST":
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if password1 == password2:
            try:
                user = User.objects.create_user(username, password=password1)
                user.save()
                login(request, user)
                return redirect('todos')
            except IntegrityError:
                context['error'] = 'The user is already exists!'
        else:
            context['error'] = 'Password are not same!'
    return render(request, 'todo/signup.html', context)

def loginUser(request):
    context = {'form': AuthenticationForm()}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('todos')
        else:
            context['error'] = 'Invalid Login or Password'

    return render(request, 'todo/login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def todos(request):
    todos =Todo.objects.filter(user=request.user, datecompleted__isnull=True).order_by('updated')
    context = {"todos": todos}
    return render(request, 'todo/todos.html', context)

@login_required(login_url='login')
def completedTodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    context = {"todos": todos}
    return render(request, 'todo/completedtodos.html', context)

@login_required(login_url='login')
def createTodo(request):
    context = {"form": TodoForm}
    if request.method == "POST":
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('todos')
        except ValueError:
            context['error'] = 'Invalid data input'
            return render(request, 'todo/createtodo.html', context)
    return render(request, 'todo/createtodo.html', context)

@login_required(login_url='login')
def detailTodo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        try:
            form.save()
            return redirect('todos')
        except Exception as error:
            return error
    form = TodoForm(instance=todo)
    context = {'todo': todo, 'form': form}
    return render(request, 'todo/detailtodo.html', context)

@login_required(login_url='login')
def completeTodo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('todos')

@login_required(login_url='login')
def deleteTodo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        todo.delete()
        return redirect('todos')
