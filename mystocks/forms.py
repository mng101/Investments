from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, Button, Div
from django.forms import TextInput, Textarea

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


class Row(Div):
    css_class = 'row g-3'


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        # fields = '__all__'
        fields = ['symbol', 'name', 'industry', 'dividend', 'currency', 'frequency', 'exdivdate',
                  'lseg_score', 'ibes_mean', 'no_of_analysts', 'fair_value', 'ms_quant', 'ms_analyst',
                  'notes']
        widgets = {
                    # The TextInput widget removed the default up-down arrows displayed in IntergerFields
                    #
                    'lseg_score': TextInput(),
                    'no_of_analysts': TextInput(),
                    'fair_value': TextInput(),
                    'dividend': TextInput(),

                    # Text area to capture notes recorded for the stock
                    #
                    'notes': Textarea(attrs={'rows':5, 'cols':20})
        }

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
            Div(
                Column('lseg_score', css_class='form_group col-1'),
                Column('ibes_mean', css_class='form_group col-1'),
                Column('no_of_analysts', css_class='form_group col-1'),
                Column('fair_value', css_class='form_group col-1'),
                Column('ms_quant', css_class='form_group col-1'),
                Column('ms_analyst', css_class='form_group col-1'),
                Column('dividend', widget=forms.TextInput(), css_class='form_group col-1'),
                Column('currency', css_class='form_group col-1'),
                Column('frequency', css_class='form_group col-2'),
                Column('exdivdate', css_class='form_group col-2'),
                css_class='form-row'
            ),
            Div(
                Column('notes'),
                css_class='form-row'
            ),

            Submit('submit', 'Submit', css_class='mt-4')
        )

        # )
        # widgets = {
        #     'exdivdate': datepicker(attrs = {
        #         'class': datepicker,
        #         'data-date-format': 'yyyy/mm/dd',
        #     })
        # }

