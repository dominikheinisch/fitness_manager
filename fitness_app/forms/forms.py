from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.forms import CharField, EmailField, Form, HiddenInput

from .validators.validators import first_capital_validator, name_validator


class RegisterForm(UserCreationForm):
    first_name = CharField(max_length=30, required=False, help_text='Optional.')
    last_name = CharField(max_length=30, required=False, help_text='Optional.')
    email = EmailField(max_length=254, required=False, help_text='Optional.')
    # email = EmailField(max_length=254, required=False, help_text='Required. Inform a valid email address.')


class SettingsForm(Form):
    # id = CharField(label='Id', widget=HiddenInput(), required=False)
    username = CharField(max_length=30, required=False, validators=[name_validator])
    first_name = CharField(max_length=30, required=False, validators=[first_capital_validator, name_validator])
    last_name = CharField(max_length=30, required=False, validators=[first_capital_validator, name_validator])
    email = CharField(max_length=254, required=False, validators=[validate_email])
