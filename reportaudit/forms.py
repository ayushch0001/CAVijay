from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from .models import AuditType, BackendReport, MainReport, Customer ,Audit ,Month ,Cluster
from django import forms

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class ClusterForm(forms.ModelForm):
    class Meta:
        model = Cluster
        fields = [ 'name' ]
        
class customerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [ 'address', 'cluster', 'nameOfOrganization','block','district']
        
        
class auditTypeForm(forms.ModelForm):
    class Meta:
        model = AuditType
        fields = ['name']
        
        
class backendReportForm(forms.ModelForm):
    class Meta:
        model = BackendReport
        fields = ['auditType', 'title' ,'cashOrBank','receiptOrPayment','dict']



class AuditForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=[r'%Y-%m-%d'],  # Allows both formats
    )
    class Meta:
        model = Audit
        fields = [ 'Udin','yearEnd','yearStart','date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
       
        
# class mainReportForm(forms.ModelForm):
    # class Meta:
    #     model = MainReport
    #     fields = ['auditType', 'title', 'dict']