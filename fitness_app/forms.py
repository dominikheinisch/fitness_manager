from django.core.validators import _lazy_re_compile, RegexValidator
from django.forms import CharField, Form, HiddenInput


string_validator = RegexValidator(regex=_lazy_re_compile(r'^[-a-zA-Z]+\Z'), message='only letters and dash are allowed')


class SettingsForm(Form):
    first_name = CharField(label='First name', max_length=100, validators=[string_validator])
    surname = CharField(label='Surname', max_length=100, validators=[string_validator])
    id = CharField(label='Id', widget = HiddenInput(), required = False)
