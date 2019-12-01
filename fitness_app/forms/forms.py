from django.forms import CharField, Form, HiddenInput
from django.core.validators import validate_email

from .validators.validators import first_capital_validator, name_validator


class SettingsForm(Form):
    id = CharField(label='Id', widget=HiddenInput(), required=False)
    first_name = CharField(label='First name', max_length=50, validators=[first_capital_validator, name_validator])
    surname = CharField(label='Surname', max_length=50, validators=[first_capital_validator, name_validator])
    email = CharField(label='Email', max_length=50, validators=[validate_email])
