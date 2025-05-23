from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from workmates.models import workmateUser
from tasks.models import InventoryItem
from .form import WorkmateUserCreationForm, InventoryItemForm
from django.db import models
from django.db.models import Q
import csv
from django.http import HttpResponse
from datetime import date, timedelta

@login_required
def home(request):
    search_query = request.GET.get('search', '')
    inventory_items = InventoryItem.objects.all()
    today = date.today()
    upcoming_expiry_date = today + timedelta(days=5)
    category_totals = InventoryItem.objects.values('item_type').annotate(total_quantity=models.Sum('quantity'))
    low_stock_items = InventoryItem.objects.filter(quantity__lte=5)  # umbral bajo
    expiring_soon_items = InventoryItem.objects.filter(expiry_date__lte=upcoming_expiry_date, expiry_date__gte=today)

    if search_query:
        inventory_items = inventory_items.filter(
            Q(name__icontains=search_query) |
            Q(item_type__icontains=search_query)
        )

    return render(request, 'base.html', {
        'inventory_items': inventory_items,
        'category_totals': category_totals,
        'expiring_soon_items': expiring_soon_items,
        'low_stock_items': low_stock_items,  # variable de bajo stock
        'today': today,
    })

'''
@login_required
def inventory_list(request):
    inventory_items = InventoryItem.objects.all()

    return render(request, "inventory_list.html", {'inventory_items': inventory_items})
'''

@login_required
def add_inventory_item(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            inventory_item = form.save(commit=False)
            inventory_item.added_by = request.user
            inventory_item.save()
            messages.success(request, "Inventory item added successfully!")
            return redirect('base:home')
    else:
        form = InventoryItemForm()
    return render(request, 'add_inventory_item.html', {'form': form})



@login_required
@permission_required('tasks.change_inventoryitem', raise_exception=True)
def edit_inventory_item(request, item_id):
    inventory_item = get_object_or_404(InventoryItem, id=item_id)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=inventory_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inventory item updated successfully!')
            return redirect('base:home')
    else:
        form = InventoryItemForm(instance=inventory_item)
    return render(request, 'edit-inventory-item.html', {'form': form, 'inventory_item': inventory_item})

@login_required
def export_inventory_csv(request):
    # Crear respuesta con tipo de contenido CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Category', 'Quantity', 'Expiry Date', 'Description'])

    for item in InventoryItem.objects.all():
        writer.writerow([
            item.name,
            item.get_item_type_display(),
            item.quantity,
            item.expiry_date,
            item.description
        ])

    return response

@login_required
@permission_required('tasks.delete_inventoryitem', raise_exception=True)
def delete_inventory_item(request, item_id):
    inventory_item = get_object_or_404(InventoryItem, id=item_id)
    if request.method == 'POST':
        inventory_item.delete()
        messages.success(request, "Inventory item deleted successfully!")
        return redirect('base:home')
    return render(request, 'delete-inventory-item.html', {'inventory_item': inventory_item})

@login_required
@permission_required('workmates.view_workmateuser', raise_exception=True)
def gestion_usuarios(request):
    users = workmateUser.objects.all()
    return render(request, "gestion-usuarios.html", {'users': users})


@login_required
@permission_required('workmates.add_workmateuser', raise_exception=True)
def gestion_crearusuario(request):
    if request.method == 'POST':
        form = WorkmateUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect('base:gestion_usuarios')
    else:
        form = WorkmateUserCreationForm()
    return render(request, "crear-usuario.html", {'form': form})


@login_required
@permission_required('workmates.change_workmateuser', raise_exception=True)
def editar_usuario(request, user_id):
    user = get_object_or_404(workmateUser, id=user_id)

    if request.method == 'POST':
        form = WorkmateUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('base:gestion_usuarios')
    else:
        form = WorkmateUserCreationForm(instance=user)

    return render(request, 'editar-usuario.html', {'form': form, 'user': user})

'''
@login_required
def mis_tareas(request):
    filter_category = request.GET.get('category', '')
    filter_priority = request.GET.get('priority', '')
    filter_progress = request.GET.get('progress', '')

    categories = [choice[0] for choice in Tasks.Categories]
    priorities = Tasks.Urgency.choices
    progressing = Tasks.Completion.choices

    mytasks = Tasks.objects.filter(user=request.user)

    if filter_category and filter_category != '':
        mytasks = mytasks.filter(category=filter_category)

    if filter_priority and filter_priority != '':
        mytasks = mytasks.filter(priority=filter_priority)

    if filter_progress and filter_progress != '':
        mytasks = mytasks.filter(progress=filter_progress)

    return render(request, "mis-tareas.html", {
        'mytasks': mytasks,
        'categories': categories,
        'priorities': priorities,
        'progressing': progressing,
        'filter_category': filter_category,
        'filter_priority': filter_priority,
        'filter_progress': filter_progress
    })


@login_required
def crear_nueva_tarea(request):
    return render(request, "crear-nueva-tarea.html", {})
'''