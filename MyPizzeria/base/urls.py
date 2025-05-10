from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    #path("gestion-tareas/", views.gestion_tareas, name="gestion_tareas"),
    path("gestion-inventario/", views.add_inventory_item, name="gestion_inventario"),
    path("gestion-usuarios/", views.gestion_usuarios, name="gestion_usuarios"),
    #path("crear-tarea/", views.crear_tarea, name="crear-tarea"),
    #path("mis-tareas/", views.mis_tareas, name="mis-tareas"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("login/", auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('editar-usuario/<int:user_id>/', views.editar_usuario, name='editar-usuario'),
    path("crear-usuario/", views.gestion_crearusuario, name="crear-usuario"),
    #path('editar-tarea/<int:task_id>/', views.editar_tarea, name='editar_tarea'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.add_inventory_item, name='add_inventory_item'),
    path('inventory/edit/<int:item_id>/', views.edit_inventory_item, name='edit_inventory_item'),
    path('inventory/delete/<int:item_id>/', views.delete_inventory_item, name='delete_inventory_item'),
    path('inventory/export_csv/', views.export_inventory_csv, name='export_inventory_csv'),

]
