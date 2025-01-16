#accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')




def send_verification_email(user, request):
    current_site = get_current_site(request)
    subject = "Activate Your Account"
    message = render_to_string('registration/activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    email = EmailMessage(subject, message, to=[user.email])
    email.send()

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Disable account until verification
            user.save()
            send_verification_email(user, request)
            return render(request, "registration/verification_sent.html")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("login")
    else:
        return render(request, "registration/activation_invalid.html")