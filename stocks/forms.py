from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Stock

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


class StockForm(forms.ModelForm):

    class Meta:
        model = Stock
        # fields = '__all__'
        # fields = ['symbol', 'name', 'industry', 'notes', 'img1', 'img2']
        # fields img1 and img2 were removed from the forms class to avoid the default display
        # of the file path to be uploaded to the image field.
        # The Image content is being copied from the clipboard using the PIL "grabclipboard" function
        #
        fields = ['symbol', 'name', 'industry', 'notes']
        widgets = {
                    # Text area to capture notes recorded for the stock
                    #
                    'notes': Textarea(attrs={'rows': 5, 'cols': 20})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Div(
                Column('symbol', css_class='form_group col-1'),
                Column('name', css_class='form_group col-5'),
                Column('industry', css_class='form_group col-5'),
                css_class='form-row'
            ),
            Div(
                Column('notes'),
                css_class='form-row'
            ),
            # Div(
            #     Column('img1'),
            #     css_class='form-row'
            # ),
            # Div(
            #     Column('img2'),
            #     css_class='form-row'
            # ),

            Submit('submit', 'Submit', css_class='mt-2')
        )
