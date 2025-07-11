from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    # GET VIEWS
    path('', views.home, name='home'),
    path('medications/', views.medication_list, name='medication_list'),
    path('purchases/', views.purchase_list, name='purchase_list'),
    path('reports/', views.reports, name='reports'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('change-language/<str:language_code>/', views.change_language, name='change_language'),
    path('staff/login/', views.admin_login, name='admin_login'),
    path('staff/logout/', views.admin_logout, name='admin_logout'),
    path('staff/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('medicaments/', views.admin_medicaments, name='admin_medicaments'),
    path('medicament/<int:medicament_id>/', views.admin_medicament_detail, name='admin_medicament_detail'),
    path('medicament/<int:medicament_id>/toggle/', views.admin_toggle_medicament, name='admin_toggle_medicament'),

    # CRUD MEDICATION
    path('medicament/get', views.get_medication_with_post, name='get_medication_post'),
    path('medicament/add', views.add_medication, name='add_medication'),
    path('medicament/edit', views.edit_medication, name='edit_medication'),
    path('medicament/delete', views.delete_medication, name='delete_medication'),

    # CRUD PURCHASE
    path('purchase/add', views.add_purchase, name='add_purchase'),
    path('purchase/get', views.get_purchase_details_post, name='get_purchase_details'),
    path('purchase/delete', views.delete_purchase, name='delete_purchase'),

    # RECEIPT URLS
    path('receipt/<int:purchase_id>/', views.print_receipt, name='print_receipt'),
    path('receipt-ajax/', views.print_receipt_ajax, name='print_receipt_ajax'),
    path('receipt-pdf/<int:purchase_id>/', views.print_receipt_pdf, name='print_receipt_pdf'),


    path('dashboard/', views.dashboard, name='dashboard'),

]
