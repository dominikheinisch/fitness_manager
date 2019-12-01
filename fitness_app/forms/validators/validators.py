from django.core.validators import RegexValidator

name_validator = RegexValidator(regex=r'^[-a-zA-Z]+\Z', message='only letters and dash are allowed')
first_capital_validator = RegexValidator(regex=r'^[A-Z]', message='start with capital letter')
