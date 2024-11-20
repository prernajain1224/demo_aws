from django.urls import path
from . import views  


urlpatterns = [
    path('', views.home),
    path('upload/', views.upload_document, name='upload_document'),
    path('upload_success/', views.upload_success, name='upload_success'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('data/', views.data_department_view, name='data_department'),
    path('infra/', views.infra_department_view, name='infra_department'),
    path('digital_marketing/', views.digital_marketing_department_view, name='digital_marketing_department'),
]


