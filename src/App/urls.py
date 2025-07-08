from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('', views.home, name='home'),
    path('medications/', views.medication_list, name='medication_list'),
    path('purchases/', views.purchase_list, name='purchase_list'),
    path('reports/', views.reports, name='reports'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('change-language/<str:language_code>/', views.change_language, name='change_language'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('medicaments/', views.admin_medicaments, name='admin_medicaments'),
    path('medicament/<int:medicament_id>/', views.admin_medicament_detail, name='admin_medicament_detail'),
    path('medicament/<int:medicament_id>/toggle/', views.admin_toggle_medicament, name='admin_toggle_medicament'),

    path('dashboard/', views.dashboard, name='dashboard'),

]
