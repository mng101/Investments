from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Stock, Portfolio

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, Button, Div
from django.forms import TextInput, Textarea


class UserCreateForm(UserCreationForm):
    class Meta:
        # fields = ("username", "email", "password1", "password2")
        fields = ("username", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Login name"
        # self.fields["email"].label = "Email address"


class DateInput(forms.DateInput):
    input_type = 'date'


class StockForm(forms.ModelForm):

    class Meta:
        model = Stock
        # fields = '__all__'
        # fields = ['symbol', 'name', 'industry', 'notes', 'img1', 'img2']
        # fields img1 and img2 were removed from the forms class to avoid the default display
        # of the file path to be uploaded to the image field.
        # The Image content is being copied from the clipboard using the PIL "grabclipboard" function
        #
        fields = ['symbol', 'name', 'industry', 'lseg', 'ibes_mean', 'count', 'quant', 'analyst', 'qty',
                  'ex_div_date', 'dividend', 'frequency', 'currency', 'last_baystreet_entry', 'last_analyst_entry',
                  'avg_cost', 'price', 'fair_value',
                  'notes', 'action', ]

        # Image fields are populated by the PIL "grabimage" functions
        # These fields are not included in the StockForm, since the default handling of an Image Field
        # uploaded from a file, is not suitable for the desired user interaction

        widgets = {
                    # Text area to capture notes recorded for the stock
                    #
                    'notes': Textarea(attrs={'rows': 5}),
                    'action': Textarea(attrs={'rows': 5}),

                    #
                    # Number Input displays spinner in the formfield
                    # 'dividend': forms.NumberInput(attrs={
                    #     'placeholder': '$ 0.00', 'class': 'currency-input'
                    # }),
                    # 'dividend': forms.NumberInput(attrs={'class': "no-spinner"}),
                    #
                    # TextInput does not display the leading '0' for values less that $1.00
                    # 'dividend': forms.TextInput(
                    #     attrs={'inputmode': 'numeric',
                    #            'pattern': '[0-9]*'
                    #     }),
                    #
                    # 'dividend': forms.NumberInput(attrs={
                    'dividend': forms.TextInput(attrs={
                        'step': '0.0001',
                        'style': 'text-align: right'
                    }),
                    'qty': forms.TextInput(attrs={
                        'step': '1',
                        'style': 'text-align: right'
                    }),
                    'avg_cost': forms.TextInput(attrs={
                        'step': '0.001',
                        'style': 'text-align: right'
                    }),
                    'price': forms.TextInput(attrs={
                        'step': '0.001',
                        'style': 'text-align: right'
                    }),
                    'fair_value': forms.TextInput(attrs={
                        'step': '0.001',
                        'style': 'text-align: right',
                    }),

                    'ex_div_date': DateInput(),
                    'last_baystreet_entry': DateInput(),
                    'last_analyst_entry': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Div(
                Column('symbol', css_class='form_group col-1'),
                Column('name', css_class='form_group col-2'),
                Column('industry', css_class='form_group col-2'),
                Column ('lseg', css_class='form_group col-1'),
                Column ('ibes_mean', css_class='form_group col-1'),
                Column ('count', css_class='form_group col-1'),
                Column('quant', css_class='form_group col-1'),
                Column('analyst', css_class='form_group col-1'),
                Column ('qty', css_class='form_group col-1'),
                Column ('avg_cost', css_class='form_group col-1'),
                css_class='row g-2'
            ),
            Div(
                Column('ex_div_date', css_class='form_group col-2'),
                Column('dividend', css_class='form_group col-1'),
                Column('currency', css_class='form_group col-1'),
                Column('frequency', css_class='form_group col-2'),
                Column('last_baystreet_entry', css_class='form_group col-2'),
                Column('last_analyst_entry', css_class='form_group col-2'),
                Column('price', css_class='form_group col-1'),
                Column ('fair_value', css_class='form_group col-1'),
                css_class='row g-2'
            ),
            Div(
                Column('notes', css_class='form_group col-9'),
                Column('action', css_class='form_group col-3'),
                css_class='row g-2'
            ),

            Submit('submit', 'Submit', css_class='mt-2 btn-sm')
        )


class PortfolioForm(forms.ModelForm):

    class Meta:
        model = Portfolio
        fields = ['portfolio_name', 'held_at', 'currency']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Div(
                Column('portfolio_name', css_class='form_group col-2'),
                Column('held_at', css_class='form_group col-3'),
                Column('currency', css_class='form_group col-1'),
                css_class='row g-2'
            ),

            Submit('submit', 'Submit', css_class='mt-2 btn-sm')
        )
