from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login as auth_login
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User
from smapp.settings import EMAIL_HOST_USER

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)), #.decode()
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail( mail_subject, message, EMAIL_HOST_USER, [to_email] )

            #email = EmailMessage(
                        #mail_subject, message, EMAIL_HOST_USER, to=[to_email]
            #)
            #email.send()
            user.save()
            return HttpResponse('Please confirm your email address to complete the registration')
            #auth_login(request, user)
            #return redirect('courses')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

##https://frfahim.github.io/post/django-registration-with-confirmation-email/
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')