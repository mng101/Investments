from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, Button, Div

from .models import Stock
# from bootstrap_datepicker_plus.widgets import DatePickerInput


class UserCreateForm(UserCreationForm):
    class Meta:
        # fields = ("username", "email", "password1", "password2")
        fields = ("username", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Login name"
        # self.fields["email"].label = "Email address"


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        # fields = '__all__'
        fields = ['symbol', 'name', 'industry']
        # widgets = {
        #     "exdivdate": DatePickerInput(),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form.action = 'submit_form'

        self.helper.layout = Layout(
            Div(
                Column('symbol', css_class='form_group col-1'),
                Column('name', css_class='form_group col-5'),
                Column('industry', css_class='form_group col-5'),
                css_class='form-row'
            ),

            Submit('submit', 'Submit', css_class='mt-4')

            # self.helper.add_input(Submit('submit', 'Submit')
        )


        # self.helper.add_input(Submit('submit', 'Submit'))

        # )
        # widgets = {
        #     'exdivdate': datepicker(attrs = {
        #         'class': datepicker,
        #         'data-date-format': 'yyyy/mm/dd',
        #     })
        # }

