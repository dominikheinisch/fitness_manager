from django.contrib.auth.forms import UsernameField, UserCreationForm, UserChangeForm
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.forms import CharField, DateField, EmailField, Form, HiddenInput, ModelChoiceField, SelectDateWidget

from .validators.validators import first_capital_validator, name_validator
from ..models import Sport


class RegisterForm(UserCreationForm):
    first_name = CharField(max_length=30, required=False, help_text='Optional.', validators=[first_capital_validator, name_validator])
    last_name = CharField(max_length=30, required=False, help_text='Optional.', validators=[first_capital_validator, name_validator])
    email = EmailField(max_length=254, required=False, help_text='Optional.', validators=[validate_email])


class SettingsForm(Form):
    # id = CharField(label='Id', widget=HiddenInput(), required=False)
    username = CharField(max_length=30, required=False, validators=[name_validator])
    first_name = CharField(max_length=30, required=False, validators=[first_capital_validator, name_validator])
    last_name = CharField(max_length=30, required=False, validators=[first_capital_validator, name_validator])
    email = CharField(max_length=254, required=False, validators=[validate_email])


class ActivityForm(Form):
    def __init__(self, is_to_add=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].required = is_to_add
        self.fields['duration'].required = is_to_add
        self.fields['sport'].required = is_to_add

    date = DateField(widget=SelectDateWidget())
    duration = CharField(max_length=4)
    sport = ModelChoiceField(queryset=Sport.objects.all())
