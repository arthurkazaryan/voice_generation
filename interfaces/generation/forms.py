from django import forms
from interfaces_project.settings import MEDIA_URL
from generation.models import AudioSamples
from settings import DJANGO_HOST, DJANGO_PORT


def get_audio_samples():
    samples = [('none', '-- Select a sample --')]
    audio_samples = AudioSamples.objects.filter(visible=True)
    if audio_samples.exists():
        samples.extend(
            [(f'http://{DJANGO_HOST}:{DJANGO_PORT}{MEDIA_URL}{str(aud_sample.audio)};{aud_sample.name}',
              aud_sample.title) for aud_sample in audio_samples])
    return samples


class SendGenerationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SendGenerationForm, self).__init__(*args, **kwargs)
        self.fields['select_voice'].choices = get_audio_samples()

    select_voice = forms.ChoiceField(label='Select voice', widget=forms.Select(
        attrs={'class': 'input-form form-middle', 'autofocus': True}
    ))
    text = forms.CharField(max_length=2048, widget=forms.Textarea(
        attrs={'cols': '', 'rows': '3', 'class': 'input-form form-middle', 'autofocus': True, 'style': 'resize: none'}
    ))
