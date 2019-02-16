from django import forms
from .models import User


class UserCreationForm(forms.ModelForm):
    CHOICES = (('m', 'Male',), ('f', 'Female',))
    sex       = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
   
    class Meta:
        model = User
        fields =('f_name', 'm_name', 'l_name', 'u_name', 'email', 'phone', 'sex', 'role')

        widgets = {
            "role": forms.CheckboxSelectMultiple(attrs={ '{% if f.choice_label =': 'student', '%} data-toggle': 'collapse', 'data-target': '#collapseroom'
            ,'{% endif %} class': 'box'
            }),
        }
        
        help_texts = {}

        requireds = {}
        
    def clean_f_name(self):
        f_name = self.cleaned_data.get("f_name")     
        if f_name:
           f_name = f_name[0].upper()+f_name[1:].lower()
        return f_name
    
    def clean_m_name(self):
        m_name = self.cleaned_data.get("m_name")
        if m_name:
           m_name = m_name[0].upper()+m_name[1:].lower()
        return m_name
    
    def clean_l_name(self):
        l_name = self.cleaned_data.get("l_name")      
        if l_name:
           l_name = l_name[0].upper()+l_name[1:].lower()
        return  l_name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            email = email.lower()
            if User.objects.filter(email=email).exclude(u_name=self.cleaned_data['u_name']):
                raise forms.ValidationError("User with this Email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if len(phone) > 8:
            phone = '+251'+phone[len(phone)-9:]
        return phone
    
    def clean_u_name(self):
        u_name = self.cleaned_data.get("u_name")
        if u_name:
            u_name = u_name.lower()
        return u_name

    def clean_role(self):
        role = self.cleaned_data.get("role") 
        r = [r.r_name for r in role]
        print(role)    
        if 'student' in r and ('admin' in r or 'teacher' in r):
           raise forms.ValidationError("Role student and (admin or teacher) was not alowed.")
        return role

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password('risu')
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    CHOICES = (('m', 'Male',), ('f', 'Female',))
    sex       = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    def __init__(self, *args, **kwargs):
        self._id = kwargs.pop('id', None)
        super(UserChangeForm,self).__init__(*args, **kwargs)

    class Meta:
        model = User
        exclude = ['last_login', 'password', 'is_admin', 'img']

        widgets = {
            "role": forms.CheckboxSelectMultiple(),
        }

    def clean_f_name(self):
        f_name = self.cleaned_data.get("f_name")     
        if f_name:
           f_name = f_name[0].upper()+f_name[1:].lower()
        return f_name
    
    def clean_m_name(self):
        m_name = self.cleaned_data.get("m_name")
        if m_name:
           m_name = m_name[0].upper()+m_name[1:].lower()
        return m_name
    
    def clean_l_name(self):
        l_name = self.cleaned_data.get("l_name")      
        if l_name:
           l_name = l_name[0].upper()+l_name[1:].lower()
        return  l_name

    def clean_email(self):
        email = self.cleaned_data.get("email")      
        if email:
            email = email.lower()
            if User.objects.filter(email=email).exclude(pk=self._id):
                raise forms.ValidationError("User with this Email already exists.")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if len(phone) > 8:
            phone = '+251'+phone[len(phone)-9:]
        return phone
    
    def clean_u_name(self):
        u_name = self.cleaned_data.get("u_name")
        if u_name:
            u_name = u_name.lower()
        return u_name

class UserCreationExel(forms.Form):
    exelfile = forms.FileField(label="Upload File", help_text="admin student teacher family")

    def clean_exelfile(self):
        exelfile = self.cleaned_data.get("exelfile")  
        
        if str(exelfile)[-4:] != '.csv':
            raise forms.ValidationError("This file was not exel(.csv).")
        return exelfile

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('city', 'subcity', 'wereda', 'home_number', 'place_of_birth', 'date_of_birth', 'disablity', 'img')

        