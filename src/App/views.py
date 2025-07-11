from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.translation import activate
from django.utils import translation
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from datetime import datetime
from decimal import Decimal
from django.core.paginator import Paginator
from .models import *
from django.template.loader import render_to_string
from django.utils import timezone
import json

def home(request):
    """Home page view with background image and navigation buttons."""
    return render(request, 'pharmacy/home.html')

@login_required(login_url='pharmacy:login')
def medication_list(request):
    """View to display and manage medications."""
    categories = Category.objects.all()
    medications = Medication.objects.all().order_by('name')
    
    context = {
        'categories': categories,
        'medications': medications,
    }
    return render(request, 'pharmacy/medication_list.html', context)

@login_required(login_url='pharmacy:login')
@csrf_exempt
@require_http_methods(["POST"])
def add_medication(request):
    """Add a new medication via AJAX."""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['name', 'category_id', 'description', 'price', 'stock_quantity', 'expiry_date']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'success': False, 'error': f'{field} is required'})
        
        # Get category
        try:
            category = Category.objects.get(id=data['category_id'])
        except Category.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid category'})
        
        # Parse expiry date
        try:
            expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid date format'})
        
        # Create medication
        medication = Medication.objects.create(
            name=data['name'],
            category=category,
            description=data['description'],
            price=float(data['price']),
            stock_quantity=int(data['stock_quantity']),
            expiry_date=expiry_date
        )
        
        return JsonResponse({
            'success': True,
            'medication': {
                'id': medication.id,
                'name': medication.name,
                'category': medication.category.name,
                'price': str(medication.price),
                'stock_quantity': medication.stock_quantity,
                'expiry_date': medication.expiry_date.strftime('%Y-%m-%d')
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required(login_url='pharmacy:login')
@csrf_exempt
@require_http_methods(["POST"])
def edit_medication(request):
    """Edit an existing medication via AJAX."""
    try:
        data = json.loads(request.body)
        medication = get_object_or_404(Medication, id=data.get("id"))
        
        # Update fields if provided
        if 'name' in data:
            medication.name = data['name']
        if 'category_id' in data:
            try:
                category = Category.objects.get(id=data['category_id'])
                medication.category = category
            except Category.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Invalid category'})
        if 'description' in data:
            medication.description = data['description']
        if 'price' in data:
            medication.price = float(data['price'])
        if 'stock_quantity' in data:
            medication.stock_quantity = int(data['stock_quantity'])
        if 'expiry_date' in data:
            try:
                medication.expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid date format'})
        
        medication.save()
        
        return JsonResponse({
            'success': True,
            'medication': {
                'id': medication.id,
                'name': medication.name,
                'category': medication.category.name,
                'price': str(medication.price),
                'stock_quantity': medication.stock_quantity,
                'expiry_date': medication.expiry_date.strftime('%Y-%m-%d')
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required(login_url='pharmacy:login')
@csrf_exempt
@require_http_methods(["POST"])
def delete_medication(request):
    """Delete a medication via AJAX."""
    try:
        print("HEY")
        data = json.loads(request.body)
        print(data)
        medication = get_object_or_404(Medication, id=data.get('id'))
        print(medication)
        medication.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required(login_url='pharmacy:login')
def get_medication(request, medication_id):
    """Get medication details for editing."""
    try:
        medication = get_object_or_404(Medication, id=medication_id)
        return JsonResponse({
            'success': True,
            'medication': {
                'id': medication.id,
                'name': medication.name,
                'category_id': medication.category.id,
                'category_name': medication.category.name,
                'description': medication.description,
                'price': str(medication.price),
                'stock_quantity': medication.stock_quantity,
                'expiry_date': medication.expiry_date.strftime('%Y-%m-%d')
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required(login_url='pharmacy:login')
def get_medication_with_post(request):
    """Get medication details for editing."""
    try:
        print("data")
        data = json.loads(request.body)
        print(data)
        medication = get_object_or_404(Medication, id=data.get("id"))
        print(str(medication.id))
        return JsonResponse({
            'success': True,
            'medication': {
                'id': medication.id,
                'name': medication.name,
                'category_id': medication.category_id,
                'category_name': medication.category.name,
                'description': medication.description,
                'price': str(medication.price),
                'stock_quantity': medication.stock_quantity,
                'expiry_date': medication.expiry_date.strftime('%Y-%m-%d')
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required(login_url='pharmacy:login')
def purchase_list(request):
    """View to display and manage purchases."""
    purchases = Purchase.objects.all().order_by('-purchase_date')
    medications = Medication.objects.filter(stock_quantity__gt=0).order_by('name')
    
    context = {
        'purchases': purchases,
        'medications': medications,
    }
    return render(request, 'pharmacy/purchase_list.html', context)

@login_required(login_url='pharmacy:login')
@csrf_exempt
@require_http_methods(["POST"])
def add_purchase(request):
    """Add a new purchase via AJAX."""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['customer_name', 'payment_method', 'items']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'success': False, 'error': f'{field} is required'})
        
        if not data['items']:
            return JsonResponse({'success': False, 'error': 'At least one item is required'})
        
        with transaction.atomic():
            # Create purchase
            purchase = Purchase.objects.create(
                customer_name=data['customer_name'],
                customer_phone=data.get('customer_phone', ''),
                payment_method=data['payment_method'],
                staff=request.user,
                total_amount=0  # Will be calculated
            )
            
            total_amount = Decimal('0.00')
            
            # Create purchase items
            for item_data in data['items']:
                try:
                    medication = Medication.objects.get(id=item_data['medication_id'])
                    quantity = int(item_data['quantity'])
                    
                    # Check stock availability
                    if medication.stock_quantity < quantity:
                        return JsonResponse({
                            'success': False, 
                            'error': f'Insufficient stock for {medication.name}. Available: {medication.stock_quantity}'
                        })
                    
                    unit_price = medication.price
                    subtotal = unit_price * quantity
                    
                    # Create purchase item
                    PurchaseItem.objects.create(
                        purchase=purchase,
                        medication=medication,
                        quantity=quantity,
                        unit_price=unit_price,
                        subtotal=subtotal
                    )
                    
                    # Update medication stock
                    medication.stock_quantity -= quantity
                    medication.save()
                    
                    total_amount += subtotal
                    
                except Medication.DoesNotExist:
                    return JsonResponse({'success': False, 'error': f'Medication not found'})
                except (ValueError, KeyError):
                    return JsonResponse({'success': False, 'error': 'Invalid item data'})
            
            # Update purchase total
            purchase.total_amount = total_amount
            purchase.save()
            
            return JsonResponse({
                'success': True,
                'purchase': {
                    'id': purchase.id,
                    'customer_name': purchase.customer_name,
                    'customer_phone': purchase.customer_phone,
                    'total_amount': str(purchase.total_amount),
                    'payment_method': purchase.get_payment_method_display(),
                    'purchase_date': purchase.purchase_date.strftime('%b %d, %Y %H:%M')
                }
            })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required(login_url='pharmacy:login')
def get_purchase(request, purchase_id):
    """Get purchase details for viewing."""
    try:
        purchase = get_object_or_404(Purchase, id=purchase_id)
        items = []
        
        for item in purchase.items.all():
            items.append({
                'medication_name': item.medication.name,
                'quantity': item.quantity,
                'unit_price': str(item.unit_price),
                'subtotal': str(item.subtotal)
            })
        
        return JsonResponse({
            'success': True,
            'purchase': {
                'id': purchase.id,
                'customer_name': purchase.customer_name,
                'customer_phone': purchase.customer_phone or 'N/A',
                'total_amount': str(purchase.total_amount),
                'payment_method': purchase.get_payment_method_display(),
                'purchase_date': purchase.purchase_date.strftime('%b %d, %Y %H:%M'),
                'staff': purchase.staff.username if purchase.staff else 'N/A',
                'items': items
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required(login_url='pharmacy:login')
@require_http_methods(["POST"])
def get_purchase_details_post(request):
    """Get purchase details for viewing."""
    try:
        data = json.loads(request.body)
        purchase = get_object_or_404(Purchase, id=data.get("id"))
        items = []
        
        for item in purchase.items.all():
            items.append({
                'medication_name': item.medication.name,
                'quantity': item.quantity,
                'unit_price': str(item.unit_price),
                'subtotal': str(item.subtotal)
            })
        
        return JsonResponse({
            'success': True,
            'purchase': {
                'id': purchase.id,
                'customer_name': purchase.customer_name,
                'customer_phone': purchase.customer_phone or 'N/A',
                'total_amount': str(purchase.total_amount),
                'payment_method': purchase.get_payment_method_display(),
                'purchase_date': purchase.purchase_date.strftime('%b %d, %Y %H:%M'),
                'staff': purchase.staff.username if purchase.staff else 'N/A',
                'items': items
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required(login_url='pharmacy:login')
@csrf_exempt
@require_http_methods(["POST"])
def delete_purchase(request):
    """Delete a purchase via AJAX."""
    try:
        data = json.loads(request.body)
        purchase = get_object_or_404(Purchase, id=data.get('id'))
        
        with transaction.atomic():
            # Restore stock for each item
            for item in purchase.items.all():
                medication = item.medication
                medication.stock_quantity += item.quantity
                medication.save()
            
            # Delete purchase (items will be deleted due to CASCADE)
            purchase.delete()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required(login_url='pharmacy:login')
def reports(request):
    """View to display various reports and analytics."""
    # Get sales data
    total_sales = Purchase.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    total_purchases = Purchase.objects.count()
    total_medications = Medication.objects.count()
    
    # Get top selling medications
    top_medications = Medication.objects.annotate(
        sold=Sum('purchaseitem__quantity')
    ).order_by('-sold')[:5]
    
    # Get low stock medications
    low_stock = Medication.objects.filter(stock_quantity__lt=10).order_by('stock_quantity')
    
    context = {
        'total_sales': total_sales,
        'total_purchases': total_purchases,
        'top_medications': top_medications,
        'total_medications': total_medications,
        'low_stock': low_stock,
    }
    return render(request, 'pharmacy/reports.html', context)

def login_view(request):
    """View for user login."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!", extra_tags='success')
                return redirect('pharmacy:home')
            else:
                messages.error(request, "Invalid username or password.", extra_tags='danger')
        else:
            messages.error(request, "Invalid username or password.", extra_tags='danger')
    else:
        form = AuthenticationForm()
    return render(request, 'pharmacy/login.html', {'form': form})

def register_view(request):
    """View for user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!", extra_tags='success')
            return redirect('pharmacy:home')
        else:
            # messages.error(request, "Registration failed. Please correct the errors.")
            messages.error(request, form.errors.as_text(), extra_tags='danger')
            
    else:
        form = UserCreationForm()
    return render(request, 'pharmacy/register.html', {'form': form})

def logout_view(request):
    """View for user logout."""
    logout(request)
    messages.info(request, "You have successfully logged out.", extra_tags='info')
    return redirect('pharmacy:home')

def change_language(request, language_code):
    """View to change the application language."""
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('pharmacy:home')))
    
    if language_code:
        activate(language_code)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language_code)
    
    return response

def is_admin(user):
    return user.is_authenticated and user.is_staff

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and ( user.is_staff or user.is_superuser):
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} !', extra_tags='success')
            
            # Redirection vers le dashboard admin
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('admin/dashboard.html')  # Redirection vers admin:dashboard
        else:
            messages.error(request, 'Identifiants invalides ou accès non autorisé', extra_tags="error")
    
    return render(request, 'admin/login.html')

@login_required(login_url='pharmacy:admin_login')
def admin_dashboard(request):
    # Statistiques générales
    total_medicaments = Medicament.objects.count()
    total_users = User.objects.count()
    medicaments_actifs = Medicament.objects.filter(is_active=True).count()
    
    # Médicaments récents
    recent_medicaments = Medicament.objects.order_by('-created_at')[:5]
    
    context = {
        'total_medicaments': total_medicaments,
        'total_users': total_users,
        'medicaments_actifs': medicaments_actifs,
        'recent_medicaments': recent_medicaments,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required(login_url='pharmacy:login')
def admin_medicaments(request):
    search_query = request.GET.get('search', '')
    medicaments = Medicament.objects.all()
    
    if search_query:
        medicaments = medicaments.filter(
            Q(nom__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(medicaments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'admin/medicaments.html', context)

@login_required(login_url='pharmacy:login')
def admin_medicament_detail(request, medicament_id):
    medicament = get_object_or_404(Medicament, id=medicament_id)
    return render(request, 'admin/medicament_detail.html', {'medicament': medicament})

@login_required(login_url='pharmacy:login')
def admin_toggle_medicament(request, medicament_id):
    if request.method == 'POST':
        medicament = get_object_or_404(Medicament, id=medicament_id)
        medicament.is_active = not medicament.is_active
        medicament.save()
        return JsonResponse({'success': True, 'is_active': medicament.is_active})
    return JsonResponse({'success': False})

def admin_logout(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté avec succès.', extra_tags="info")
    return redirect('pharmacy:admin_login')


def dashboard(request):
    return render(request, 'pharmacy/dashboard.html')

@login_required
@require_http_methods(["GET"])
def print_receipt(request, purchase_id):
    """
    Generate a printable receipt for a specific purchase
    """
    try:
        purchase = get_object_or_404(Purchase, id=purchase_id)
        purchase_items = PurchaseItem.objects.filter(purchase=purchase).select_related('medication')
        
        context = {
            'purchase': purchase,
            'purchase_items': purchase_items,
            'print_date': timezone.now(),
            'company_name': 'Smart Pharmacy',
            'company_address': 'Yaounde, BP xxx s/c UY1',
            'company_phone': '(237) 698 78 46 67',
        }
        
        # Render the receipt template
        return render(request, 'pharmacy/receipt.html', context)
        
    except Purchase.DoesNotExist:
        return HttpResponse("Purchase not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error generating receipt: {str(e)}", status=500)

@login_required
@require_http_methods(["POST"])
def print_receipt_ajax(request):
    """
    AJAX endpoint for generating receipt content
    """
    try:
        data = json.loads(request.body)
        purchase_id = data.get('id')
        
        if not purchase_id:
            return JsonResponse({'success': False, 'error': 'Purchase ID is required'})
        
        purchase = get_object_or_404(Purchase, id=purchase_id)
        purchase_items = PurchaseItem.objects.filter(purchase=purchase).select_related('medication')
        
        context = {
            'purchase': purchase,
            'purchase_items': purchase_items,
            'print_date': timezone.now(),
            'company_name': 'Smart Pharmacy',
            'company_address': 'Yaounde, BP xxx s/c UY1',
            'company_phone': '(237) 698 78 46 67',
        }
        
        # Render the receipt template to string
        # receipt_html = render_to_string('pharmacy/receipt_content.html', context)
        receipt_html = render_to_string('pharmacy/receipt.html', context)
        
        return JsonResponse({
            'success': True,
            'receipt_html': receipt_html,
            'purchase_id': purchase_id
        })
        
    except Purchase.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Purchase not found'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_http_methods(["GET"])
def print_receipt_pdf(request, purchase_id):
    """
    Generate a PDF receipt (requires reportlab)
    pip install reportlab
    """
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.units import inch
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib import colors
        from io import BytesIO
        
        purchase = get_object_or_404(Purchase, id=purchase_id)
        purchase_items = PurchaseItem.objects.filter(purchase=purchase).select_related('medication')
        
        # Create a BytesIO buffer for the PDF
        buffer = BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Company header
        story.append(Paragraph("<b>Smart Pharmacy</b>", styles['Title']))
        story.append(Paragraph("Yaounde, BP xxx s/c UY1", styles['Normal']))
        story.append(Paragraph("Phone: (237) 698 78 46 67", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Receipt title
        story.append(Paragraph("<b>RECEIPT</b>", styles['Heading1']))
        story.append(Spacer(1, 10))
        
        # Purchase details
        purchase_details = [
            ['Receipt #:', str(purchase.id)],
            ['Date:', purchase.purchase_date.strftime('%Y-%m-%d %H:%M:%S')],
            ['Customer:', purchase.customer_name],
            ['Phone:', purchase.customer_phone or 'N/A'],
            ['Payment:', purchase.get_payment_method_display()],
        ]
        
        details_table = Table(purchase_details, colWidths=[1.5*inch, 3*inch])
        details_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(details_table)
        story.append(Spacer(1, 20))
        
        # Items table
        items_data = [['Item', 'Qty', 'Price', 'Total']]
        for item in purchase_items:
            items_data.append([
                item.medication.name,
                str(item.quantity),
                f'${item.price:.2f}',
                f'${item.price * item.quantity:.2f}'
            ])
        
        # Add total row
        items_data.append(['', '', 'TOTAL:', f'${purchase.total_amount:.2f}'])
        
        items_table = Table(items_data, colWidths=[3*inch, 1*inch, 1*inch, 1*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, -1), (-1, -1), colors.grey),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        story.append(items_table)
        story.append(Spacer(1, 20))
        
        # Footer
        story.append(Paragraph("Thank you for your business!", styles['Normal']))
        story.append(Paragraph(f"Printed on: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        # Get the PDF data
        pdf_data = buffer.getvalue()
        buffer.close()
        
        # Create HTTP response
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="receipt_{purchase_id}.pdf"'
        return response
        
    except ImportError:
        return HttpResponse("PDF generation requires reportlab library. Install it using: pip install reportlab", status=500)
    except Purchase.DoesNotExist:
        return HttpResponse("Purchase not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)