from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.decorators import otp_required
from .models import Statement

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        otp_token = request.POST.get('otp_token')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # ✅ Attempt to verify 2FA token
            devices = devices_for_user(user, confirmed=True)
            for device in devices:
                if device.verify_token(otp_token):
                    request.session['otp_device_id'] = device.persistent_id
                    
                    send_mail(
                        subject='City Trust Bank Login Alert',
                        message=f'Hello {user.username},\n\nYou just signed in to your account from {request.META.get("REMOTE_ADDR")}.',
                        from_email=None,  # Optional: configure in settings.py
                        recipient_list=[user.email],
                        fail_silently=True,
                    )
                    return redirect('dashboard')

            logout(request)  # 🚨 Log out user if 2FA fails after login
            return render(request, 'accounts/login.html', {'error': 'Invalid 2FA code'})
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

    return render(request, 'accounts/login.html')


@otp_required
def user_dashboard(request):
    statements = Statement.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'accounts/dashboard.html', {'statements': statements})


def user_logout(request):
    logout(request)
    return redirect('login')
