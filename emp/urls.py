from django.urls import path
from .import views

urlpatterns = [
    path('', views.CreateTask, name='home'),
    path('details/<str:pk>', views.UpdateEmployee, name='details'),
    path('delete/<str:pk>', views.DeleteDetail, name='delete'),
    path('search/', views.SearchField, name='search'),
    path('emp_api/', views.EmpCrudApi.as_view(), name='emp_api'),
    path('emp_api/<str:pk>', views.EmpCrudApi.as_view(), name='emp_api'),

]