import datetime

from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import UsernameField, UserCreationForm, UserChangeForm
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.forms import CharField, DateField, DateInput, DateTimeField, DateTimeInput, EmailField, Form, \
    IntegerField, ModelChoiceField, NumberInput, Select, TextInput, ValidationError

from .validators.validators import first_capital_validator, name_validator
from ..models import Food, Sport


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
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    from_date = DateField(widget=DateInput(attrs={'class': "form-control onClickDatepicker"}))
    to_date = DateField(widget=DateInput(attrs={'class': "form-control onClickDatepicker"}))
    date = DateField(initial=datetime.date.today().strftime('%m/%d/%Y'),
                     widget=DateInput(attrs={'class': "form-control datepicker"}))
    duration = IntegerField(min_value=1, max_value=999,
                            widget=NumberInput(attrs={'class': "form-control", 'placeholder': "minutes"}))
    sport = ModelChoiceField(queryset=Sport.objects.all().order_by('name'),
                             empty_label='choose sport',
                             widget=Select(attrs={'class': "form-control"}))

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        if from_date and to_date and from_date > to_date:
            self.add_error(field='to_date', error=ValidationError('"To" date cannot be earlier than "From" date'))
        return cleaned_data


class MealForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

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
                              input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'],
                              help_text='input eg. YYYY-mm-dd HH:MM',
                              widget=DateTimeInput(attrs={'type': 'datetime-local', 'class': 'modalToClear'}))

    def clean(self):
        self.are_fields_filled = True

    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')
        if date_time is None:
            self.are_fields_filled = False
            self.add_error(field='date_time', error=ValidationError('Field is required'))
        return date_time


class AddPortionForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    food = ModelChoiceField(queryset=Food.objects.all().order_by('name'),
                            empty_label='choose food',
                            widget=Select(attrs={'class': "form-control"}))

    weight = IntegerField(min_value=1, max_value=9999,
                          widget=NumberInput(attrs={'class': "form-control", 'placeholder': "grams"}))

    def clean_food(self):
        food = self.cleaned_data.get('food')
        if food is None:
            self.add_error(field='date_time', error=ValidationError('Field is required'))
        return food

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight is None:
            self.add_error(field='date_time', error=ValidationError('Field is required'))
        return weight

    def is_fullfilled(self):
        return len(self.cleaned_data) == len(self.fields)


class PortionsForm(AddPortionForm):
    calories = CharField(disabled=True, required=False, initial=0)


class MealTimeForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_to_highlight = False

    time = CharField(disabled=True, widget=TextInput(attrs={'type': 'hidden'}))
    id = IntegerField(disabled=True, widget=NumberInput(attrs={'type': 'hidden'}))


class MetadataForm(Form):
    current_meal_id = IntegerField(widget=NumberInput(attrs={'type': 'hidden'}))
