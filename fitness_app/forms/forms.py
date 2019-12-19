import datetime

from django.contrib.auth.forms import UsernameField, UserCreationForm, UserChangeForm
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.forms import CharField, DateField, DateInput, DateTimeField, DateTimeInput, EmailField, Form, \
    IntegerField, ModelChoiceField, NumberInput, Select, ValidationError

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

    from_date = DateField(widget=DateInput(attrs={'class': "form-control onClickDatepicker"}))
    to_date = DateField(widget=DateInput(attrs={'class': "form-control onClickDatepicker"}))
    date = DateField(initial=datetime.date.today().strftime('%m/%d/%Y'),
                     widget=DateInput(attrs={'class': "form-control datepicker"}))
    duration = IntegerField(min_value=1, max_value=999,
                            widget=NumberInput(attrs={'class': "form-control", 'placeholder': "minutes"}))
    sport = ModelChoiceField(queryset=Sport.objects.all(), empty_label='choose sport',
                             widget=Select(attrs={'class': "form-control"}))

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        if from_date and to_date and from_date > to_date:
            self.add_error(field='to_date', error=ValidationError('"To" date cannot be earlier than "From" date'))
        return cleaned_data


class MealForm(Form):
    from_date = DateField(widget=DateInput(attrs={'class': "form-control onClickDatepicker"}))
    to_date = DateField(widget=DateInput(attrs={'class': "form-control onClickDatepicker"}))

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        if from_date and to_date and from_date > to_date:
            self.add_error(field='to_date', error=ValidationError('"To" date cannot be earlier than "From" date'))
        return cleaned_data


class AddMealForm(Form):
    date_time = DateTimeField(required=False,
                              help_text='input YYYY-mm-dd HH:MM',
                              widget=DateTimeInput(attrs={'type': 'datetime-local', 'class': 'modalToClear'}))

    def clean(self):
        self.are_fields_filled = True

    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')
        print(date_time)
        if date_time is None:
            self.are_fields_filled = False
            self.add_error(field='date_time', error=ValidationError('Field is required'))
