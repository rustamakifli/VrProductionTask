from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import UpdatePersonalInfoForm,LoginForm,ContactForm,RegisterForm
from django.contrib.auth import logout as django_logout
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from users.models import Contact
from django.views.generic import CreateView
from django.contrib import messages


User = get_user_model()

# Create your views here.
@login_required
def account(request):
    # user = User.objects.filter(user=request.user).first()
    print(request.user.sex)
    form_pers_info = UpdatePersonalInfoForm()
    # print(form_pers_info)
    if request.method == 'POST':
        if request.POST.get('submit') == 'personal_info_submit':
            form_pers_info = UpdatePersonalInfoForm(data=request.POST,instance=request.user)
            if form_pers_info.is_valid():
                request.user.first_name = request.POST.get('first_name')
                request.user.last_name = request.POST.get('last_name')
                request.user.email = request.POST.get('email')
                request.user.birthdate = request.POST.get('birthdate')
                request.user.sex = request.POST.get('sex')
                request.user.save()
                return redirect(reverse_lazy('account'))
    context = {       
        'form_pers_info':form_pers_info,
    } 
    if request.user.is_authenticated:
        return render(request, "profile.html",context)
    return render(request, "login.html")

@login_required
def logout(request):
    django_logout(request)
    return redirect('blogs')

class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = LoginForm()

        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blogs')
        return super().dispatch(request, *args, **kwargs)
    
class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    context_object_name = 'reg_form'

    def form_invalid(self, form) :
        print(form.errors)
        return super().form_invalid(form)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        print(user)
        form.instance.set_password(form.cleaned_data['password'])
        user.save()
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reg_form'] = RegisterForm()

        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
class ContactView(CreateView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, 'Mesajiniz qeyde alindi!')
        return result