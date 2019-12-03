from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.forms import CharField, EmailField, Form, HiddenInput

from .validators.validators import first_capital_validator, name_validator


class RegisterForm(UserCreationForm):
    first_name = CharField(max_length=30, required=False, help_text='Optional.')
    last_name = CharField(max_length=30, required=False, help_text='Optional.')
    email = EmailField(max_length=254, required=False, help_text='Required. Inform a valid email address.')


class SettingsForm(Form):
    id = CharField(label='Id', widget=HiddenInput(), required=False)
    first_name = CharField(label='First name', max_length=50, validators=[first_capital_validator, name_validator])
    surname = CharField(label='Surname', max_length=50, validators=[first_capital_validator, name_validator])
    email = CharField(label='Email', max_length=50, validators=[validate_email])
