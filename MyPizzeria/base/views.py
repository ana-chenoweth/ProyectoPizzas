from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .forms import UserRegisterForm


@login_required
def home(request):
    return render(request, 'base/home.html')

def register(request):
    print("Vista de registro llamada") 
    print(f"Usuario autenticado: {request.user.is_authenticated}")
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}. Ahora puedes iniciar sesión.')
            return redirect('base:login')
    else:
        form = UserRegisterForm()
        
    return render(request, 'base/register.html', {'form': form})