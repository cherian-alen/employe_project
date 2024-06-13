from django import forms
from django.forms import ModelForm
from .models import *



class LoginForm(ModelForm):
    class Meta:
        model=Register
        fields=['username','password']  
        help_texts = {
            'username' : None
        }



class StaffAddForm(ModelForm):
    ROLE_CHOICES = (
        ('Select','Select'),
        ('Manager', 'Manager'),
        ('Staff', 'Staff')
    )
    Dep = (
        ('Select','Select'),
        ('Engineering', 'Engineering'),
    )
    
    role = forms.ChoiceField(choices=ROLE_CHOICES)  

    # Dropdown for role
    
    class Meta:
        model = Register
        fields = ['username', 'email', 'contact', 'role', 'password','registrationid']
        widgets = {
            "username": forms.TextInput(attrs={'class': 'reg-form'}),
            "contact": forms.TextInput(attrs={'class': 'reg-form'}),
            "password": forms.TextInput(attrs={'class': 'reg-form', 'type': 'password'}),
            "registrationid": forms.TextInput(attrs={'class':'reg-form'}),

        }    
        help_texts = {
            'username': None
        } 
        
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.attrs['class'] = 'reg-form' 
        
        
class StaffEditForm(ModelForm):
    
    ROLE_CHOICES = (
        ('Select','Select'),
        ('Manager', 'Manager'),
        ('Staff', 'Staff')
    )
    
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['role'].widget.attrs['class'] = 'reg-form'
            
    class Meta:
        model = Register
        fields = ['name','email','contact','role','Department','registrationid']
        widgets = {
            "contact" : forms.TextInput(attrs={'class':'reg-form '}),

            "registrationid" : forms.TextInput(attrs={'class':'reg-form '}),
        }    
        help_texts = {
            'username' : None
        }

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
class ProjectAddForm(ModelForm):
    class Meta:
        model = Projects
        fields = ['title','description','start_date','due_date','file']
        widgets = {
            "title" : forms.TextInput(attrs={'class':'form-control2'}),
            "description" : forms.Textarea(attrs={'class':'form-control2'}),
            "start_date" : forms.TextInput(attrs={'class':'form-control2','type':'date'}),
            "due_date" : forms.TextInput(attrs={'class':'form-control2','type':'date'}),
            'team' : forms.Select(attrs={'class':'form-control2','type':'select'}),
            'file' : forms.FileInput(attrs={'class':'form-control2'}),
        }
class ProjectEditForm(ModelForm):    
    class Meta:
        model = Projects
        fields = ['title','description','start_date','due_date']
        widgets = {
            "title" : forms.TextInput(attrs={'class':'form-control2'}),
            "description" : forms.Textarea(attrs={'class':'form-control2'}),
            "start_date" : forms.TextInput(attrs={'class':'form-control2','type':'date'}),
            "due_date" : forms.TextInput(attrs={'class':'form-control2','type':'date'}),
            'team' : forms.Select(attrs={'class':'form-control2','type':'select'}),
        }

class timesheetAddForm(ModelForm):
    class Meta:
        model = timesheet
        fields = ['workinghours']
        widgets = {
            "workinghours" : forms.NumberInput(attrs={'class':'form-control2'}),
          
        }
class complaintAddForm(ModelForm):
    class Meta:
        model = complaints
        fields = ['title','description','file']
        widgets = {
            "title" : forms.TextInput(attrs={'class':'form-control2'}),
            "description" : forms.Textarea(attrs={'class':'form-control2'}),
            "file" : forms.FileInput(attrs={'class':'form-control2'}),
        }
class leaveAddForm(ModelForm):
    class Meta:
        model = leave
        fields = ['reason','date','ltype']
        widgets = {
            "reason" : forms.TextInput(attrs={'class':'form-control2'}),
            "date" : forms.DateInput(attrs={'class':'form-control2','type':'date'}),
            "ltype": forms.Select(attrs={'class': 'form-control2'})  # Add a class to the ltype field

        }     
        labels = {
            'ltype': 'Leave Type',  
        }   


class departmentaddform(forms.ModelForm):
    class Meta:
        model = Departments
        fields = "__all__"
        widgets = {
            'description' : forms.Textarea(attrs={'class':'contact-input'}),
          
        
        }      



class profiledit(ModelForm):
    class Meta:
        model = Register
        fields = ['username','email','contact']
        widgets = {
            "username" : forms.TextInput(attrs={'class':'form-control2'}),
            "email" : forms.TextInput(attrs={'class':'form-control2'}),
            "contact" : forms.TextInput(attrs={'class':'form-control2'}),
        }
        help_texts = {
            'username' : None
        }
