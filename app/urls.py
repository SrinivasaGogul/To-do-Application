from django.urls import path
from app import views
urlpatterns = [
    path('', views.Tasklist.as_view(), name='detail'),
    path('task/<int:pk>', views.Taskdetail.as_view(), name='tasks'),
    path("create/", views.CreateTask.as_view(), name='create'),
    path('update/<int:pk>', views.Taskupdate.as_view(), name='update'),
    path('delete/<int:pk>', views.Deletetask.as_view(), name='delete'),
    path('login/', views.Customlogin.as_view(), name='login'),
    path('logout/', views.Customlogout.as_view(next_page = 'login'), name='logout'),
    path('register/', views.RegisterForm.as_view(), name = 'register')
    
]