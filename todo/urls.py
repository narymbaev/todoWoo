from django.urls import path
from .views import signUp, todos, logoutUser, loginUser, createTodo, detailTodo, completeTodo, deleteTodo, completedTodos, home

urlpatterns = [
    path('signup/', signUp, name='signup'),
    path('home/', home, name='home'),
    path('todos/', todos, name='todos'),
    path('completedtodos/', completedTodos, name='completedtodos'),
    path('todo/<int:pk>/', detailTodo, name='detailtodo'),
    path('todo/<int:pk>/complete/', completeTodo, name='completetodo'),
    path('todo/<int:pk>/delete/', deleteTodo, name='deletetodo'),
    path('create/', createTodo, name='createtodo'),
    path('logout/', logoutUser, name='logout'),
    path('login/', loginUser, name='login')
]