from django.forms import CharField, Form, HiddenInput

from .validators.validators import first_capital_validator, name_validator


class SettingsForm(Form):
    first_name = CharField(label='First name', max_length=100, validators=[first_capital_validator, name_validator])
    surname = CharField(label='Surname', max_length=100, validators=[first_capital_validator, name_validator])
    id = CharField(label='Id', widget = HiddenInput(), required = False)
