from django import forms
from .models import Statement
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class AnwserProposeForm(forms.Form):
    text = forms.CharField(
        label='Tekst odpowiedź'
    )
    make_new_statement = forms.BooleanField(
        required=False,
        label='Nowa wypowiedź'
    )
    new_statement = forms.CharField(
        label="Tekst nowej odpowiedzi",
        widget=forms.Textarea,
        required=False
    )
    goto_statement = forms.CharField(
        label="ID wypowiedzi",
        max_length=128,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Znajdziejsz na dole strony'
            }
        )
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={'data-callback': 'enableSubmit'}
        )
    )
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("captcha"):
            raise forms.ValidationError("Sprawdź czy nie jesteś robotem :)")

        make_new_statement = cleaned_data.get("make_new_statement")
        if make_new_statement:
            new_statement = cleaned_data.get("new_statement")
            if len(new_statement) < 1:
                raise forms.ValidationError("Jeśli wybrano nowe zdanie to należy je podać")
        else:
            try:
                goto_statement = cleaned_data.get("goto_statement")
                s = Statement.objects.get(id=goto_statement)
            except Exception as e:
                raise forms.ValidationError("W trakcie odnajdywania zdania napotkono błąd: {}".format(e))
