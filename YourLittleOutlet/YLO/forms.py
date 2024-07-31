from django import forms
from YLO.models import *
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

        widgets = {
            'Category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['Category'].initial = 1

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

class CustomerForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    class Meta:
        model = Customer
        fields = ['profile_pic', 'user', 'gender', 'contact', 'state', 'city', 'pincode', 'address']
        widgets = {
            'user': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].disabled = True
        self.fields['user'].widget = forms.HiddenInput()  

    def clean_password(self):
        password = self.cleaned_data['password']
        user = self.instance.user
        if not user.check_password(password):
            raise forms.ValidationError('Incorrect password. Profile update failed.')
        return password

    def clean_user(self):
        return self.instance.user

class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    contact = forms.CharField(max_length=15, required=False)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        contact = cleaned_data.get('contact')

        user_query = User.objects.filter(username=username, email=email)

        if contact:
            user_query = user_query.filter(customer__contact=contact)

        user = user_query.first()

        if not user:
            raise forms.ValidationError('User not found. Please check your credentials.')

        return cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        new_password = self.cleaned_data['new_password']

        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Enter your password")