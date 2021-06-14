from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterForm(ModelForm):
    name = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['name', 'phone', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        email = cleaned_data['email']
        phone = cleaned_data['phone']
        password = cleaned_data['password']

        if len(phone) != 10:
            self.add_error(
                'phone', 'Phone number must be 10 digit.'
            )

        if len(password) < 8:
            self.add_error(
                'password', 'Password is too short. It must contain at least 8 character.'
            )

        if User.objects.filter(email=email).count():
            self.add_error('email', "User with this Email already exists.")

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        user = User(username=cleaned_data['email'].split('@')[0],
                    phone=cleaned_data['phone'],
                    email=cleaned_data['email'],
                    first_name=cleaned_data['name'].split(' ')[0],
                    last_name=cleaned_data['name'].split(' ')[-1],)
        user.set_password(cleaned_data['password'])
        user.save()


class LoginForm(forms.Form):
    phone = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        phone = cleaned_data['phone']
        password = cleaned_data['password']

        if not User.objects.filter(phone=phone).count():
            self.add_error('phone', "Wrong phone no.")

        elif not User.objects.filter(phone=phone).first().check_password(password):
            self.add_error(
                'password', 'Wrong passowrd.'
            )

        return cleaned_data


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    cnf_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        current_password = cleaned_data['current_password']
        password = cleaned_data['password']
        cnf_password = cleaned_data['cnf_password']

        if not self.user.check_password(current_password):
            self.add_error(
                'currentPassword', 'Wrong password.')

        if len(password) < 8:
            self.add_error(
                'password', 'Password is too short. It must contain at least 8 character.')

        elif password != cnf_password:
            self.add_error(
                'cnf_password', "Password and Confirm Password must match!")

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        self.user.set_password(cleaned_data['password'])
        self.user.save()


class EditProfileForm(forms.Form):
    name = forms.CharField(required=False)
    bio = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'rows': 5}))
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    profile_pic = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(EditProfileForm, self).clean()
        email = cleaned_data['email']
        phone = cleaned_data['phone']

        if len(phone) and len(phone) != 10:
            self.add_error(
                'phone', 'Phone number must be 10 digit.'
            )

        if self.user.phone != phone:
            if User.objects.filter(phone=phone).count():
                self.add_error(
                    'phone', "User with this Phone number already exists.")

        if self.user.email != email:
            if User.objects.filter(email=email).count():
                self.add_error('email', "User with this Email already exists.")

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        profile_pic = cleaned_data['profile_pic']
        self.user.username = cleaned_data['email'].split('@')[0]
        self.user.first_name = cleaned_data['name'].split(' ')[0]
        self.user.last_name = cleaned_data['name'].split(' ')[1]
        self.user.bio = cleaned_data['bio']
        if profile_pic and self.user.profile_pic != profile_pic:
            self.user.profile_pic = profile_pic
        self.user.phone = cleaned_data['phone']
        self.user.email = cleaned_data['email']
        self.user.save()
