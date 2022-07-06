from django import forms
from . models import Employee
from django.contrib import messages
import re
from datetime import datetime



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


        widgets={
            'name':forms.TextInput(attrs=({'class':'form-control','placeholder':"Enter name"})),
            'dob':forms.DateInput(attrs=({'class':'form-control', 'type':'date'})),
            'email':forms.EmailInput(attrs=({'class':'form-control','placeholder':"Email"})),
            'phone':forms.NumberInput(attrs=({'class':'form-control','placeholder':"phone"})),

        }
    def clean(self):
 
        # data from the form is fetched using super function
        super(EmployeeForm, self).clean()
         
        # extract the username and text field from the data
        name = self.cleaned_data.get('name')
        phone = self.cleaned_data.get('phone')
        email = self.cleaned_data.get('email')
        dob = self.cleaned_data.get('dob')
        curdate = datetime.now().date()
        pattern = '^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@google.com$'
        result=re.match(pattern, email)
 
        # conditions to be met for the username length
            
        if len(name) < 5:
            self._errors['Name'] = self.error_class([
                'Minimum 5 characters required'])
        if len(str(phone)) !=10:
            self._errors['phone'] = self.error_class([
                'Phone number  Should Contain exactr 10 characters'])
        if ((curdate-dob).days)/365 < 20:
            self._errors['DOB'] = self.error_class([
                'Age should be greater than 20 years'])
        if not result:
            self._errors['Email'] = self.error_class([
                "Only domain with 'google' is supported"])
       
 
        # return any errors if found
        return self.cleaned_data