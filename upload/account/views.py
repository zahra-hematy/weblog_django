from django.shortcuts import render
from .models import User
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
                ListView,
                CreateView, 
                UpdateView,
                DeleteView
            )     
from django.http import HttpResponse
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
import django
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage  

from django.contrib.auth.views import LoginView, PasswordChangeView
from blog.models import Articlemodel
from django.urls import reverse_lazy
from .mixins import (
        FieldsMixin, 
        FormValidMixin, 
        AuthorAccessMixin,
        SuperAccessMixin,
        AuthorsAccessMixin,
    )
from django.contrib import messages

# Create your views here.

class ArticleList(AuthorsAccessMixin,  ListView):
    # queryset = Articlemodel.objects.all()
    template_name = 'registration/home.html'

    def get_queryset(self) :
        if self.request.user.is_superuser:
            return Articlemodel.objects.all()
        else:
             return Articlemodel.objects.filter(author=self.request.user)

# @login_required
# def home(request):
#     return render(request, 'registration/home.html')
class ArticleCreate(AuthorsAccessMixin,FormValidMixin, FieldsMixin, CreateView):
    model = Articlemodel
    template_name = 'registration/article_create_update.html'

class ArticleUpdate(AuthorAccessMixin,FormValidMixin, FieldsMixin, UpdateView):
    model = Articlemodel
    template_name = 'registration/article_create_update.html'
    success_url = reverse_lazy('account:profile')

class ArticleDelete(SuperAccessMixin, DeleteView):
    model = Articlemodel
    success_url = reverse_lazy('account:home')
    template_name = 'registration/article_confirm_delete.html'

class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('account:profile')
    def get_object(self):
        return User.objects.get(pk = self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_author:
            return reverse_lazy("account:home")
        else:
            return reverse_lazy('account:Profile')

# class PasswordChange(PasswordChangeView):
#     success_url = reverse_lazy('account:password_change_done')

class Register(CreateView):
    form_class = SignupForm
    template_name = 'registration/register.html'
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('registration/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
        email.send()
        return HttpResponse('لینک فعالسازی به ایمیل شما ارسال شد.<a href="{% url login %}">ورود</a>')

        

# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = 'Activate your blog account.'
#             message = render_to_string('acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                         mail_subject, message, to=[to_email]
#             )
#             email.send()
#             return HttpResponse('Please confirm your email address to complete the registration')
#     else:
#         form = SignupForm()
#     return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponse('اکانت شما با موفقیت فعال شد برای ورود کلیک کنید<a href="login/">کلیک</a>کنید you can login your account.')
    else:
        return HttpResponse('لینک فعالسازی منقضی شده است <a href="/registration">دوباره امتحان کنید</a>')