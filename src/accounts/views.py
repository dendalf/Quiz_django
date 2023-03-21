from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.views import LogoutView
from django.core.signing import BadSignature
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView
from django.views.generic import UpdateView

from .apps import user_register
from .forms import UserRegisterForm, UserUpdateForm, UserPasswordChangeForm, UserSendVerificationForm
from .utils import signer


class UserRegisterView(CreateView):
    model = get_user_model()
    template_name = 'accounts/user_register.html'
    success_url = reverse_lazy('accounts:register_done')
    form_class = UserRegisterForm


class UserSendVerificationView(FormView):
    model = get_user_model()
    template_name = 'accounts/send_verification.html'
    success_url = reverse_lazy('accounts:register_done')
    form_class = UserSendVerificationForm


def user_send_verification(request):
    if request.method == 'GET':
        form = UserSendVerificationForm()
    elif request.method == 'POST':
        form = UserSendVerificationForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(get_user_model(), email=form.cleaned_data['email'])
            user_register.send(get_user_model(), instance=user)
            return HttpResponseRedirect(reverse('accounts:register_done'))

    return render(
        request=request,
        template_name='accounts/send_verification.html',
        context={
            'form': form,
        }
    )


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'accounts/bad_signature.html')

    user = get_object_or_404(get_user_model(), username=username)
    if user.is_activated:
        template = 'accounts/user_is_activated.html'
    else:
        template = 'accounts/user_activation_done.html'
        user.is_activated = True
        user.is_active = True
        user.save()

    return render(request, template)


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/user_logout.html'


@login_required
def user_profile_view(request):
    return render(request, 'accounts/user_profile.html')


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/user_profile_update.html'
    model = get_user_model()
    success_url = reverse_lazy('accounts:profile')
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        return self.request.user


class AccountChangePasswordView(PasswordChangeView):
    model = get_user_model()
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('accounts:change_done')
    template_name = 'accounts/password_change.html'


class AccountChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'

