from django import forms
from django.contrib.auth import get_user_model,authenticate
User = get_user_model()
from django.db.models import Q
from captcha.fields import CaptchaField

class SignUpForm(forms.ModelForm):
    email  = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'email_input'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'id':'username_input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'password_input'}))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')

        user_exists = User.objects.filter(Q(email=email) | Q(username=username)).first()

        if user_exists:
            if user_exists.email == email:
                self.add_error('email', "A user with this email already exists!")
            if user_exists.username == username:
                self.add_error('username', "This username is taken!")

        return cleaned_data
    
class LoginForm(forms.Form):
    email  = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'email_input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'password_input'}))
    # captcha = CaptchaField()
    def clean(self):
        
        cleaned_data= super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        cleaned_data['user'] = user
        if user is None:
            raise forms.ValidationError("Invalid email or password!")
        return cleaned_data