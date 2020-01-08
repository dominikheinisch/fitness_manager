import datetime

from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import CharField, DateField, DateInput, DateTimeField, DateTimeInput, EmailField, Form, \
    IntegerField, ModelChoiceField, ModelForm, NumberInput, Select, TextInput, ValidationError

from .validators.validators import first_capital_validator, name_validator
from ..models import Activity, Food, Goals, Sport


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('password1', 'password2', 'first_name', 'last_name', 'email')

    first_name = CharField(required=False, help_text='Optional.', validators=[first_capital_validator, name_validator])
    last_name = CharField(required=False, help_text='Optional.', validators=[first_capital_validator, name_validator])
    email = EmailField(required=False, help_text='Optional.')


class SettingsForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    password = None
    first_name = CharField(required=False, help_text='Optional.', validators=[first_capital_validator, name_validator])
    last_name = CharField(required=False, help_text='Optional.', validators=[first_capital_validator, name_validator])


class GoalsForm(ModelForm):
    daily_calories = IntegerField(min_value=1, max_value=9999, widget=NumberInput(attrs={'placeholder': "kcal"}))
    daily_proteins = IntegerField(min_value=1, max_value=9999, widget=NumberInput(attrs={'placeholder': "grams"}))
    daily_carbs = IntegerField(min_value=1, max_value=9999, widget=NumberInput(attrs={'placeholder': "grams"}))
    daily_fats = IntegerField(min_value=1, max_value=9999, widget=NumberInput(attrs={'placeholder': "grams"}))

    class Meta:
        model = Goals
        exclude = ['user']


class ActivityForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Activity
        exclude = ['User']

    date = DateField(required=False,
                     initial=datetime.date.today().strftime('%m/%d/%Y'),
                     widget=DateInput(attrs={'class': "form-control datepicker"}))
    duration = IntegerField(required=False,
                            min_value=1,
                            max_value=999,
                            widget=NumberInput(attrs={'class': "form-control", 'placeholder': "minutes"}))
    Sport = ModelChoiceField(required=False,
                             queryset=Sport.objects.all().order_by('name'),
                             empty_label='choose sport',
                             widget=Select(attrs={'class': "form-control"}))

    def clean_date(self):
        return check_not_empty(self, filed_name='date')

    def clean_duration(self):
        return check_not_empty(self, filed_name='duration')

    def clean_sport(self):
        return check_not_empty(self, filed_name='sport')


class FromToDateForm(Form):
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


class MealDateTimeForm(Form):
    date_time = DateTimeField(required=False,
                              input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'],
                              help_text='input eg. YYYY-mm-dd HH:MM',
                              widget=DateTimeInput(attrs={'type': 'datetime-local', 'class': 'modalToClear'}))

    def clean_date_time(self):
        return check_not_empty(self, filed_name='date_time')


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

    # TODO check why its not needed, probably its default for formset (for only one of two fields filled)
    # def clean_food(self):
    #     return check_not_empty(self, filed_name='food')
    #
    # def clean_weight(self):
    #     return check_not_empty(self, filed_name='weight')

    def is_fullfilled(self):
        return len(self.cleaned_data) == len(self.fields)


class PortionsForm(AddPortionForm):
    calories = CharField(disabled=True, required=False, initial=0)
    carbohydrates = CharField(disabled=True, required=False, initial=0)
    fats = CharField(disabled=True, required=False, initial=0)
    proteins = CharField(disabled=True, required=False, initial=0)


class MealTimeForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_to_highlight = False

    time = CharField(disabled=True, widget=TextInput(attrs={'type': 'hidden'}))
    id = IntegerField(disabled=True, widget=NumberInput(attrs={'type': 'hidden'}))


class MetadataForm(Form):
    current_meal_id = IntegerField(widget=NumberInput(attrs={'type': 'hidden'}))


def check_not_empty(self, filed_name):
    field = self.cleaned_data.get(filed_name)
    if field is None:
        self.add_error(field=filed_name, error=ValidationError('Field is required'))
    return field
