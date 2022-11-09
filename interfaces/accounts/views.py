from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView
from django.shortcuts import render
from accounts.forms import RegistrationForm, LoginForm
from generation.utils import post_generation, get_generation_audio, get_generation_status
from interfaces.utils import DataMixin
from generation.forms import SendGenerationForm
from generation.models import AudioFile
from pathlib import Path
from time import sleep
import requests
import uuid

from interfaces_project.settings import MEDIA_ROOT


class RegisterUser(DataMixin, CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts-home')

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(current_page='accounts-register')

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):

        user = form.save()
        login(self.request, user)

        return redirect('accounts-home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(current_page='accounts-login')

        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):

        return reverse_lazy('accounts-home')


def logout_user(request):
    logout(request)
    return redirect('accounts-login')


class ProfilePage(DataMixin, TemplateView, LoginRequiredMixin):
    template_name = 'accounts/accounts.html'

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(self.get_login_url()))

        send_generation_form = SendGenerationForm

        voices = AudioFile.objects.filter(user=request.user)

        context = self.get_user_context(
            current_page='accounts-home',
            user=request.user,
            send_generation_form=send_generation_form,
            voices=voices
        )

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        send_generation_form = SendGenerationForm(request.POST)
        if send_generation_form.is_valid():
            data = send_generation_form.cleaned_data
            if data['select_voice'] != 'none':
                audio_file = AudioFile(
                    user=request.user,
                    voice=data['select_voice'],
                    status='PENDING',
                    text=data['text'],
                )
                # audio_file.save()

                try:
                    post_request = post_generation(text=data['text'], voice=data['select_voice'])
                    api_status = post_request.json()['status']
                    api_task_id = post_request.json()['task_id']

                    ready = False

                    while not ready:
                        status = get_generation_status(api_task_id)
                        status_data = status.json()
                        audio_file.status = status_data['status']
                        if 200 <= status.status_code < 300 and status_data['status'] == 'REVOKED':
                            ready = True
                            audio_file.save()
                        elif 200 <= status.status_code < 300 and status_data['status'] == 'SUCCESS':
                            file_suffix = Path(status_data['result']['file_path']).suffix
                            target_path = Path('generation', 'audio_created', str(uuid.uuid4()) + file_suffix)
                            request_file = get_generation_audio(audio_path=status_data['result']['file_path'])
                            with open(str(MEDIA_ROOT.joinpath(target_path)), 'wb') as target_audio:
                                target_audio.write(request_file.content)
                            audio_file.audio = str(target_path)
                            ready = True
                        elif status.status_code > 400 or status_data['status'] in ['NOT FOUND', 'FAILED']:
                            audio_file.save()
                        sleep(3)
                    messages.success(request, f'Audiofile has been successfully created.')
                except:
                    messages.error(request, f'Error occured when requesting to server.')
                else:
                    messages.success(request, f'Audiofile has been successfully created.')
            else:
                messages.error(request, f'Error occurred while validating forms. Check your input data.')

        return HttpResponseRedirect(reverse('accounts-home'))
