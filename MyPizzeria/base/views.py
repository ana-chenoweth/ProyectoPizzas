from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .forms import UserRegisterForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode

@login_required
def home(request):
    return render(request, 'base/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Desactiva la cuenta hasta que se confirme el correo
            user.save()

            # Generar el token y el enlace de activación
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = request.build_absolute_uri(f'/activate/{uid}/{token}/')

            # Enviar el correo de activación
            subject = 'Activate your account'
            message = render_to_string('base/activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            send_mail(subject, message, 'noreply@example.com', [user.email])

            messages.success(request, 'Please check your email to activate your account.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'base/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')