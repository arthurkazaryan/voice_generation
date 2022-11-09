from django import forms


def get_audio_samples():
    samples = [('none', '-- Select a sample --')]
    for name in ['0', '1', '2', '3', '4', '5', '6']:
        samples.append((name, name))
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
